/**
 * Backend Validation Tests
 * Tests backend code validation and structure
 */

const assert = require('assert');
const fs = require('fs');
const path = require('path');

// Test 1: Server file exists and is readable
function testServerFileExists() {
  try {
    const serverPath = path.join(__dirname, '../src/server.js');
    assert(fs.existsSync(serverPath), 'server.js should exist');
    const stats = fs.statSync(serverPath);
    assert(stats.isFile(), 'server.js should be a file');
    assert(stats.size > 0, 'server.js should not be empty');
    console.log('✅ Test 1: Server file validation passed');
    return true;
  } catch (error) {
    console.error('❌ Test 1: Server file validation failed:', error.message);
    return false;
  }
}

// Test 2: App file exists and is readable
function testAppFileExists() {
  try {
    const appPath = path.join(__dirname, '../src/app.js');
    assert(fs.existsSync(appPath), 'app.js should exist');
    const stats = fs.statSync(appPath);
    assert(stats.isFile(), 'app.js should be a file');
    assert(stats.size > 0, 'app.js should not be empty');
    console.log('✅ Test 2: App file validation passed');
    return true;
  } catch (error) {
    console.error('❌ Test 2: App file validation failed:', error.message);
    return false;
  }
}

// Test 3: Package.json is valid
function testPackageJson() {
  try {
    const packagePath = path.join(__dirname, '../package.json');
    assert(fs.existsSync(packagePath), 'package.json should exist');
    const packageContent = fs.readFileSync(packagePath, 'utf8');
    const packageJson = JSON.parse(packageContent);
    assert(packageJson.name, 'package.json should have name');
    assert(packageJson.version, 'package.json should have version');
    assert(packageJson.scripts, 'package.json should have scripts');
    assert(packageJson.scripts.start, 'package.json should have start script');
    console.log('✅ Test 3: Package.json validation passed');
    return true;
  } catch (error) {
    console.error('❌ Test 3: Package.json validation failed:', error.message);
    return false;
  }
}

// Test 4: Environment file structure
function testEnvFile() {
  try {
    const envPath = path.join(__dirname, '../.env');
    if (fs.existsSync(envPath)) {
      const envContent = fs.readFileSync(envPath, 'utf8');
      assert(envContent.length > 0, '.env file should not be empty');
      console.log('✅ Test 4: Environment file validation passed');
    } else {
      console.log('⚠️  Test 4: .env file not found (this is OK for CI/CD)');
    }
    return true;
  } catch (error) {
    console.error('❌ Test 4: Environment file validation failed:', error.message);
    return false;
  }
}

// Run all tests
function runTests() {
  console.log('🧪 Running Backend Validation Tests...\n');
  
  const results = [
    testServerFileExists(),
    testAppFileExists(),
    testPackageJson(),
    testEnvFile()
  ];
  
  const passed = results.filter(r => r).length;
  const total = results.length;
  
  console.log(`\n📊 Test Results: ${passed}/${total} tests passed`);
  
  if (passed === total) {
    console.log('✅ All validation tests passed!');
    process.exit(0);
  } else {
    console.log('❌ Some validation tests failed!');
    process.exit(1);
  }
}

runTests();
