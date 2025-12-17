/**
 * Test Runner
 * Runs all backend tests
 */

const { spawn } = require('child_process');
const path = require('path');

const tests = [
  path.join(__dirname, 'validation.test.js'),
  path.join(__dirname, 'health.test.js')
];

let passed = 0;
let failed = 0;

function runTest(testFile) {
  return new Promise((resolve) => {
    console.log(`\n📝 Running: ${path.basename(testFile)}\n`);
    
    const testProcess = spawn('node', [testFile], {
      stdio: 'inherit',
      cwd: path.join(__dirname, '..')
    });
    
    testProcess.on('close', (code) => {
      if (code === 0) {
        passed++;
        resolve(true);
      } else {
        failed++;
        resolve(false);
      }
    });
    
    testProcess.on('error', (error) => {
      console.error(`Error running test: ${error.message}`);
      failed++;
      resolve(false);
    });
  });
}

async function runAllTests() {
  console.log('🚀 Starting Backend Test Suite...\n');
  console.log('='.repeat(50));
  
  for (const test of tests) {
    await runTest(test);
  }
  
  console.log('\n' + '='.repeat(50));
  console.log(`\n📊 Final Results:`);
  console.log(`   ✅ Passed: ${passed}`);
  console.log(`   ❌ Failed: ${failed}`);
  console.log(`   📦 Total: ${passed + failed}\n`);
  
  if (failed === 0) {
    console.log('✅ All tests passed!');
    process.exit(0);
  } else {
    console.log('❌ Some tests failed!');
    process.exit(1);
  }
}

runAllTests();
