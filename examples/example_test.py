from ai_web_tester import AIWebTester
import os

def main():
    tester = AIWebTester()
    try:
        # 1. Record a test
        print("Recording test...")
        test_case = tester.start_recording(
            url="https://www.example.com",
            name="Example Test"
        )
        
        # 2. Save the test
        os.makedirs('tests/recorded', exist_ok=True)
        test_file = 'tests/recorded/example_test.json'
        tester.save_test(test_case, test_file)
        
        # 3. Load and run the test
        print("\nRunning saved test...")
        loaded_test = tester.load_test(test_file)
        results = tester.run_test(loaded_test)
        
        # 4. Display results
        print("\nTest Results:")
        print(f"Test Name: {results['name']}")
        print(f"Success: {results['success']}")
        if not results['success']:
            print(f"Error: {results.get('error', 'Unknown error')}")
        
        print("\nAction Results:")
        for action in results['actions']:
            status = "✓" if action['success'] else "✗"
            print(f"{status} {action['action_type']}: {action['selector']}")
            if not action['success']:
                print(f"  Error: {action['error']}")
        
    finally:
        tester.cleanup()

if __name__ == "__main__":
    main()
