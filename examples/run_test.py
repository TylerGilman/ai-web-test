from ai_web_tester import TestRunner
import json

def main():
    runner = TestRunner()
    try:
        # Get test file path
        test_file = input("Enter path to test file (e.g., my_test.json): ")
        
        # Load and run test
        print(f"\nLoading test from {test_file}...")
        test_case = runner.load_test(test_file)
        
        print(f"\nRunning test: {test_case.name}")
        results = runner.run_test(test_case)
        
        # Display results
        print("\nTest Results:")
        print(f"Test Name: {results['name']}")
        print(f"Success: {results['success']}")
        
        if results['error']:
            print(f"Error: {results['error']}")
        
        print("\nStep Results:")
        for i, step in enumerate(results['steps'], 1):
            status = "✓" if step['success'] else "✗"
            action = step['action']
            print(f"{status} Step {i}: {action['action']} on {action['selector']}")
            if not step['success']:
                print(f"  Error: {step['error']}")
        
    finally:
        runner.cleanup()

if __name__ == "__main__":
    main()
