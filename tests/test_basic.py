import unittest
from selenium.webdriver.common.by import By
from ai_web_tester import AIWebTester, TestCase, TestStep

class TestAIWebTester(unittest.TestCase):
    def setUp(self):
        self.tester = AIWebTester()
    
    def tearDown(self):
        self.tester.cleanup()
    
    def test_basic_navigation(self):
        """Test basic navigation to a website"""
        test_case = TestCase(
            name="Basic Navigation",
            description="Test navigation to a website",
            preconditions=["Navigate to https://example.com"],
            steps=[
                TestStep(
                    action_type="verify",
                    selector="//h1",
                    expected_result="Example Domain"
                )
            ],
            expected_outcome="Page loads successfully"
        )
        
        result = self.tester.execute_test_case(test_case)
        self.assertTrue(result.success)
