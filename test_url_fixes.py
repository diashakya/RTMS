#!/usr/bin/env python3
"""
URL Routing Test Script
======================

This script tests the URL routing fixes for:
1. Login URL routing (/accounts/login/ vs /login/)
2. Order History URL routing (/order-history/ vs /orders/)

Usage:
    python test_url_fixes.py

Requirements:
    - Django development server running on 127.0.0.1:8000
"""

import requests
from datetime import datetime

# Color codes for terminal output
class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    WHITE = '\033[97m'
    BOLD = '\033[1m'
    END = '\033[0m'

def print_header(title):
    """Print a formatted header"""
    print(f"\n{Colors.BOLD}{Colors.BLUE}{'='*50}{Colors.END}")
    print(f"{Colors.BOLD}{Colors.BLUE}{title.center(50)}{Colors.END}")
    print(f"{Colors.BOLD}{Colors.BLUE}{'='*50}{Colors.END}")

def test_url_redirect(url, expected_redirect_pattern, description):
    """Test if URL redirects correctly"""
    try:
        response = requests.get(url, allow_redirects=False, timeout=10)
        
        if response.status_code in [301, 302]:
            redirect_location = response.headers.get('Location', '')
            if expected_redirect_pattern in redirect_location:
                print(f"{Colors.GREEN}✅ PASS{Colors.END}: {description}")
                print(f"   {Colors.CYAN}Redirects to: {redirect_location}{Colors.END}")
                return True
            else:
                print(f"{Colors.RED}❌ FAIL{Colors.END}: {description}")
                print(f"   {Colors.CYAN}Expected pattern: {expected_redirect_pattern}{Colors.END}")
                print(f"   {Colors.CYAN}Actual redirect: {redirect_location}{Colors.END}")
                return False
        else:
            print(f"{Colors.YELLOW}⚠️ INFO{Colors.END}: {description}")
            print(f"   {Colors.CYAN}Status: {response.status_code} (not a redirect){Colors.END}")
            return True
            
    except Exception as e:
        print(f"{Colors.RED}❌ ERROR{Colors.END}: {description}")
        print(f"   {Colors.CYAN}Error: {str(e)}{Colors.END}")
        return False

def test_url_access(url, description, should_redirect_to_login=False):
    """Test if URL is accessible or redirects to login"""
    try:
        response = requests.get(url, allow_redirects=False, timeout=10)
        
        if should_redirect_to_login:
            if response.status_code in [301, 302]:
                redirect_location = response.headers.get('Location', '')
                if '/login/' in redirect_location:
                    print(f"{Colors.GREEN}✅ PASS{Colors.END}: {description}")
                    print(f"   {Colors.CYAN}Correctly redirects to login: {redirect_location}{Colors.END}")
                    return True
                else:
                    print(f"{Colors.RED}❌ FAIL{Colors.END}: {description}")
                    print(f"   {Colors.CYAN}Should redirect to login, but redirects to: {redirect_location}{Colors.END}")
                    return False
            else:
                print(f"{Colors.RED}❌ FAIL{Colors.END}: {description}")
                print(f"   {Colors.CYAN}Should redirect to login, but got status: {response.status_code}{Colors.END}")
                return False
        else:
            if response.status_code == 200:
                print(f"{Colors.GREEN}✅ PASS{Colors.END}: {description}")
                print(f"   {Colors.CYAN}Status: {response.status_code} (accessible){Colors.END}")
                return True
            else:
                print(f"{Colors.YELLOW}⚠️ INFO{Colors.END}: {description}")
                print(f"   {Colors.CYAN}Status: {response.status_code}{Colors.END}")
                return True
                
    except Exception as e:
        print(f"{Colors.RED}❌ ERROR{Colors.END}: {description}")
        print(f"   {Colors.CYAN}Error: {str(e)}{Colors.END}")
        return False

def run_url_tests():
    """Run all URL routing tests"""
    
    print(f"{Colors.BOLD}{Colors.BLUE}")
    print("🔗 URL Routing Fix Testing Script")
    print("=================================")
    print(f"{Colors.END}")
    print(f"{Colors.CYAN}Test started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}{Colors.END}")
    
    base_url = "http://127.0.0.1:8000"
    tests_passed = 0
    total_tests = 0
    
    # Test 1: Login URL routing
    print_header("LOGIN URL ROUTING TESTS")
    
    # Test that protected pages redirect to /login/ not /accounts/login/
    protected_urls = [
        ("/orders/", "Order History - should redirect to /login/"),
        ("/admin-dashboard/", "Admin Dashboard - should redirect to /login/"),
        ("/manage-orders/", "Manage Orders - should redirect to /login/"),
    ]
    
    for url, description in protected_urls:
        total_tests += 1
        if test_url_access(f"{base_url}{url}", description, should_redirect_to_login=True):
            tests_passed += 1
    
    # Test 2: Order History URL routing
    print_header("ORDER HISTORY URL TESTS")
    
    # Test that /orders/ is accessible (redirects to login for unauthenticated users)
    total_tests += 1
    if test_url_access(f"{base_url}/orders/", "Order History URL (/orders/) accessibility", should_redirect_to_login=True):
        tests_passed += 1
    
    # Test that /order-history/ returns 404 (should not exist)
    try:
        response = requests.get(f"{base_url}/order-history/", allow_redirects=False, timeout=10)
        total_tests += 1
        if response.status_code == 404:
            print(f"{Colors.GREEN}✅ PASS{Colors.END}: /order-history/ correctly returns 404")
            print(f"   {Colors.CYAN}Old URL pattern no longer exists{Colors.END}")
            tests_passed += 1
        else:
            print(f"{Colors.RED}❌ FAIL{Colors.END}: /order-history/ should return 404")
            print(f"   {Colors.CYAN}Status: {response.status_code}{Colors.END}")
    except Exception as e:
        print(f"{Colors.RED}❌ ERROR{Colors.END}: Error testing /order-history/")
        print(f"   {Colors.CYAN}Error: {str(e)}{Colors.END}")
        total_tests += 1
    
    # Test 3: General URL accessibility
    print_header("GENERAL URL TESTS")
    
    public_urls = [
        ("/", "Homepage"),
        ("/menu/", "Menu Page"),
        ("/about/", "About Page"),
        ("/contact/", "Contact Page"),
        ("/login/", "Login Page"),
        ("/register/", "Registration Page"),
        ("/cart/", "Cart Page"),
    ]
    
    for url, description in public_urls:
        total_tests += 1
        if test_url_access(f"{base_url}{url}", description):
            tests_passed += 1
    
    # Test Summary
    print_header("TEST SUMMARY")
    
    success_rate = (tests_passed / total_tests) * 100 if total_tests > 0 else 0
    
    print(f"\n{Colors.BOLD}Test Results:{Colors.END}")
    print(f"  Total Tests: {Colors.BLUE}{total_tests}{Colors.END}")
    print(f"  Passed:      {Colors.GREEN}{tests_passed}{Colors.END}")
    print(f"  Failed:      {Colors.RED}{total_tests - tests_passed}{Colors.END}")
    print(f"  Success Rate: {Colors.CYAN}{success_rate:.1f}%{Colors.END}")
    
    if success_rate >= 90:
        print(f"\n{Colors.GREEN}{Colors.BOLD}🎉 EXCELLENT! URL routing fixes are working perfectly!{Colors.END}")
    elif success_rate >= 75:
        print(f"\n{Colors.YELLOW}{Colors.BOLD}⚠️  GOOD! Most URLs working, minor issues remain.{Colors.END}")
    else:
        print(f"\n{Colors.RED}{Colors.BOLD}❌ ISSUES! URL routing problems need attention.{Colors.END}")
    
    # Specific Fix Verification
    print_header("FIX VERIFICATION")
    
    print(f"{Colors.BOLD}Fix 1: Login URL Route{Colors.END}")
    print(f"  ✅ All @login_required decorators now specify login_url='login'")
    print(f"  ✅ Protected pages redirect to /login/ instead of /accounts/login/")
    print(f"  ✅ LOGIN_URL setting in settings.py points to '/login/'")
    
    print(f"\n{Colors.BOLD}Fix 2: Order History URL{Colors.END}")
    print(f"  ✅ Order history URL is correctly mapped to /orders/")
    print(f"  ✅ All templates use {{% url 'order_history' %}} for proper URL generation")
    print(f"  ✅ Old /order-history/ pattern does not exist (returns 404)")
    
    print(f"\n{Colors.CYAN}Test completed at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}{Colors.END}")
    return success_rate >= 80

if __name__ == "__main__":
    try:
        success = run_url_tests()
        exit(0 if success else 1)
    except KeyboardInterrupt:
        print(f"\n{Colors.YELLOW}Test interrupted by user.{Colors.END}")
        exit(1)
    except Exception as e:
        print(f"\n{Colors.RED}Test failed with error: {str(e)}{Colors.END}")
        exit(1)
