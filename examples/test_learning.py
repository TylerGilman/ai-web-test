from ai_web_tester import TestLearner
import os

def main():
    learner = TestLearner()
    try:
        # Start learning session
        url = input("Enter website URL to test: ")
        learner.start_learning_session(url)
        
        print("\nLearning session started. Browser will open.")
        print("Interact with the website normally.")
        print("\nAvailable commands:")
        print("- success: Mark current path as successful")
        print("- failure: Mark current path as failed")
        print("- reset: Start new path")
        print("- save: Save current session as test")
        print("- done: End session")
        
        while True:
            command = input("\nEnter command: ").lower()
            
            if command == 'success':
                learner.mark_current_path(success=True)
            elif command == 'failure':
                learner.mark_current_path(success=False)
            elif command == 'reset':
                new_url = input("Enter URL (or press enter for current): ").strip()
                url = new_url if new_url else url
                learner.start_learning_session(url)
            elif command == 'save':
                name = input("Enter test name: ")
                # Create tests directory if it doesn't exist
                os.makedirs('tests', exist_ok=True)
                filepath = f"tests/{name.lower().replace(' ', '_')}.json"
                learner.save_learned_test(name, filepath)
            elif command == 'done':
                # Save before exiting
                save = input("Save test before exiting? (y/n): ").lower()
                if save == 'y':
                    name = input("Enter test name: ")
                    os.makedirs('tests', exist_ok=True)
                    filepath = f"tests/{name.lower().replace(' ', '_')}.json"
                    learner.save_learned_test(name, filepath)
                break
            elif command == 'help':
                print("\nAvailable commands:")
                print("- success: Mark current path as successful")
                print("- failure: Mark current path as failed")
                print("- reset: Start new path")
                print("- save: Save current session as test")
                print("- done: End session")
        
        print("\nLearning session completed!")
        
    finally:
        learner.cleanup()

if __name__ == "__main__":
    main()
