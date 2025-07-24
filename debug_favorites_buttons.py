#!/usr/bin/env python3
"""
Debug favorites page button functionality
"""
import requests
import json

def debug_favorites_buttons():
    """Debug why the favorites buttons are not working"""
    base_url = "http://127.0.0.1:8000"
    
    print("🔍 Debugging Favorites Page Button Issues")
    print("=" * 50)
    
    # Create session and login as aditya
    session = requests.Session()
    
    # Get login page first
    login_page = session.get(f"{base_url}/login/")
    csrf_token = login_page.cookies.get('csrftoken')
    
    print(f"1. CSRF Token: {csrf_token[:10]}..." if csrf_token else "❌ No CSRF token")
    
    # Login as aditya (assuming this user exists)
    login_data = {
        'username': 'aditya',
        'password': 'your_password_here',  # You'll need to provide this
        'csrfmiddlewaretoken': csrf_token
    }
    
    # For testing, let's check if favorites page loads
    print("\n2. Testing favorites page load...")
    favorites_response = session.get(f"{base_url}/favorites/")
    
    if favorites_response.status_code == 200:
        print("✅ Favorites page loads successfully")
        content = favorites_response.text
        
        # Check for required elements
        print("\n3. Checking page elements...")
        
        if 'add-to-cart-btn' in content:
            print("✅ Add to cart buttons found in HTML")
        else:
            print("❌ Add to cart buttons NOT found")
            
        if 'remove-favorite-btn' in content:
            print("✅ Remove favorite buttons found in HTML")
        else:
            print("❌ Remove favorite buttons NOT found")
            
        if 'csrfmiddlewaretoken' in content:
            print("✅ CSRF token found in page")
        else:
            print("❌ CSRF token NOT found in page")
            
        if 'addEventListener' in content:
            print("✅ JavaScript event listeners found")
        else:
            print("❌ JavaScript event listeners NOT found")
            
        # Check if the JavaScript functions are defined
        if 'addToCartFromFavorites' in content:
            print("✅ addToCartFromFavorites function found")
        else:
            print("❌ addToCartFromFavorites function NOT found")
            
        if 'removeFavorite' in content:
            print("✅ removeFavorite function found")
        else:
            print("❌ removeFavorite function NOT found")
            
    else:
        print(f"❌ Favorites page failed to load: {favorites_response.status_code}")
        if favorites_response.status_code == 302:
            print("   -> Redirected (probably to login page)")
        return
    
    # Test API endpoints
    print("\n4. Testing API endpoints...")
    
    # Get fresh CSRF token
    csrf_token = favorites_response.cookies.get('csrftoken')
    headers = {
        'Content-Type': 'application/json',
        'X-CSRFToken': csrf_token,
        'Referer': f"{base_url}/favorites/"
    }
    
    # Test add to cart API
    print("\n   a) Testing add-to-cart API...")
    test_add_data = {
        'type': 'food',
        'id': '4',  # American Classic Zinger ID
        'quantity': 1
    }
    
    add_response = session.post(
        f"{base_url}/api/add-to-cart/",
        headers=headers,
        json=test_add_data
    )
    
    print(f"   Status: {add_response.status_code}")
    if add_response.status_code == 200:
        result = add_response.json()
        print(f"   ✅ Add to cart works: {result}")
    else:
        print(f"   ❌ Add to cart failed: {add_response.text}")
    
    # Test remove favorite API (we need a valid favorite ID)
    print("\n   b) Testing remove-favorite API...")
    # This might fail without a valid favorite ID, but we're testing the endpoint
    test_remove_data = {
        'favorite_id': '1'
    }
    
    remove_response = session.post(
        f"{base_url}/api/remove-favorite/",
        headers=headers,
        json=test_remove_data
    )
    
    print(f"   Status: {remove_response.status_code}")
    print(f"   Response: {remove_response.text}")
    
    print("\n" + "=" * 50)
    print("🎯 LIKELY ISSUES AND SOLUTIONS:")
    print("\n1. JavaScript Console Errors:")
    print("   - Open browser dev tools (F12)")
    print("   - Check Console tab for red error messages")
    print("   - Common issues: CSRF token undefined, fetch not supported")
    
    print("\n2. Event Listener Problems:")
    print("   - Check if DOMContentLoaded event fires")
    print("   - Verify querySelector finds elements")
    print("   - Ensure buttons have correct classes/attributes")
    
    print("\n3. CSRF Token Issues:")
    print("   - Verify csrfmiddlewaretoken is in the page")
    print("   - Check if token is being passed to AJAX calls")
    
    print("\n4. API Authentication:")
    print("   - Ensure user is properly logged in")
    print("   - Check session cookies are maintained")
    
    print("\n✅ DEBUGGING STEPS:")
    print("1. Open browser dev tools (F12)")
    print("2. Go to Console tab")
    print("3. Click an 'Add to Cart' button")
    print("4. Look for any red error messages")
    print("5. Check Network tab for failed API calls")

if __name__ == "__main__":
    debug_favorites_buttons()
