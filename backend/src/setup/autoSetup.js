// Auto-setup script that runs on server startup
// Creates admin user and initial data if database is empty

require('dotenv').config({ path: '.env' });
require('dotenv').config({ path: '.env.local' });
const { globSync } = require('glob');
const fs = require('fs');
const { generate: uniqueId } = require('shortid');
const mongoose = require('mongoose');

async function autoSetup() {
  try {
    const Admin = require('../models/coreModels/Admin');
    const AdminPassword = require('../models/coreModels/AdminPassword');
    const Setting = require('../models/coreModels/Setting');
    const PaymentMode = require('../models/appModels/PaymentMode');
    const Taxes = require('../models/appModels/Taxes');

    // Check if admin exists
    const adminCount = await Admin.countDocuments();
    
    if (adminCount > 0) {
      console.log('✅ Admin user already exists. Skipping auto-setup.');
      return;
    }

    console.log('📦 No admin found. Running auto-setup...');

    // Create admin user
    const newAdminPassword = new AdminPassword();
    const salt = uniqueId();
    const passwordHash = newAdminPassword.generateHash(salt, 'admin123');

    const demoAdmin = {
      email: 'admin@admin.com',
      name: 'IDURAR',
      surname: 'Admin',
      enabled: true,
      role: 'owner',
    };
    const result = await new Admin(demoAdmin).save();

    const AdminPasswordData = {
      password: passwordHash,
      emailVerified: true,
      salt: salt,
      user: result._id,
    };
    await new AdminPassword(AdminPasswordData).save();
    console.log('👍 Admin created: admin@admin.com / admin123');

    // Create settings
    const settingFiles = [];
    const settingsFiles = globSync('./src/setup/defaultSettings/**/*.json');

    for (const filePath of settingsFiles) {
      const file = JSON.parse(fs.readFileSync(filePath, 'utf-8'));
      settingFiles.push(...file);
    }

    await Setting.insertMany(settingFiles);
    console.log('👍 Settings created');

    // Create default tax
    await Taxes.insertMany([{ taxName: 'Tax 0%', taxValue: '0', isDefault: true }]);
    console.log('👍 Taxes created');

    // Create default payment mode
    await PaymentMode.insertMany([
      {
        name: 'Default Payment',
        description: 'Default Payment Mode (Cash , Wire Transfert)',
        isDefault: true,
      },
    ]);
    console.log('👍 PaymentMode created');

    console.log('🥳 Auto-setup completed successfully!');
    console.log('📧 Login credentials: admin@admin.com / admin123');
  } catch (error) {
    console.error('❌ Auto-setup error:', error.message);
    // Don't throw - let server continue even if setup fails
  }
}

module.exports = autoSetup;
