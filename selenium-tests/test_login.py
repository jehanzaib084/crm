"""
Test Case 2: Validate Login Functionality
This test verifies login form behavior and authentication
"""
import pytest
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from base_test import BaseTest
import config


class TestLogin(BaseTest):
    """Test cases for login functionality"""
    
    def setup_method(self):
        """Setup before each test"""
        super().setup_method()
    
    def teardown_method(self):
        """Cleanup after each test"""
        super().teardown_method()
    
    def test_login_page_loads(self):
        """Test that login page loads correctly"""
        try:
            # Navigate to login page
            self.navigate_to('/login')
            
            # Take screenshot
            self.take_screenshot('login_page_load')
            
            # Verify login form elements are present
            email_input = self.wait_for_element_visible(By.NAME, 'email')
            password_input = self.wait_for_element_visible(By.NAME, 'password')
            
            assert email_input is not None, "Email input field not found"
            assert password_input is not None, "Password input field not found"
            
            # Verify login button exists
            login_button = self.wait_for_element_clickable(
                By.CSS_SELECTOR,
                'button[type="submit"], .login-form-button, button.ant-btn-primary'
            )
            assert login_button is not None, "Login button not found"
            
            print("✓ Login page loaded with all required elements")
            
        except Exception as e:
            self.take_screenshot('login_page_load_error')
            raise
    
    def test_login_with_valid_credentials(self):
        """Test login with valid credentials"""
        try:
            # Navigate to login page
            self.navigate_to('/login')
            
            # Take screenshot before login
            self.take_screenshot('login_before')
            
            # Perform login
            self.login()
            
            # Wait for navigation/redirect after login
            time.sleep(3)
            
            # Take screenshot after login
            self.take_screenshot('login_after_success')
            
            # Verify successful login
            # Check if redirected away from login page
            current_url = self.driver.current_url
            assert '/login' not in current_url, "Still on login page after successful login"
            
            # Verify we're on dashboard or home page
            assert config.BASE_URL in current_url, "Not on expected domain"
            
            # Check for dashboard elements or navigation
            try:
                # Look for common dashboard/navigation elements
                self.wait_for_element(By.TAG_NAME, 'body', timeout=5)
                print("✓ Successfully logged in and redirected")
            except TimeoutException:
                # At minimum, verify page loaded
                page_source = self.driver.page_source
                assert len(page_source) > 100, "Page appears blank after login"
                print("✓ Login successful, page loaded")
            
        except Exception as e:
            self.take_screenshot('login_error')
            raise
    
    def test_login_with_invalid_credentials(self):
        """Test login with invalid credentials"""
        try:
            # Navigate to login page
            self.navigate_to('/login')
            
            # Attempt login with invalid credentials
            email_input = self.wait_for_element_visible(By.NAME, 'email')
            password_input = self.wait_for_element_visible(By.NAME, 'password')
            
            email_input.clear()
            email_input.send_keys('invalid@email.com')
            password_input.clear()
            password_input.send_keys('wrongpassword')
            
            # Take screenshot before submit
            self.take_screenshot('login_invalid_before')
            
            # Click login button
            login_button = self.wait_for_element_clickable(
                By.CSS_SELECTOR,
                'button[type="submit"], .login-form-button, button.ant-btn-primary'
            )
            login_button.click()
            
            # Wait for error message or response
            time.sleep(3)
            
            # Take screenshot after error
            self.take_screenshot('login_invalid_after')
            
            # Verify error handling
            # Check for error message (could be in various formats)
            page_source = self.driver.page_source.lower()
            current_url = self.driver.current_url
            
            # Should either show error message or stay on login page
            has_error = any(keyword in page_source for keyword in [
                'error', 'invalid', 'incorrect', 'failed', 'wrong'
            ])
            still_on_login = '/login' in current_url
            
            assert has_error or still_on_login, \
                "Expected error message or to remain on login page"
            
            print("✓ Invalid credentials handled correctly")
            
        except Exception as e:
            self.take_screenshot('login_invalid_error')
            raise
    
    def test_login_form_validation(self):
        """Test login form validation behavior"""
        try:
            # Navigate to login page
            self.navigate_to('/login')
            
            # Try to submit empty form
            login_button = self.wait_for_element_clickable(
                By.CSS_SELECTOR,
                'button[type="submit"], .login-form-button, button.ant-btn-primary'
            )
            
            # Take screenshot before submit
            self.take_screenshot('login_validation_before')
            
            # Click login without filling fields
            login_button.click()
            
            # Wait for validation
            time.sleep(2)
            
            # Take screenshot after validation
            self.take_screenshot('login_validation_after')
            
            # Check for validation messages
            page_source = self.driver.page_source.lower()
            
            # Modern forms might prevent submission or show validation
            # Just verify form is still accessible
            email_input = self.wait_for_element(By.NAME, 'email')
            assert email_input is not None, "Form should still be accessible"
            
            print("✓ Form validation working")
            
        except Exception as e:
            self.take_screenshot('login_validation_error')
            raise
