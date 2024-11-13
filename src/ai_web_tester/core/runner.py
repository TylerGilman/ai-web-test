from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time
import json
from .models import TestCase, TestStep, TestAction

class TestRunner:
    def __init__(self):
        self.driver = None
    
    def _setup_driver(self):
        options = webdriver.ChromeOptions()
        options.add_argument('--no-sandbox')
        service = Service(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=service, options=options)
    
    def load_test(self, filepath: str) -> TestCase:
        """Load a test case from file"""
        with open(filepath, 'r') as f:
            data = json.load(f)
            steps = [
                TestStep(
                    action=TestAction(**step_data['action']),
                    expected_state=step_data['expected_state']
                )
                for step_data in data['steps']
            ]
            
            # Handle the case where 'expected_outcomes' is not present
            expected_outcomes = data.get('expected_outcomes', [])
            
            return TestCase(
                name=data['name'],
                url=data['url'],
                steps=steps,
                expected_outcomes=expected_outcomes)
    
    def run_test(self, test_case: TestCase) -> dict:
        """Run a saved test case"""
        if not self.driver:
            self._setup_driver()
        
        results = {
            'name': test_case.name,
            'url': test_case.url,
            'steps': [],
            'success': True,
            'error': None
        }
        
        try:
            print(f"Navigating to {test_case.url}")
            self.driver.get(test_case.url)
            
            for i, step in enumerate(test_case.steps, 1):
                print(f"\nExecuting step {i}: {step.action.action} on {step.action.selector}")
                step_result = self._execute_step(step)
                results['steps'].append(step_result)
                
                if not step_result['success']:
                    results['success'] = False
                    results['error'] = step_result['error']
                    print(f"Step {i} failed: {step_result['error']}")
                    break
                print(f"Step {i} completed successfully")
                    
        except Exception as e:
            results['success'] = False
            results['error'] = str(e)
            print(f"Test failed: {str(e)}")
        
        return results
    
    def _execute_step(self, step: TestStep) -> dict:
        """Execute a single test step"""
        result = {
            'action': step.action.to_dict(),
            'success': True,
            'error': None
        }

        num_retries = 3  # Number of retries
        retry_delay = 5  # Delay between retries (in seconds)

        for attempt in range(1, num_retries + 1):
            try:
                # Wait for the element to be present
                element = WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, step.action.selector))
                )

                # Wait for the element to be visible
                element = WebDriverWait(self.driver, 10).until(
                    EC.visibility_of_element_located((By.CSS_SELECTOR, step.action.selector))
                )

                if step.action.action == "click":
                    element.click()
                elif step.action.action == "input":
                    element.clear()
                    element.send_keys(step.action.value)

                time.sleep(0.5)  # Small wait for state to settle
                break  # Exit the loop if the step executed successfully
            except Exception as e:
                if attempt == num_retries:
                    result['success'] = False
                    result['error'] = str(e)
                else:
                    print(f"Attempt {attempt}/{num_retries} failed, retrying in {retry_delay} seconds...")
                    time.sleep(retry_delay)

        return result
    
    def cleanup(self):
        if self.driver:
            self.driver.quit()
