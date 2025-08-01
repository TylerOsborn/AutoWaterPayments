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
        
        # TODO: Implement banking automation
        # TODO: Implement SMS functionality
        
    except Exception as e:
        logging.error(f"Error occurred: {str(e)}")
    finally:
        app.cleanup()
        logging.info("Script completed")

if __name__ == "__main__":
    main()