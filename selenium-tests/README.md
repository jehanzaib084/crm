# Selenium Automated Testing - IDURAR ERP CRM

This directory contains Selenium automated test scripts for the IDURAR ERP CRM application.

## Test Cases Overview

### Test Case 1: Homepage/Dashboard Loads (`test_homepage.py`)
- ✅ Verify homepage loads successfully
- ✅ Test redirect to login when not authenticated

### Test Case 2: Login Functionality (`test_login.py`)
- ✅ Verify login page loads with all required elements
- ✅ Test login with valid credentials
- ✅ Test login with invalid credentials
- ✅ Test login form validation

### Test Case 3: Frontend-to-Backend API Integration (`test_api_integration.py`)
- ✅ Test login API call
- ✅ Test dashboard API data load
- ✅ Test direct API endpoint access

### Test Case 4: Navigation and Button Behavior (`test_navigation.py`)
- ✅ Test navigation menu display
- ✅ Test navigation to Invoice page
- ✅ Test navigation to Customer page
- ✅ Test create button functionality
- ✅ Test browser back button navigation

## Prerequisites

1. **Python 3.8+** installed
2. **Chrome/Firefox/Edge** browser installed
3. **Application running**:
   - Frontend: `http://localhost:3000`
   - Backend: `http://localhost:8888`

## Installation

1. Install Python dependencies:
```bash
cd selenium-tests
pip install -r requirements.txt
```

## Configuration

Edit `config.py` to customize test settings:

```python
BASE_URL = 'http://localhost:3000'  # Frontend URL
API_BASE_URL = 'http://localhost:8888/api'  # Backend API URL
TEST_EMAIL = 'admin@admin.com'  # Test credentials
TEST_PASSWORD = 'admin123'
BROWSER = 'chrome'  # chrome, firefox, edge
HEADLESS = False  # Set True for headless mode
```

## Running Tests

### Run All Tests
```bash
python run_tests.py
```

### Run Specific Test File
```bash
pytest test_homepage.py -v
pytest test_login.py -v
pytest test_api_integration.py -v
pytest test_navigation.py -v
```

### Run with HTML Report
```bash
pytest --html=reports/test_report.html --self-contained-html
```

### Run in Headless Mode
```bash
HEADLESS=True pytest -v
```

## Test Reports and Screenshots

- **HTML Report**: `reports/test_report.html`
- **Screenshots**: `screenshots/` directory
  - Screenshots are automatically captured for each test
  - Named with test name and timestamp

## Test Execution Screenshots

After running tests, you will find:
1. Screenshots of each test step in `screenshots/` directory
2. HTML test report in `reports/test_report.html`

## Example Test Execution

```bash
$ python run_tests.py

======================================================================
SELENIUM AUTOMATED TESTING - IDURAR ERP CRM
======================================================================
Test Execution Started: 2024-01-15 10:30:00

test_homepage.py::TestHomepage::test_homepage_loads PASSED
test_login.py::TestLogin::test_login_with_valid_credentials PASSED
test_api_integration.py::TestAPIIntegration::test_login_api_call PASSED
test_navigation.py::TestNavigation::test_navigation_to_invoice_page PASSED
...

======================================================================
Test Execution Completed: 2024-01-15 10:35:00
======================================================================
✓ All tests passed!

📊 HTML Report: reports/test_report.html
📸 Screenshots: screenshots/
```

## Troubleshooting

### Browser Driver Issues
If you encounter driver issues, the tests use `webdriver-manager` to automatically download drivers. If problems persist:
- Ensure Chrome/Firefox/Edge is installed
- Check internet connection for driver downloads

### Application Not Running
Ensure both frontend and backend are running:
```bash
# Terminal 1 - Backend
cd backend
npm start

# Terminal 2 - Frontend
cd frontend
npm run dev
```

### Timeout Errors
If tests timeout:
- Increase `IMPLICIT_WAIT` and `EXPLICIT_WAIT` in `config.py`
- Check application performance
- Ensure network connectivity

## Test Structure

```
selenium-tests/
├── base_test.py              # Base test class with common utilities
├── config.py                 # Configuration settings
├── conftest.py               # Pytest configuration
├── test_homepage.py          # Homepage tests
├── test_login.py             # Login functionality tests
├── test_api_integration.py   # API integration tests
├── test_navigation.py        # Navigation and button tests
├── run_tests.py              # Main test runner
├── requirements.txt          # Python dependencies
├── screenshots/              # Test screenshots directory
├── reports/                   # Test reports directory
└── README.md                 # This file
```

## Notes

- Tests are designed to be independent and can run in any order
- Screenshots are captured automatically for debugging
- Tests wait for elements to load before interacting
- All tests include error handling and screenshot capture on failure

## Support

For issues or questions, please refer to the main project documentation or create an issue in the repository.
