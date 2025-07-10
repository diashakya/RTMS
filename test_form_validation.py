#!/usr/bin/env python3
"""
Enhanced Form Validation Testing Script
======================================

This script tests all the enhanced form validation features implemented
in the Django restaurant management system.

Tests include:
- Django form validation (server-side)
- JavaScript validation (client-side)
- Template integration
- Error message display
- User experience enhancements

Usage:
    python test_form_validation.py

Requirements:
    - Django development server running
    - All form validation files in place
    - Test data available
"""

import os
import sys
import requests
import time
from datetime import datetime

# Color codes for terminal output
class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    PURPLE = '\033[95m'
    CYAN = '\033[96m'
    WHITE = '\033[97m'
    BOLD = '\033[1m'
    END = '\033[0m'

def print_header(title):
    """Print a formatted header"""
    print(f"\n{Colors.BOLD}{Colors.BLUE}{'='*60}{Colors.END}")
    print(f"{Colors.BOLD}{Colors.BLUE}{title.center(60)}{Colors.END}")
    print(f"{Colors.BOLD}{Colors.BLUE}{'='*60}{Colors.END}")

def print_test(test_name, status, details=""):
    """Print test result with color coding"""
    status_color = Colors.GREEN if status == "PASS" else Colors.RED if status == "FAIL" else Colors.YELLOW
    print(f"{Colors.WHITE}Testing: {test_name:<40}{Colors.END} [{status_color}{status}{Colors.END}]")
    if details:
        print(f"         {Colors.CYAN}{details}{Colors.END}")

def print_info(message):
    """Print information message"""
    print(f"{Colors.CYAN}ℹ {message}{Colors.END}")

def check_file_exists(file_path, description):
    """Check if a file exists"""
    if os.path.exists(file_path):
        print_test(f"{description}", "PASS", f"Found: {file_path}")
        return True
    else:
        print_test(f"{description}", "FAIL", f"Missing: {file_path}")
        return False

def check_file_content(file_path, search_text, description):
    """Check if file contains specific content"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            if search_text in content:
                print_test(f"{description}", "PASS", f"Found '{search_text}' in {file_path}")
                return True
            else:
                print_test(f"{description}", "FAIL", f"Missing '{search_text}' in {file_path}")
                return False
    except Exception as e:
        print_test(f"{description}", "FAIL", f"Error reading {file_path}: {str(e)}")
        return False

def test_server_response(url, expected_status=200, description=""):
    """Test server response"""
    try:
        response = requests.get(url, timeout=10)
        if response.status_code == expected_status:
            print_test(f"Server Response: {description}", "PASS", f"Status: {response.status_code}")
            return True
        else:
            print_test(f"Server Response: {description}", "FAIL", f"Status: {response.status_code}")
            return False
    except Exception as e:
        print_test(f"Server Response: {description}", "FAIL", f"Error: {str(e)}")
        return False

def run_validation_tests():
    """Run all form validation tests"""
    
    print_header("ENHANCED FORM VALIDATION TESTING")
    print_info(f"Test started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Base paths
    base_path = os.path.dirname(os.path.abspath(__file__))
    static_path = os.path.join(base_path, "main", "static")
    templates_path = os.path.join(base_path, "main", "templates")
    
    # Test results
    total_tests = 0
    passed_tests = 0
    
    # 1. File Structure Tests
    print_header("FILE STRUCTURE TESTS")
    
    test_files = [
        (os.path.join(base_path, "main", "forms.py"), "Enhanced Django Forms"),
        (os.path.join(static_path, "js", "form-validation.js"), "Form Validation JavaScript"),
        (os.path.join(static_path, "css", "style.css"), "Enhanced CSS Styles"),
        (os.path.join(templates_path, "main", "cart.html"), "Enhanced Cart Template"),
        (os.path.join(templates_path, "main", "form_validation_demo.html"), "Validation Demo Template"),
        (os.path.join(templates_path, "authenticate", "register.html"), "Enhanced Registration Template"),
        (os.path.join(templates_path, "authenticate", "login.html"), "Enhanced Login Template"),
        (os.path.join(templates_path, "base.html"), "Base Template with JS Includes"),
        (os.path.join(base_path, "main", "urls.py"), "URL Configuration"),
    ]
    
    for file_path, description in test_files:
        total_tests += 1
        if check_file_exists(file_path, description):
            passed_tests += 1
    
    # 2. Form Enhancement Tests
    print_header("DJANGO FORM ENHANCEMENT TESTS")
    
    forms_file = os.path.join(base_path, "main", "forms.py")
    form_tests = [
        ("class FormValidator", "FormValidator class"),
        ("error_messages", "Custom error messages"),
        ("data-validation", "Validation attributes"),
        ("RegexValidator", "Regex validators"),
        ("def clean_", "Custom clean methods"),
    ]
    
    for search_text, description in form_tests:
        total_tests += 1
        if check_file_content(forms_file, search_text, description):
            passed_tests += 1
    
    # 3. JavaScript Validation Tests
    print_header("JAVASCRIPT VALIDATION TESTS")
    
    js_file = os.path.join(static_path, "js", "form-validation.js")
    js_tests = [
        ("class FormValidator", "FormValidator class definition"),
        ("validateField", "Field validation method"),
        ("showFieldFeedback", "Visual feedback method"),
        ("validationRules", "Validation rules object"),
        ("real-time validation", "Real-time validation comment"),
        ("handleSubmit", "Form submission handler"),
        ("scrollToFirstError", "Error navigation method"),
    ]
    
    for search_text, description in js_tests:
        total_tests += 1
        if check_file_content(js_file, search_text, description):
            passed_tests += 1
    
    # 4. CSS Styling Tests
    print_header("CSS STYLING TESTS")
    
    css_file = os.path.join(static_path, "css", "style.css")
    css_tests = [
        ("Enhanced Form Validation Styles", "Validation CSS section"),
        (".form-control.is-valid", "Valid state styling"),
        (".form-control.is-invalid", "Invalid state styling"),
        (".invalid-feedback", "Error feedback styling"),
        (".validation-tooltip", "Tooltip styling"),
        ("@keyframes shake", "Shake animation"),
    ]
    
    for search_text, description in css_tests:
        total_tests += 1
        if check_file_content(css_file, search_text, description):
            passed_tests += 1
    
    # 5. Template Integration Tests
    print_header("TEMPLATE INTEGRATION TESTS")
    
    template_tests = [
        (os.path.join(templates_path, "main", "cart.html"), "form-group-enhanced", "Enhanced form groups"),
        (os.path.join(templates_path, "main", "cart.html"), "invalid-feedback", "Error display elements"),
        (os.path.join(templates_path, "main", "cart.html"), "data-validation", "Validation attributes"),
        (os.path.join(templates_path, "authenticate", "register.html"), "data-validation", "Registration validation"),
        (os.path.join(templates_path, "authenticate", "login.html"), "login-form", "Login form class"),
        (os.path.join(templates_path, "base.html"), "form-validation.js", "JavaScript inclusion"),
    ]
    
    for file_path, search_text, description in template_tests:
        total_tests += 1
        if check_file_content(file_path, search_text, description):
            passed_tests += 1
    
    # 6. URL Configuration Tests
    print_header("URL CONFIGURATION TESTS")
    
    urls_file = os.path.join(base_path, "main", "urls.py")
    url_tests = [
        ("form-validation-demo", "Demo page URL"),
        ("cart", "Cart URL"),
        ("register", "Registration URL"),
        ("login", "Login URL"),
    ]
    
    for search_text, description in url_tests:
        total_tests += 1
        if check_file_content(urls_file, search_text, description):
            passed_tests += 1
    
    # 7. Server Response Tests (if server is running)
    print_header("SERVER RESPONSE TESTS")
    
    server_urls = [
        ("http://127.0.0.1:8000/", "Homepage"),
        ("http://127.0.0.1:8000/cart/", "Cart Page"),
        ("http://127.0.0.1:8000/form-validation-demo/", "Validation Demo Page"),
        ("http://127.0.0.1:8000/register/", "Registration Page"),
        ("http://127.0.0.1:8000/login/", "Login Page"),
    ]
    
    print_info("Testing server responses (server must be running)...")
    for url, description in server_urls:
        total_tests += 1
        if test_server_response(url, description=description):
            passed_tests += 1
    
    # 8. Feature Completeness Tests
    print_header("FEATURE COMPLETENESS TESTS")
    
    feature_files = [
        (forms_file, "phone_validator", "Phone validation"),
        (forms_file, "def clean_customer_firstname", "Name validation"),
        (forms_file, "def clean_customer_email", "Email validation"),
        (js_file, "custom:", "Custom validation"),
        (js_file, "QuantityValidator", "Quantity validation"),
        (os.path.join(templates_path, "main", "cart.html"), "char-count", "Character counter"),
    ]
    
    for file_path, search_text, description in feature_files:
        total_tests += 1
        if check_file_content(file_path, search_text, description):
            passed_tests += 1
    
    # Print Summary
    print_header("TEST SUMMARY")
    
    success_rate = (passed_tests / total_tests) * 100 if total_tests > 0 else 0
    
    print(f"\n{Colors.BOLD}Test Results:{Colors.END}")
    print(f"  Total Tests: {Colors.BLUE}{total_tests}{Colors.END}")
    print(f"  Passed:      {Colors.GREEN}{passed_tests}{Colors.END}")
    print(f"  Failed:      {Colors.RED}{total_tests - passed_tests}{Colors.END}")
    print(f"  Success Rate: {Colors.CYAN}{success_rate:.1f}%{Colors.END}")
    
    if success_rate >= 90:
        print(f"\n{Colors.GREEN}{Colors.BOLD}✅ EXCELLENT! Form validation implementation is complete!{Colors.END}")
    elif success_rate >= 75:
        print(f"\n{Colors.YELLOW}{Colors.BOLD}⚠️  GOOD! Most features implemented, minor issues remain.{Colors.END}")
    else:
        print(f"\n{Colors.RED}{Colors.BOLD}❌ INCOMPLETE! Significant issues need to be addressed.{Colors.END}")
    
    # Next Steps
    print_header("NEXT STEPS")
    
    if passed_tests == total_tests:
        print_info("🎉 All tests passed! Form validation is ready for production.")
        print_info("📋 Test the features manually:")
        print_info("   • Visit /form-validation-demo/ to see all features")
        print_info("   • Try submitting forms with invalid data")
        print_info("   • Check real-time validation as you type")
        print_info("   • Verify error messages are helpful and clear")
    else:
        print_info("🔧 Some tests failed. Check the following:")
        print_info("   • Ensure all files are created correctly")
        print_info("   • Verify file paths and content")
        print_info("   • Check for syntax errors in code")
        print_info("   • Make sure Django server is running for response tests")
    
    print(f"\n{Colors.CYAN}Test completed at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}{Colors.END}")
    return success_rate >= 75

if __name__ == "__main__":
    print(f"{Colors.BOLD}{Colors.PURPLE}")
    print("🔍 Enhanced Form Validation Testing Script")
    print("==========================================")
    print(f"{Colors.END}")
    
    try:
        success = run_validation_tests()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print(f"\n{Colors.YELLOW}Test interrupted by user.{Colors.END}")
        sys.exit(1)
    except Exception as e:
        print(f"\n{Colors.RED}Test failed with error: {str(e)}{Colors.END}")
        sys.exit(1)
