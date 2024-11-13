from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time

from .models import TestAction, TestCase

class AIWebTester:
    def __init__(self):
        self.driver = None
    
    def initialize_driver(self):
        options = webdriver.ChromeOptions()
        options.add_argument('--no-sandbox')
        service = Service(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=service, options=options)
        return self.driver
    
    def cleanup(self):
        if self.driver:
            self.driver.quit()
