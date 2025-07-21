#!/usr/bin/env python3
"""
Test script for favorites functionality
"""
import requests
import json
import sys

def test_favorites_functionality():
    """Test the favorites page functionality"""
    base_url = "http://127.0.0.1:8000"
    
    print("🧪 Testing Favorites Functionality...")
    print("=" * 50)
    
    # Test 1: Check if favorites page loads
    print("\n1. Testing favorites page load...")
    try:
        response = requests.get(f"{base_url}/favorites/")
        if response.status_code == 200:
            print("✅ Favorites page loads successfully")
            print(f"   Response size: {len(response.content)} bytes")
        else:
            print(f"❌ Favorites page failed with status: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Error loading favorites page: {e}")
        return False
    
    # Test 2: Get CSRF token first
    print("\n2. Getting CSRF token...")
    try:
        # Get CSRF token from menu page
        menu_response = requests.get(f"{base_url}/menu/")
        if 'csrftoken' in menu_response.cookies:
            csrf_token = menu_response.cookies['csrftoken']
            print(f"✅ CSRF token obtained: {csrf_token[:10]}...")
        else:
            print("❌ Could not get CSRF token")
            return False
    except Exception as e:
        print(f"❌ Error getting CSRF token: {e}")
        return False
    
    # Test 3: Test add to cart API endpoint
    print("\n3. Testing add to cart API endpoint...")
    try:
        headers = {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrf_token,
            'Referer': f"{base_url}/favorites/"
        }
        
        # Create a session to maintain cookies
        session = requests.Session()
        session.get(f"{base_url}/menu/")  # Get session cookies
        
        data = {
            'type': 'food',
            'id': '1',  # Assuming food item with ID 1 exists
            'quantity': 1
        }
        
        response = session.post(
            f"{base_url}/api/add-to-cart/",
            headers=headers,
            json=data
        )
        
        print(f"   Status Code: {response.status_code}")
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Add to cart API working: {result}")
        else:
            print(f"❌ Add to cart failed: {response.text}")
            
    except Exception as e:
        print(f"❌ Error testing add to cart API: {e}")
    
    # Test 4: Check JavaScript console errors (simulate)
    print("\n4. Checking common JavaScript issues...")
    
    # Check if CSRF token is available in the page
    if 'csrf' in response.text.lower():
        print("✅ CSRF token likely available in page")
    else:
        print("⚠️  CSRF token might not be available in page")
    
    # Check if jQuery/fetch is available
    if 'fetch' in response.text or 'jquery' in response.text.lower():
        print("✅ JavaScript fetch/AJAX capability detected")
    else:
        print("⚠️  JavaScript AJAX capability not clearly detected")
    
    print("\n" + "=" * 50)
    print("🔍 Possible Issues and Solutions:")
    print("1. Check browser console for JavaScript errors")
    print("2. Ensure CSRF token is properly included")
    print("3. Verify API endpoints are accessible")
    print("4. Check if items exist in favorites to test")
    print("5. Make sure user is logged in")
    
    return True

if __name__ == "__main__":
    try:
        test_favorites_functionality()
    except KeyboardInterrupt:
        print("\n\n🛑 Test interrupted by user")
    except Exception as e:
        print(f"\n\n❌ Test failed with error: {e}")
