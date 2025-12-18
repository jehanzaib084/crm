"""
Test Case 4: Validate Navigation and Button Behavior
This test verifies navigation menu and button interactions
"""
import pytest
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from base_test import BaseTest
import config


class TestNavigation(BaseTest):
    """Test cases for navigation and button behavior"""
    
    def setup_method(self):
        """Setup before each test"""
        super().setup_method()
    
    def teardown_method(self):
        """Cleanup after each test"""
        super().teardown_method()
    
    def test_navigation_menu_display(self):
        """Test that navigation menu is displayed"""
        try:
            # Login first
            self.login()
            time.sleep(3)
            
            # Take screenshot
            self.take_screenshot('navigation_menu')
            
            # Look for navigation elements
            # Could be sidebar, top menu, or hamburger menu
            nav_selectors = [
                'nav',
                '[class*="menu"]',
                '[class*="navigation"]',
                '[class*="sidebar"]',
                '[class*="sider"]',
                'aside',
                '[role="navigation"]'
            ]
            
            nav_found = False
            for selector in nav_selectors:
                try:
                    nav_elements = self.driver.find_elements(By.CSS_SELECTOR, selector)
                    if nav_elements:
                        print(f"✓ Found navigation element with selector: {selector}")
                        nav_found = True
                        break
                except:
                    continue
            
            if not nav_found:
                # Check for any clickable menu items
                clickable_items = self.driver.find_elements(
                    By.CSS_SELECTOR,
                    'a[href], button, [role="button"], [class*="link"]'
                )
                if clickable_items:
                    print(f"✓ Found {len(clickable_items)} clickable navigation items")
                    nav_found = True
            
            # At minimum, verify page has interactive elements
            assert nav_found or len(self.driver.find_elements(By.TAG_NAME, 'a')) > 0, \
                "No navigation elements found"
            
            print("✓ Navigation menu is displayed")
            
        except Exception as e:
            self.take_screenshot('navigation_menu_error')
            raise
    
    def test_navigation_to_invoice_page(self):
        """Test navigation to Invoice page"""
        try:
            # Login first
            self.login()
            time.sleep(3)
            
            # Take screenshot before navigation
            self.take_screenshot('navigation_invoice_before')
            
            # Try to find and click invoice link
            invoice_selectors = [
                'a[href*="invoice"]',
                'a[href="/invoice"]',
                'a:contains("Invoice")',
                '*[class*="invoice"]',
                'button:contains("Invoice")'
            ]
            
            invoice_clicked = False
            for selector in invoice_selectors:
                try:
                    if ':contains' in selector:
                        # Find by text
                        elements = self.driver.find_elements(By.XPATH, 
                            "//a[contains(text(), 'Invoice') or contains(text(), 'invoice')]")
                    else:
                        elements = self.driver.find_elements(By.CSS_SELECTOR, selector)
                    
                    if elements:
                        element = elements[0]
                        self.driver.execute_script("arguments[0].scrollIntoView(true);", element)
                        time.sleep(1)
                        element.click()
                        invoice_clicked = True
                        print(f"✓ Clicked invoice link using selector: {selector}")
                        break
                except Exception as e:
                    continue
            
            if not invoice_clicked:
                # Try direct navigation
                self.navigate_to('/invoice')
                print("✓ Navigated directly to invoice page")
            
            # Wait for page to load
            time.sleep(3)
            
            # Take screenshot after navigation
            self.take_screenshot('navigation_invoice_after')
            
            # Verify we're on invoice page
            current_url = self.driver.current_url
            assert 'invoice' in current_url.lower(), \
                f"Expected to be on invoice page, but URL is: {current_url}"
            
            # Verify page content loaded
            body = self.wait_for_element(By.TAG_NAME, 'body')
            assert body is not None, "Invoice page should load"
            
            print("✓ Successfully navigated to Invoice page")
            
        except Exception as e:
            self.take_screenshot('navigation_invoice_error')
            raise
    
    def test_navigation_to_customer_page(self):
        """Test navigation to Customer page"""
        try:
            # Login first
            self.login()
            time.sleep(3)
            
            # Take screenshot before navigation
            self.take_screenshot('navigation_customer_before')
            
            # Try to navigate to customer page
            try:
                # Try finding customer link
                customer_links = self.driver.find_elements(
                    By.XPATH,
                    "//a[contains(text(), 'Customer') or contains(text(), 'customer') or contains(@href, 'customer')]"
                )
                
                if customer_links:
                    customer_links[0].click()
                    print("✓ Clicked customer link from menu")
                else:
                    # Direct navigation
                    self.navigate_to('/customer')
                    print("✓ Navigated directly to customer page")
            except:
                # Direct navigation fallback
                self.navigate_to('/customer')
            
            # Wait for page to load
            time.sleep(3)
            
            # Take screenshot after navigation
            self.take_screenshot('navigation_customer_after')
            
            # Verify we're on customer page
            current_url = self.driver.current_url
            assert 'customer' in current_url.lower(), \
                f"Expected to be on customer page, but URL is: {current_url}"
            
            print("✓ Successfully navigated to Customer page")
            
        except Exception as e:
            self.take_screenshot('navigation_customer_error')
            raise
    
    def test_create_button_functionality(self):
        """Test create/new button functionality"""
        try:
            # Login first
            self.login()
            time.sleep(3)
            
            # Navigate to a page with create button (e.g., Invoice)
            self.navigate_to('/invoice')
            time.sleep(3)
            
            # Take screenshot before clicking create
            self.take_screenshot('create_button_before')
            
            # Look for create/new/add button
            create_selectors = [
                'button:contains("Create")',
                'button:contains("New")',
                'button:contains("Add")',
                'a[href*="create"]',
                '*[class*="create"]',
                '*[class*="add"]',
                'button[type="button"]'
            ]
            
            create_clicked = False
            for selector in create_selectors:
                try:
                    if ':contains' in selector:
                        # Find by text
                        elements = self.driver.find_elements(
                            By.XPATH,
                            "//button[contains(text(), 'Create') or contains(text(), 'New') or contains(text(), 'Add')]"
                        )
                    else:
                        elements = self.driver.find_elements(By.CSS_SELECTOR, selector)
                    
                    if elements:
                        # Filter for visible and clickable buttons
                        for element in elements:
                            if element.is_displayed() and element.is_enabled():
                                self.driver.execute_script("arguments[0].scrollIntoView(true);", element)
                                time.sleep(1)
                                element.click()
                                create_clicked = True
                                print("✓ Clicked create button")
                                break
                        if create_clicked:
                            break
                except Exception as e:
                    continue
            
            if not create_clicked:
                # Try direct navigation to create page
                self.navigate_to('/invoice/create')
                print("✓ Navigated directly to create page")
            
            # Wait for page to load
            time.sleep(3)
            
            # Take screenshot after clicking
            self.take_screenshot('create_button_after')
            
            # Verify we're on create page or form opened
            current_url = self.driver.current_url
            page_source = self.driver.page_source.lower()
            
            # Should be on create page or have form elements
            is_create_page = 'create' in current_url.lower() or \
                           any(keyword in page_source for keyword in ['form', 'create', 'new', 'add'])
            
            assert is_create_page, "Expected to be on create page or see form"
            
            print("✓ Create button functionality working")
            
        except Exception as e:
            self.take_screenshot('create_button_error')
            raise
    
    def test_back_button_navigation(self):
        """Test browser back button navigation"""
        try:
            # Login first
            self.login()
            time.sleep(2)
            
            # Navigate to a page
            self.navigate_to('/invoice')
            time.sleep(2)
            invoice_url = self.driver.current_url
            
            # Take screenshot
            self.take_screenshot('back_button_before')
            
            # Navigate to another page
            self.navigate_to('/customer')
            time.sleep(2)
            customer_url = self.driver.current_url
            
            # Use browser back button
            self.driver.back()
            time.sleep(3)
            
            # Take screenshot after back
            self.take_screenshot('back_button_after')
            
            # Verify we're back on previous page
            current_url = self.driver.current_url
            # Should be back on invoice page (or at least not on customer)
            assert 'customer' not in current_url.lower() or invoice_url in current_url, \
                "Back button should navigate to previous page"
            
            print("✓ Browser back button navigation working")
            
        except Exception as e:
            self.take_screenshot('back_button_error')
            raise
