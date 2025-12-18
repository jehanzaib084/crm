"""
Main test runner script for Selenium tests
"""
import sys
import os
import subprocess
from datetime import datetime

def run_tests():
    """Run all Selenium tests and generate report"""
    
    print("=" * 70)
    print("SELENIUM AUTOMATED TESTING - IDURAR ERP CRM")
    print("=" * 70)
    print(f"Test Execution Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    # Test files to run
    test_files = [
        'test_homepage.py',
        'test_login.py',
        'test_api_integration.py',
        'test_navigation.py'
    ]
    
    # Run pytest with HTML report
    cmd = [
        'pytest',
        '-v',  # Verbose output
        '--tb=short',  # Short traceback format
        '--html=reports/test_report.html',  # HTML report
        '--self-contained-html',  # Self-contained HTML
        '--capture=no',  # Show print statements
    ] + test_files
    
    try:
        result = subprocess.run(cmd, cwd=os.path.dirname(__file__))
        
        print()
        print("=" * 70)
        print(f"Test Execution Completed: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("=" * 70)
        
        if result.returncode == 0:
            print("✓ All tests passed!")
        else:
            print("⚠ Some tests failed. Check the report for details.")
        
        print(f"\n📊 HTML Report: reports/test_report.html")
        print(f"📸 Screenshots: screenshots/")
        
        return result.returncode
        
    except FileNotFoundError:
        print("ERROR: pytest not found. Please install requirements:")
        print("  pip install -r requirements.txt")
        return 1
    except Exception as e:
        print(f"ERROR: {str(e)}")
        return 1

if __name__ == '__main__':
    sys.exit(run_tests())
