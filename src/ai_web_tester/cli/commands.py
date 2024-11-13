import click
from ai_web_tester import AIWebTester, TestCase
import json

@click.group()
def cli():
    """AI Web Testing Tool - Automated web testing with AI assistance"""
    pass

@cli.command()
@click.option('--url', prompt='Website URL', help='URL to test')
@click.option('--name', prompt='Test case name', help='Name for the test case')
def record(url, name):
    """Record a new test case by following your actions"""
    tester = AIWebTester()
    click.echo("Recording test case. Press 'q' to stop recording.")
    test_case = tester.record_test_case(url=url, name=name)
    filename = f"{name.lower().replace(' ', '_')}_test.json"
    tester.save_test_case(test_case, filename)
    click.echo(f"Test case saved as {filename}")
    tester.cleanup()

@cli.command()
@click.argument('filename')
def run(filename):
    """Run a saved test case"""
    tester = AIWebTester()
    test_case = tester.load_test_case(filename)
    result = tester.execute_test_case(test_case)
    
    click.echo("\nTest Results:")
    click.echo(f"Success: {result.success}")
    if not result.success:
        click.echo(f"Error: {result.error_message}")
    
    report_file = "test_report.json"
    tester.generate_test_report(report_file)
    click.echo(f"\nTest report generated as {report_file}")
    tester.cleanup()
