# AI Web Tester

An AI-powered web testing automation tool that learns from your actions and creates reproducible test cases.

## Installation

```bash
pip install ai-web-tester
```

## Quick Start

1. Record a new test case:
```bash
ai-web-test record --url https://example.com --name login_test
```

2. Run a saved test case:
```bash
ai-web-test run login_test.json
```

## Features

- AI-powered test recording and execution
- Automatic error detection and reporting
- Reproducible test cases
- Command-line interface
- Detailed test reports
- Screenshot capture on failures

## Example Usage

```python
from ai_web_tester import AIWebTester, TestCase, TestStep

# Initialize tester
tester = AIWebTester()

# Record a test case
test_case = tester.record_test_case(
    url="https://example.com",
    name="Login Test"
)

# Save the test case
tester.save_test_case(test_case, "login_test.json")

# Run the test case
result = tester.execute_test_case(test_case)

# Generate report
tester.generate_test_report("test_report.json")

# Cleanup
tester.cleanup()
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.
