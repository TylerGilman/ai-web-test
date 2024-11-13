from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time
import json
import os
from .models import TestAction, TestStep

class TestLearner:
    def __init__(self):
        self.driver = None
        self.current_session = []
        self.successful_paths = []
        self.failure_paths = []
        self.base_url = None
        self.debug = True  # Enable debug mode

    def _setup_driver(self):
        """Initialize webdriver with debugging"""
        options = webdriver.ChromeOptions()
        options.add_argument('--no-sandbox')
        # Enable browser logging
        options.set_capability('goog:loggingPrefs', {'browser': 'ALL'})
        
        service = Service(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=service, options=options)
        print("WebDriver initialized successfully")
        
    def _inject_visual_feedback(self):
        """Inject CSS for visual feedback"""
        css = """
        .ai-test-highlight {
            outline: 2px solid red !important;
            transition: outline 0.3s ease-in-out;
        }
        #ai-test-logger {
            position: fixed;
            bottom: 10px;
            right: 10px;
            background: rgba(0, 0, 0, 0.8);
            color: white;
            padding: 10px;
            border-radius: 5px;
            font-family: monospace;
            z-index: 10000;
            max-height: 200px;
            overflow-y: auto;
        }
        """
        self.driver.execute_script(f"""
            let style = document.createElement('style');
            style.textContent = `{css}`;
            document.head.appendChild(style);
            
            let logger = document.createElement('div');
            logger.id = 'ai-test-logger';
            document.body.appendChild(logger);
        """)

    def _setup_event_listeners(self):
        """Set up JavaScript event listeners with visual feedback"""
        js_code = """
        window.recordedActions = [];
        
        function logAction(message) {
            let logger = document.getElementById('ai-test-logger');
            if (logger) {
                let entry = document.createElement('div');
                entry.textContent = message;
                logger.appendChild(entry);
                logger.scrollTop = logger.scrollHeight;
                
                // Keep only last 10 messages
                while (logger.children.length > 10) {
                    logger.removeChild(logger.firstChild);
                }
            }
            console.log(message);
        }

        function highlightElement(element) {
            element.classList.add('ai-test-highlight');
            setTimeout(() => {
                element.classList.remove('ai-test-highlight');
            }, 500);
        }
        
        function recordAction(event) {
            if (!event.target || event.target.id === 'ai-test-logger') return;
            
            let element = event.target;
            highlightElement(element);
            
            let action = {
                timestamp: Date.now(),
                type: event.type,
                tagName: element.tagName.toLowerCase(),
                id: element.id,
                className: element.className,
                value: element.value || element.textContent,
                href: element.href,
                xpath: getXPath(element)
            };
            
            window.recordedActions.push(action);
            logAction(`Recorded ${event.type} on ${element.tagName.toLowerCase()}`);
        }

        function getXPath(element) {
            if (element.id)
                return `//*[@id="${element.id}"]`;
                
            function getElementIndex(element) {
                let index = 1;
                let sibling = element.previousSibling;
                while (sibling) {
                    if (sibling.nodeType === 1 && sibling.tagName === element.tagName) {
                        index++;
                    }
                    sibling = sibling.previousSibling;
                }
                return index;
            }
            
            let paths = [];
            while (element && element.nodeType === 1) {
                let tag = element.tagName.toLowerCase();
                let index = getElementIndex(element);
                paths.unshift(`${tag}[${index}]`);
                element = element.parentNode;
            }
            return '/' + paths.join('/');
        }

        // Remove existing listeners
        document.removeEventListener('click', recordAction, true);
        document.removeEventListener('input', recordAction, true);
        document.removeEventListener('change', recordAction, true);
        
        // Add new listeners
        document.addEventListener('click', recordAction, true);
        document.addEventListener('input', recordAction, true);
        document.addEventListener('change', recordAction, true);
        
        logAction('Event listeners initialized');
        """
        
        self.driver.execute_script(js_code)
        print("Event listeners set up successfully")

    def start_learning_session(self, url: str):
        """Start a new learning session with debugging"""
        if not self.driver:
            self._setup_driver()
        
        try:
            print(f"\nNavigating to {url}")
            self.base_url = url
            self.driver.get(url)
            time.sleep(2)  # Wait for page load
            
            print("Injecting visual feedback...")
            self._inject_visual_feedback()
            
            print("Setting up event listeners...")
            self._setup_event_listeners()
            
            self.current_session = []
            
            print("\nRecording started!")
            print("You should see:")
            print("- Red highlight when clicking elements")
            print("- Action log in bottom-right corner")
            print("- Console messages for each action")
            return True
            
        except Exception as e:
            print(f"Error starting session: {e}")
            if self.debug:
                print("\nBrowser logs:")
                for entry in self.driver.get_log('browser'):
                    print(entry)
            return False

    def _get_recorded_actions(self):
        """Retrieve actions with debugging"""
        try:
            actions = self.driver.execute_script("return window.recordedActions || [];")
            if actions:
                print(f"\nRetrieved {len(actions)} actions:")
                for action in actions:
                    print(f"- {action['type']} on {action['tagName']} ({action['xpath']})")
            return actions
        except Exception as e:
            print(f"Error retrieving actions: {e}")
            if self.debug:
                print("\nBrowser logs:")
                for entry in self.driver.get_log('browser'):
                    print(entry)
            return []

    def mark_current_path(self, success: bool):
        """Mark the current session as success or failure"""
        actions = self._get_recorded_actions()
        
        if not actions:
            print("No actions to mark!")
            return

        test_actions = []
        for action in actions:
            test_action = TestAction(
                element_type=action.get('tagName', 'unknown'),
                selector=action.get('xpath', ''),
                action=action.get('type', 'unknown'),
                value=action.get('value', None),
                timestamp=action.get('timestamp', None)
            )
            test_actions.append(test_action)
        
        self.current_session = test_actions
        
        path = {
            'url': self.base_url,
            'actions': [action.to_dict() for action in test_actions]
        }
        
        if success:
            self.successful_paths.append(path)
            print(f"Marked path with {len(test_actions)} actions as successful")
        else:
            self.failure_paths.append(path)
            print(f"Marked path with {len(test_actions)} actions as failure")
        
        # Clear recorded actions
        self.driver.execute_script("window.recordedActions = [];")

    def save_learned_test(self, name: str, filepath: str):
        """Save the current session as a test case"""
        actions = self._get_recorded_actions()
        
        if not actions and not self.current_session:
            print("No actions to save!")
            return
        
        if actions:
            test_actions = []
            for action in actions:
                test_action = TestAction(
                    element_type=action.get('tagName', 'unknown'),
                    selector=action.get('xpath', ''),
                    action=action.get('type', 'unknown'),
                    value=action.get('value', None),
                    timestamp=action.get('timestamp', None)
                )
                test_actions.append(test_action)
            
            self.current_session.extend(test_actions)
        
        test_case = {
            'name': name,
            'url': self.base_url,
            'steps': [
                {
                    'action': action.to_dict(),
                    'expected_state': {}
                } for action in self.current_session
            ],
            'successful_paths': self.successful_paths,
            'failure_paths': self.failure_paths
        }
        
        # Create directory if it doesn't exist
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        
        with open(filepath, 'w') as f:
            json.dump(test_case, f, indent=2)
        print(f"Test saved to: {filepath}")
        print(f"Recorded {len(self.current_session)} actions")
        
        # Clear recorded actions
        self.driver.execute_script("window.recordedActions = [];")
        return test_case

    def cleanup(self):
        """Clean up resources"""
        if self.driver:
            self.driver.quit()
