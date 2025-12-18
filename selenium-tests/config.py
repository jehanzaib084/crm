"""
Configuration file for Selenium tests
"""
import os

# Application URLs
BASE_URL = os.getenv('BASE_URL', 'http://localhost:3000')
API_BASE_URL = os.getenv('API_BASE_URL', 'http://localhost:8888/api')

# Test Credentials
TEST_EMAIL = os.getenv('TEST_EMAIL', 'admin@admin.com')
TEST_PASSWORD = os.getenv('TEST_PASSWORD', 'admin123')

# Screenshot settings
SCREENSHOT_DIR = os.path.join(os.path.dirname(__file__), 'screenshots')
REPORT_DIR = os.path.join(os.path.dirname(__file__), 'reports')

# Browser settings
BROWSER_ENV = os.getenv('BROWSER', 'chrome')
# Only use chrome, firefox, or edge - ignore other values
if BROWSER_ENV.lower() in ['chrome', 'firefox', 'edge']:
    BROWSER = BROWSER_ENV.lower()
else:
    BROWSER = 'chrome'  # Default to chrome
HEADLESS = os.getenv('HEADLESS', 'False').lower() == 'true'
IMPLICIT_WAIT = 10
EXPLICIT_WAIT = 20

# Test timeouts
PAGE_LOAD_TIMEOUT = 30
ELEMENT_TIMEOUT = 10
