// MongoDB initialization script
// This runs automatically when MongoDB starts for the first time

// Create database and collections
db = db.getSiblingDB('idurar');

// Create collections (they will be created automatically when data is inserted)
db.createCollection('admins');
db.createCollection('adminpasswords');
db.createCollection('settings');
db.createCollection('clients');
db.createCollection('invoices');
db.createCollection('quotes');
db.createCollection('payments');

print('MongoDB initialized for IDURAR ERP/CRM');
