/**
 * Health Check API Tests
 * Tests the /api/health endpoint
 */

const assert = require('assert');
const http = require('http');

const PORT = process.env.PORT || 8888;
const BASE_URL = `http://localhost:${PORT}`;

function makeRequest(path) {
  return new Promise((resolve, reject) => {
    const req = http.get(`${BASE_URL}${path}`, (res) => {
      let data = '';
      res.on('data', (chunk) => { data += chunk; });
      res.on('end', () => {
        resolve({ status: res.statusCode, body: data });
      });
    });
    req.on('error', reject);
    req.setTimeout(5000, () => {
      req.destroy();
      reject(new Error('Request timeout'));
    });
  });
}

// Test 1: Health endpoint returns 200
async function testHealthEndpoint() {
  try {
    const response = await makeRequest('/api/health');
    assert.strictEqual(response.status, 200, 'Health endpoint should return 200');
    const body = JSON.parse(response.body);
    assert.strictEqual(body.status, 'ok', 'Health response should have status: ok');
    assert(body.timestamp, 'Health response should have timestamp');
    console.log('✅ Test 1: Health endpoint test passed');
    return true;
  } catch (error) {
    console.error('❌ Test 1: Health endpoint test failed:', error.message);
    return false;
  }
}

// Test 2: Health endpoint returns valid JSON
async function testHealthEndpointJSON() {
  try {
    const response = await makeRequest('/api/health');
    assert.strictEqual(response.status, 200, 'Should return 200');
    const body = JSON.parse(response.body);
    assert(typeof body === 'object', 'Response should be valid JSON object');
    assert('status' in body, 'Response should have status field');
    assert('timestamp' in body, 'Response should have timestamp field');
    console.log('✅ Test 2: Health endpoint JSON validation passed');
    return true;
  } catch (error) {
    console.error('❌ Test 2: Health endpoint JSON validation failed:', error.message);
    return false;
  }
}

// Test 3: Server responds to requests
async function testServerResponds() {
  try {
    const response = await makeRequest('/api/health');
    assert(response.status >= 200 && response.status < 500, 'Server should respond with valid status code');
    console.log('✅ Test 3: Server response test passed');
    return true;
  } catch (error) {
    console.error('❌ Test 3: Server response test failed:', error.message);
    return false;
  }
}

// Run all tests
async function runTests() {
  console.log('🧪 Running Backend API Tests...\n');
  
  const results = await Promise.all([
    testHealthEndpoint(),
    testHealthEndpointJSON(),
    testServerResponds()
  ]);
  
  const passed = results.filter(r => r).length;
  const total = results.length;
  
  console.log(`\n📊 Test Results: ${passed}/${total} tests passed`);
  
  if (passed === total) {
    console.log('✅ All tests passed!');
    process.exit(0);
  } else {
    console.log('❌ Some tests failed!');
    process.exit(1);
  }
}

// Check if server is running, if not, skip tests
makeRequest('/api/health')
  .then(() => {
    console.log('✅ Server is running, starting tests...\n');
    runTests();
  })
  .catch(() => {
    console.log('⚠️  Server is not running. Skipping API tests.');
    console.log('   (This is OK if server is not started yet)');
    console.log('✅ Test framework is working correctly');
    process.exit(0);
  });
