# Test Execution Guide

## Quick Start

### Option 1: Using Python directly
```bash
cd selenium-tests
pip install -r requirements.txt
python run_tests.py
```

### Option 2: Using the shell script
```bash
cd selenium-tests
./run_tests.sh
```

### Option 3: Using pytest directly
```bash
cd selenium-tests
pip install -r requirements.txt
pytest -v --html=reports/test_report.html --self-contained-html
```

## Prerequisites Checklist

Before running tests, ensure:

- [ ] **Frontend is running** on `http://localhost:3000`
  ```bash
  cd frontend
  npm run dev
  ```

- [ ] **Backend is running** on `http://localhost:8888`
  ```bash
  cd backend
  npm start
  ```

- [ ] **Python 3.8+** is installed
  ```bash
  python3 --version
  ```

- [ ] **Chrome/Firefox/Edge** browser is installed

## Test Execution Steps

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Verify application is running:**
   - Open browser and go to `http://localhost:3000`
   - You should see the login page

3. **Run tests:**
   ```bash
   python run_tests.py
   ```

4. **View results:**
   - HTML Report: `reports/test_report.html`
   - Screenshots: `screenshots/` directory

## Expected Test Results

### Test Case 1: Homepage Loads
- ✅ Homepage loads successfully
- ✅ Redirects to login when not authenticated

### Test Case 2: Login Functionality
- ✅ Login page loads with all elements
- ✅ Login with valid credentials succeeds
- ✅ Login with invalid credentials shows error
- ✅ Form validation works

### Test Case 3: API Integration
- ✅ Login API call works
- ✅ Dashboard loads data from API
- ✅ Backend API is accessible

### Test Case 4: Navigation
- ✅ Navigation menu displays
- ✅ Can navigate to Invoice page
- ✅ Can navigate to Customer page
- ✅ Create button works
- ✅ Browser back button works

## Screenshots

Screenshots are automatically captured:
- Before and after each major action
- On test failures
- At key verification points

Screenshot naming format: `{test_name}_{timestamp}.png`

## Troubleshooting

### Issue: "WebDriver not found"
**Solution:** The tests use `webdriver-manager` which automatically downloads drivers. Ensure you have internet connection.

### Issue: "Connection refused"
**Solution:** Ensure both frontend and backend servers are running.

### Issue: "Element not found"
**Solution:** 
- Check if application UI has changed
- Increase wait times in `config.py`
- Verify application is fully loaded

### Issue: "Tests timeout"
**Solution:**
- Increase `PAGE_LOAD_TIMEOUT` in `config.py`
- Check application performance
- Ensure network connectivity

## Configuration

Edit `config.py` to customize:

```python
BASE_URL = 'http://localhost:3000'  # Change if frontend runs on different port
API_BASE_URL = 'http://localhost:8888/api'  # Change if backend runs on different port
TEST_EMAIL = 'admin@admin.com'  # Default test credentials
TEST_PASSWORD = 'admin123'
BROWSER = 'chrome'  # Options: chrome, firefox, edge
HEADLESS = False  # Set True to run without browser window
```

## Running Individual Tests

```bash
# Run only homepage tests
pytest test_homepage.py -v

# Run only login tests
pytest test_login.py -v

# Run only API tests
pytest test_api_integration.py -v

# Run only navigation tests
pytest test_navigation.py -v
```

## Generating Reports

The test runner automatically generates:
- **HTML Report**: `reports/test_report.html` (self-contained, can be shared)
- **Console Output**: Detailed test execution log
- **Screenshots**: Visual evidence of test execution

## Submission Requirements

For your assignment submission, include:

1. ✅ **Selenium scripts** (all `.py` files in `selenium-tests/`)
2. ✅ **Screenshot of test run** (from `reports/test_report.html` or console output)
3. ✅ **Test execution report** (`reports/test_report.html`)

## Notes

- Tests are designed to be independent
- Each test cleans up after itself
- Screenshots help with debugging
- All tests include error handling
