#!/usr/bin/env python3
"""
Auto Water Purchase Script
Automates monthly water payment via Standard Bank online banking.
"""

import os
import time
import logging
from datetime import datetime
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.core.os_manager import ChromeType

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('auto_water_purchase.log'),
        logging.StreamHandler()
    ]
)

class AutoWaterPurchase:
    def __init__(self):
        self.username = os.getenv('STANDARD_BANK_USERNAME')
        self.password = os.getenv('STANDARD_BANK_PASSWORD')
        self.payment_amount = os.getenv('PAYMENT_AMOUNT', '1')  # Default to R1 if not set
        self.driver = None
        
        required_vars = [self.username, self.password]
        if not all(required_vars):
            raise ValueError("Missing required environment variables")
    
    def setup_driver(self):
        """Initialize Chrome WebDriver with appropriate options"""
        chrome_options = Options()
        # chrome_options.add_argument('--headless')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument('--window-size=1920,1080')
        
        # Use chromium-browser binary explicitly
        chrome_options.binary_location = '/usr/bin/chromium-browser'
        
        # Use system chromedriver or download compatible one
        try:
            service = Service('/usr/bin/chromedriver')
        except:
            service = Service(ChromeDriverManager(chrome_type=ChromeType.CHROMIUM).install())
        
        self.driver = webdriver.Chrome(service=service, options=chrome_options)
        self.wait = WebDriverWait(self.driver, 30)
        
    def login_to_standard_bank(self):
        """Navigate to Standard Bank and perform login"""
        try:
            logging.info("Navigating to Standard Bank login page")
            self.driver.get("https://onlinebanking.standardbank.co.za/#/landing-page")
            
            # Click sign in button
            sign_in_button = self.wait.until(
                EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Sign in') or contains(text(), 'SIGN IN')]"))
            )
            sign_in_button.click()
            logging.info("Clicked sign in button")
            
            # Input username - wait for element to be present and enabled
            try:
                username_field = self.wait.until(
                    EC.presence_of_element_located((By.NAME, "pf.username"))
                )
                logging.info("Found username field")
                # Wait a bit more for the field to be ready
                time.sleep(2)
                self.wait.until(EC.element_to_be_clickable((By.NAME, "pf.username")))
                logging.info("Username field is clickable")
                
                # Try clicking first, then clearing, then entering text
                username_field.click()
                time.sleep(0.5)  # Brief pause after click
                
                # Use JavaScript to clear and set value as fallback
                try:
                    username_field.clear()
                    logging.info("Cleared username field")
                except:
                    logging.info("Using JavaScript to clear username field")
                    self.driver.execute_script("arguments[0].value = '';", username_field)
                
                # Try send_keys first, then JavaScript as fallback
                try:
                    username_field.send_keys(self.username)
                    logging.info("Entered username using send_keys")
                except:
                    logging.info("Using JavaScript to enter username")
                    self.driver.execute_script("arguments[0].value = arguments[1];", username_field, self.username)
                    logging.info("Entered username using JavaScript")
            except Exception as e:
                logging.error(f"Error with username field: {str(e)}")
                raise
            
            # Input password - wait for element to be present and enabled
            try:
                password_field = self.wait.until(
                    EC.presence_of_element_located((By.NAME, "pf.pass"))
                )
                logging.info("Found password field")
                # Wait a bit more for the field to be ready
                time.sleep(1)
                self.wait.until(EC.element_to_be_clickable((By.NAME, "pf.pass")))
                logging.info("Password field is clickable")
                
                # Try clicking first, then clearing, then entering text
                password_field.click()
                time.sleep(0.5)  # Brief pause after click
                
                # Use JavaScript to clear and set value as fallback
                try:
                    password_field.clear()
                    logging.info("Cleared password field")
                except:
                    logging.info("Using JavaScript to clear password field")
                    self.driver.execute_script("arguments[0].value = '';", password_field)
                
                # Try send_keys first, then JavaScript as fallback
                try:
                    password_field.send_keys(self.password)
                    logging.info("Entered password using send_keys")
                except:
                    logging.info("Using JavaScript to enter password")
                    self.driver.execute_script("arguments[0].value = arguments[1];", password_field, self.password)
                    logging.info("Entered password using JavaScript")
            except Exception as e:
                logging.error(f"Error with password field: {str(e)}")
                raise
            
            # Click login/submit button - wait for it to be clickable
            login_button = self.wait.until(
                EC.element_to_be_clickable((By.ID, "signon"))
            )
            login_button.click()
            logging.info("Clicked login button")
            
            # Wait for login to complete
            time.sleep(5)
            logging.info("Login completed successfully")
            
        except Exception as e:
            logging.error(f"Error during login: {str(e)}")
            raise
    
    def navigate_to_pay_section(self):
        """Navigate directly to the beneficiaries list"""
        try:
            logging.info("Navigating directly to beneficiaries list")
            
            # Navigate directly to the beneficiaries list URL
            self.driver.get("https://onlinebanking.standardbank.co.za/#/beneficiaries/list")
            logging.info("Navigated to beneficiaries list page")
            
            # Wait for page to load
            time.sleep(3)
            
        except Exception as e:
            logging.error(f"Error navigating to beneficiaries list: {str(e)}")
            raise
    
    def search_and_pay_beneficiary(self):
        """Search for enbaya beneficiary and initiate payment"""
        try:
            logging.info("Searching for enbaya beneficiary")
            
            # Find and use the search input field
            search_field = self.wait.until(
                EC.presence_of_element_located((By.ID, "filter"))
            )
            search_field.click()
            search_field.clear()
            search_field.click()
            search_field.send_keys("enbaya")
            logging.info("Entered 'enbaya' in search field")
            
            # Wait for search results and click pay button
            time.sleep(2)
            pay_link = self.wait.until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "a.action.pay"))
            )
            actions = ActionChains(self.driver)
            actions.move_to_element(pay_link).pause(2).click().perform()
            logging.info("Clicked pay button for enbaya beneficiary")
            
        except Exception as e:
            logging.error(f"Error searching for beneficiary: {str(e)}")
            raise
    
    def enter_payment_amount(self):
        """Enter payment amount"""
        try:
            logging.info("Entering payment amount")
            
            # Find amount input field and enter payment amount
            amount_field = self.wait.until(
                EC.presence_of_element_located((By.ID, "amount"))
            )

            actions = ActionChains(self.driver)
            actions.scroll_by_amount(0, 2000).pause(2) \
                .move_to_element(amount_field) \
                .pause(2) \
                .click() \
                .send_keys(self.payment_amount) \
                .perform()
            logging.info(f"Entered {self.payment_amount} as payment amount")
            
            # Click Next button
            next_button = self.wait.until(
                EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Next')]"))
            )
            actions = ActionChains(self.driver)
            actions.move_to_element(next_button).pause(2).click().perform()
            logging.info("Clicked Next button")
            
        except Exception as e:
            logging.error(f"Error entering payment amount: {str(e)}")
            raise
    
    def confirm_payment(self):
        """Confirm the payment"""
        try:
            logging.info("Confirming payment")
            
            # Wait for confirmation page to load
            time.sleep(3)
            
            # Click Confirm button
            confirm_button = self.wait.until(
                EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Confirm')]"))
            )

            actions = ActionChains(self.driver)
            actions.move_to_element(confirm_button).pause(2).click().perform()
            logging.info("Clicked Confirm button")
            
            # Wait for payment to process
            time.sleep(5)
            logging.info("Payment confirmation completed")
            
        except Exception as e:
            logging.error(f"Error confirming payment: {str(e)}")
            raise
    
    def take_screenshot(self):
        """Take a screenshot of the payment confirmation page"""
        try:
            logging.info("Taking screenshot of payment confirmation")
            
            # Generate timestamp for unique filename
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            screenshot_filename = f"payment_confirmation_{timestamp}.png"
            
            # Take screenshot
            screenshot_saved = self.driver.save_screenshot(screenshot_filename)
            
            if screenshot_saved:
                logging.info(f"Screenshot saved as {screenshot_filename}")
                return screenshot_filename
            else:
                logging.error("Failed to save screenshot")
                return None
                
        except Exception as e:
            logging.error(f"Error taking screenshot: {str(e)}")
            return None
    
    def cleanup(self):
        """Clean up resources"""
        if self.driver:
            self.driver.quit()

def main():
    """Main execution function"""
    logging.info("Starting Auto Water Purchase script")
    
    # Check if it's the first day of the month at 00:01 (or allow override for testing)
    now = datetime.now()
    force_run = os.getenv('FORCE_RUN', 'false').lower() == 'true'
    
    if not force_run and (now.day != 1 or now.hour != 0 or now.minute != 1):
        logging.info(f"Not scheduled time. Current: {now}. Exiting.")
        logging.info("Set FORCE_RUN=true environment variable to override timing check")
        return
    
    app = AutoWaterPurchase()
    try:
        app.setup_driver()
        logging.info("WebDriver initialized successfully")
        
        # Step 1: Login to Standard Bank
        app.login_to_standard_bank()
        
        # Step 2: Navigate to PAY section
        app.navigate_to_pay_section()
        
        # Step 3: Search and select beneficiary
        app.search_and_pay_beneficiary()
        
        # Step 4: Enter payment amount
        app.enter_payment_amount()
        
        # Step 5: Confirm payment
        app.confirm_payment()
        
        # Step 6: Take screenshot
        screenshot_file = app.take_screenshot()
        
        # Step 7: Save screenshot
        if screenshot_file:
            logging.info(f"Payment confirmation screenshot saved: {screenshot_file}")
        else:
            logging.warning("No screenshot taken due to an error")
        
        
        logging.info("Auto water purchase process completed successfully")
        
    except Exception as e:
        logging.error(f"Error occurred: {str(e)}")
    finally:
        app.cleanup()
        logging.info("Script completed")

if __name__ == "__main__":
    main()