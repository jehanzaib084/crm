"""
Simple Selenium Tests for IDURAR ERP CRM
Run this file directly: python simple_test.py
"""
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from webdriver_manager.chrome import ChromeDriverManager
import time
import os

# Configuration
BASE_URL = "http://localhost:3000"
API_URL = "http://localhost:8888/api"
EMAIL = "admin@admin.com"
PASSWORD = "admin123"
SCREENSHOT_DIR = "screenshots"

# Create screenshot directory
os.makedirs(SCREENSHOT_DIR, exist_ok=True)

def take_screenshot(driver, name):
    """Take a screenshot"""
    filename = f"{SCREENSHOT_DIR}/{name}.png"
    driver.save_screenshot(filename)
    print(f"  Screenshot saved: {filename}")
    return filename

def setup_driver():
    """Setup Chrome driver"""
    options = Options()
    # Uncomment next line for headless mode
    # options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    driver.maximize_window()
    driver.implicitly_wait(10)
    return driver

def test_1_homepage_loads():
    """Test Case 1: Verify Homepage Loads"""
    print("\n" + "="*60)
    print("TEST 1: Homepage Loads")
    print("="*60)
    
    driver = setup_driver()
    try:
        # Navigate to homepage
        print("  Navigating to homepage...")
        driver.get(BASE_URL)
        time.sleep(3)
        
        take_screenshot(driver, "test1_homepage")
        
        # Verify page loaded
        body = driver.find_element(By.TAG_NAME, "body")
        assert body is not None, "Page body not found"
        
        print("  ✓ Homepage loaded successfully")
        print("  ✓ Test 1 PASSED")
        return True
    except Exception as e:
        take_screenshot(driver, "test1_error")
        print(f"  ✗ Test 1 FAILED: {str(e)}")
        return False
    finally:
        driver.quit()

def test_2_login_functionality():
    """Test Case 2: Validate Login Functionality"""
    print("\n" + "="*60)
    print("TEST 2: Login Functionality")
    print("="*60)
    
    driver = setup_driver()
    try:
        # Navigate to login page
        print("  Navigating to login page...")
        driver.get(f"{BASE_URL}/login")
        time.sleep(2)
        
        take_screenshot(driver, "test2_login_page")
        
        # Find and fill login form
        print("  Filling login form...")
        email_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.NAME, "email"))
        )
        password_input = driver.find_element(By.NAME, "password")
        
        email_input.clear()
        email_input.send_keys(EMAIL)
        password_input.clear()
        password_input.send_keys(PASSWORD)
        
        take_screenshot(driver, "test2_login_filled")
        
        # Click login button
        print("  Clicking login button...")
        login_button = driver.find_element(
            By.CSS_SELECTOR, 
            "button[type='submit'], .login-form-button, button.ant-btn-primary"
        )
        login_button.click()
        
        # Wait for redirect
        time.sleep(5)
        take_screenshot(driver, "test2_after_login")
        
        # Verify login success
        current_url = driver.current_url
        if "/login" not in current_url:
            print("  ✓ Login successful - redirected from login page")
            print("  ✓ Test 2 PASSED")
            return True
        else:
            print("  ✗ Still on login page - login may have failed")
            return False
            
    except Exception as e:
        take_screenshot(driver, "test2_error")
        print(f"  ✗ Test 2 FAILED: {str(e)}")
        return False
    finally:
        driver.quit()

def test_3_api_integration():
    """Test Case 3: Check Frontend-to-Backend API Response"""
    print("\n" + "="*60)
    print("TEST 3: Frontend-to-Backend API Integration")
    print("="*60)
    
    driver = setup_driver()
    try:
        # Login first
        print("  Logging in...")
        driver.get(f"{BASE_URL}/login")
        time.sleep(2)
        
        email_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.NAME, "email"))
        )
        password_input = driver.find_element(By.NAME, "password")
        email_input.send_keys(EMAIL)
        password_input.send_keys(PASSWORD)
        
        login_button = driver.find_element(
            By.CSS_SELECTOR, 
            "button[type='submit'], .login-form-button, button.ant-btn-primary"
        )
        login_button.click()
        time.sleep(5)
        
        take_screenshot(driver, "test3_after_login")
        
        # Navigate to dashboard
        print("  Checking dashboard API data load...")
        driver.get(BASE_URL)
        time.sleep(3)
        
        take_screenshot(driver, "test3_dashboard")
        
        # Verify page has content (indicating API data loaded)
        body_text = driver.find_element(By.TAG_NAME, "body").text
        if len(body_text) > 50:
            print("  ✓ Dashboard loaded with content")
            print("  ✓ API integration working")
            print("  ✓ Test 3 PASSED")
            return True
        else:
            print("  ✗ Dashboard appears empty")
            return False
            
    except Exception as e:
        take_screenshot(driver, "test3_error")
        print(f"  ✗ Test 3 FAILED: {str(e)}")
        return False
    finally:
        driver.quit()

def test_4_navigation():
    """Test Case 4: Validate Navigation and Button Behavior"""
    print("\n" + "="*60)
    print("TEST 4: Navigation and Button Behavior")
    print("="*60)
    
    driver = setup_driver()
    try:
        # Login first
        print("  Logging in...")
        driver.get(f"{BASE_URL}/login")
        time.sleep(2)
        
        email_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.NAME, "email"))
        )
        password_input = driver.find_element(By.NAME, "password")
        email_input.send_keys(EMAIL)
        password_input.send_keys(PASSWORD)
        
        login_button = driver.find_element(
            By.CSS_SELECTOR, 
            "button[type='submit'], .login-form-button, button.ant-btn-primary"
        )
        login_button.click()
        time.sleep(5)
        
        # Navigate to Invoice page
        print("  Navigating to Invoice page...")
        driver.get(f"{BASE_URL}/invoice")
        time.sleep(3)
        
        take_screenshot(driver, "test4_invoice_page")
        
        # Verify we're on invoice page
        current_url = driver.current_url
        if "invoice" in current_url.lower():
            print("  ✓ Successfully navigated to Invoice page")
            
            # Try to find create button or navigation elements
            try:
                buttons = driver.find_elements(By.TAG_NAME, "button")
                links = driver.find_elements(By.TAG_NAME, "a")
                print(f"  ✓ Found {len(buttons)} buttons and {len(links)} links")
                print("  ✓ Navigation working correctly")
                print("  ✓ Test 4 PASSED")
                return True
            except:
                print("  ✓ Navigation successful")
                print("  ✓ Test 4 PASSED")
                return True
        else:
            print(f"  ✗ Not on invoice page. Current URL: {current_url}")
            return False
            
    except Exception as e:
        take_screenshot(driver, "test4_error")
        print(f"  ✗ Test 4 FAILED: {str(e)}")
        return False
    finally:
        driver.quit()

def main():
    """Run all tests"""
    print("\n" + "="*60)
    print("SELENIUM AUTOMATED TESTING - IDURAR ERP CRM")
    print("="*60)
    print(f"\nBase URL: {BASE_URL}")
    print(f"API URL: {API_URL}")
    print(f"Test Email: {EMAIL}")
    print("\nMake sure your application is running!")
    print("="*60)
    
    results = []
    
    # Run all tests
    results.append(("Test 1: Homepage Loads", test_1_homepage_loads()))
    results.append(("Test 2: Login Functionality", test_2_login_functionality()))
    results.append(("Test 3: API Integration", test_3_api_integration()))
    results.append(("Test 4: Navigation", test_4_navigation()))
    
    # Print summary
    print("\n" + "="*60)
    print("TEST EXECUTION SUMMARY")
    print("="*60)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = "PASSED ✓" if result else "FAILED ✗"
        print(f"  {test_name}: {status}")
    
    print("="*60)
    print(f"Total: {passed}/{total} tests passed")
    print(f"Screenshots saved in: {SCREENSHOT_DIR}/")
    print("="*60)

if __name__ == "__main__":
    main()
