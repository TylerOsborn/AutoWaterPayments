#!/usr/bin/env python3
"""
Auto Water Purchase Script
Automates monthly water payment via Standard Bank online banking
and sends SMS notification.
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
from webdriver_manager.chrome import ChromeDriverManager

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
        self.phone_user = os.getenv('PHONE_NUMBER_USER')
        self.phone_enbaya = os.getenv('PHONE_NUMBER_ENBAYA')
        self.driver = None
        
        if not all([self.username, self.password, self.phone_user, self.phone_enbaya]):
            raise ValueError("Missing required environment variables")
    
    def setup_driver(self):
        """Initialize Chrome WebDriver with appropriate options"""
        chrome_options = Options()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument('--window-size=1920,1080')
        
        service = Service(ChromeDriverManager().install())
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
            
            # Input username
            username_field = self.wait.until(
                EC.presence_of_element_located((By.NAME, "username"))
            )
            username_field.clear()
            username_field.send_keys(self.username)
            logging.info("Entered username")
            
            # Input password
            password_field = self.driver.find_element(By.NAME, "password")
            password_field.clear()
            password_field.send_keys(self.password)
            logging.info("Entered password")
            
            # Click login/submit button
            login_button = self.driver.find_element(By.XPATH, "//button[@type='submit']")
            login_button.click()
            logging.info("Clicked login button")
            
            # Wait for login to complete
            time.sleep(5)
            logging.info("Login completed successfully")
            
        except Exception as e:
            logging.error(f"Error during login: {str(e)}")
            raise
    
    def navigate_to_pay_section(self):
        """Navigate to the PAY section"""
        try:
            logging.info("Navigating to PAY section")
            
            # Click the PAY button
            pay_button = self.wait.until(
                EC.element_to_be_clickable((By.ID, "Transact-Pay"))
            )
            pay_button.click()
            logging.info("Clicked PAY button")
            
            # Click Beneficiary dropdown
            beneficiary_dropdown = self.wait.until(
                EC.element_to_be_clickable((By.XPATH, "//a[contains(text(), 'Beneficiary') or contains(text(), 'BENEFICIARY')]"))
            )
            beneficiary_dropdown.click()
            logging.info("Clicked Beneficiary dropdown")
            
        except Exception as e:
            logging.error(f"Error navigating to pay section: {str(e)}")
            raise
    
    def search_and_pay_beneficiary(self):
        """Search for enbaya beneficiary and initiate payment"""
        try:
            logging.info("Searching for enbaya beneficiary")
            
            # Find and use the search input field
            search_field = self.wait.until(
                EC.presence_of_element_located((By.ID, "filter"))
            )
            search_field.clear()
            search_field.send_keys("enbaya")
            logging.info("Entered 'enbaya' in search field")
            
            # Wait for search results and click pay button
            time.sleep(2)
            pay_link = self.wait.until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "a.action.pay"))
            )
            pay_link.click()
            logging.info("Clicked pay button for enbaya beneficiary")
            
        except Exception as e:
            logging.error(f"Error searching for beneficiary: {str(e)}")
            raise
    
    def enter_payment_amount(self):
        """Enter R500 payment amount"""
        try:
            logging.info("Entering payment amount")
            
            # Find amount input field and enter 500
            amount_field = self.wait.until(
                EC.presence_of_element_located((By.ID, "amount"))
            )
            amount_field.clear()
            amount_field.send_keys("500")
            logging.info("Entered R500 as payment amount")
            
            # Click Next button
            next_button = self.wait.until(
                EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Next')]"))
            )
            next_button.click()
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
            confirm_button.click()
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
    
    # Check if it's the first day of the month at 00:01
    now = datetime.now()
    if now.day != 1 or now.hour != 0 or now.minute != 1:
        logging.info(f"Not scheduled time. Current: {now}. Exiting.")
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
        
        # TODO: Implement SMS functionality
        
    except Exception as e:
        logging.error(f"Error occurred: {str(e)}")
    finally:
        app.cleanup()
        logging.info("Script completed")

if __name__ == "__main__":
    main()