"""
Base test class for Selenium tests
"""
import os
import time
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.edge.service import Service as EdgeService
from selenium.webdriver.edge.options import Options as EdgeOptions
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException, WebDriverException
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from webdriver_manager.microsoft import EdgeChromiumDriverManager
import config


class BaseTest:
    """Base class for all Selenium tests"""
    
    def setup_method(self):
        """Setup method called before each test"""
        self.driver = None
        self.wait = None
        self.screenshot_dir = config.SCREENSHOT_DIR
        os.makedirs(self.screenshot_dir, exist_ok=True)
        self.driver = self._create_driver()
        self.wait = WebDriverWait(self.driver, config.EXPLICIT_WAIT)
        self.driver.maximize_window()
        self.driver.implicitly_wait(config.IMPLICIT_WAIT)
        self.driver.set_page_load_timeout(config.PAGE_LOAD_TIMEOUT)
    
    def teardown_method(self):
        """Teardown method called after each test"""
        if self.driver:
            self.driver.quit()
    
    def _create_driver(self):
        """Create and return a WebDriver instance"""
        browser = config.BROWSER.lower()
        
        if browser == 'chrome':
            options = Options()
            if config.HEADLESS:
                options.add_argument('--headless')
            options.add_argument('--no-sandbox')
            options.add_argument('--disable-dev-shm-usage')
            options.add_argument('--disable-gpu')
            options.add_argument('--window-size=1920,1080')
            driver_path = ChromeDriverManager().install()
            # Find the actual chromedriver executable
            driver_dir = os.path.dirname(driver_path) if os.path.isfile(driver_path) else driver_path
            # Look for chromedriver in the directory
            possible_paths = [
                os.path.join(driver_dir, 'chromedriver'),
                os.path.join(driver_dir, 'chromedriver-linux64', 'chromedriver'),
                driver_path
            ]
            for path in possible_paths:
                if os.path.exists(path) and os.access(path, os.X_OK):
                    driver_path = path
                    break
            service = Service(driver_path)
            return webdriver.Chrome(service=service, options=options)
        
        elif browser == 'firefox':
            options = FirefoxOptions()
            if config.HEADLESS:
                options.add_argument('--headless')
            service = FirefoxService(GeckoDriverManager().install())
            return webdriver.Firefox(service=service, options=options)
        
        elif browser == 'edge':
            options = EdgeOptions()
            if config.HEADLESS:
                options.add_argument('--headless')
            service = EdgeService(EdgeChromiumDriverManager().install())
            return webdriver.Edge(service=service, options=options)
        
        else:
            raise ValueError(f"Unsupported browser: {browser}")
    
    def take_screenshot(self, name):
        """Take a screenshot and save it"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{name}_{timestamp}.png"
        filepath = os.path.join(self.screenshot_dir, filename)
        self.driver.save_screenshot(filepath)
        print(f"Screenshot saved: {filepath}")
        return filepath
    
    def wait_for_element(self, by, value, timeout=None):
        """Wait for an element to be present"""
        if timeout is None:
            timeout = config.ELEMENT_TIMEOUT
        wait = WebDriverWait(self.driver, timeout)
        return wait.until(EC.presence_of_element_located((by, value)))
    
    def wait_for_element_clickable(self, by, value, timeout=None):
        """Wait for an element to be clickable"""
        if timeout is None:
            timeout = config.ELEMENT_TIMEOUT
        wait = WebDriverWait(self.driver, timeout)
        return wait.until(EC.element_to_be_clickable((by, value)))
    
    def wait_for_element_visible(self, by, value, timeout=None):
        """Wait for an element to be visible"""
        if timeout is None:
            timeout = config.ELEMENT_TIMEOUT
        wait = WebDriverWait(self.driver, timeout)
        return wait.until(EC.visibility_of_element_located((by, value)))
    
    def navigate_to(self, path=''):
        """Navigate to a specific path"""
        url = f"{config.BASE_URL}{path}"
        self.driver.get(url)
        time.sleep(2)  # Allow page to load
    
    def login(self, email=None, password=None):
        """Perform login action"""
        email = email or config.TEST_EMAIL
        password = password or config.TEST_PASSWORD
        
        # Navigate to login page if not already there
        if '/login' not in self.driver.current_url:
            self.navigate_to('/login')
        
        # Wait for login form
        email_input = self.wait_for_element_visible(By.NAME, 'email')
        password_input = self.wait_for_element_visible(By.NAME, 'password')
        
        # Fill in credentials
        email_input.clear()
        email_input.send_keys(email)
        password_input.clear()
        password_input.send_keys(password)
        
        # Click login button
        login_button = self.wait_for_element_clickable(
            By.CSS_SELECTOR, 
            'button[type="submit"], .login-form-button, button.ant-btn-primary'
        )
        login_button.click()
        
        # Wait for navigation to dashboard
        time.sleep(3)
        self.wait_for_element(By.TAG_NAME, 'body')
