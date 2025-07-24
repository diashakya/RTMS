#!/usr/bin/env python3
"""
Comprehensive test for favorites page functionality
"""
import requests
import json
import time

def test_favorites_page_comprehensive():
    """Test favorites page functionality comprehensively"""
    base_url = "http://127.0.0.1:8000"
    
    print("🧪 Comprehensive Favorites Page Test")
    print("=" * 50)
    
    # Create session for consistent cookies
    session = requests.Session()
    
    # Step 1: Load favorites page
    print("\n1. Loading favorites page...")
    try:
        favorites_response = session.get(f"{base_url}/favorites/")
        if favorites_response.status_code == 200:
            print("✅ Favorites page loaded successfully")
            print(f"   Page size: {len(favorites_response.content)} bytes")
            
            # Check if CSRF token is in the page
            page_content = favorites_response.text
            if 'csrfmiddlewaretoken' in page_content:
                print("✅ CSRF token found in page")
            else:
                print("⚠️  CSRF token not found in page content")
                
            # Check for JavaScript event handlers
            if 'add-to-cart-btn' in page_content:
                print("✅ Add to cart buttons found in HTML")
            else:
                print("⚠️  Add to cart buttons not found")
                
            if 'addToCartFromFavorites' in page_content:
                print("✅ JavaScript function addToCartFromFavorites found")
            else:
                print("⚠️  JavaScript function addToCartFromFavorites not found")
                
        else:
            print(f"❌ Favorites page failed: {favorites_response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Error loading favorites: {e}")
        return False
    
    # Step 2: Get CSRF token
    print("\n2. Getting CSRF token...")
    csrf_token = favorites_response.cookies.get('csrftoken')
    if csrf_token:
        print(f"✅ CSRF token obtained: {csrf_token[:10]}...")
    else:
        print("❌ Could not get CSRF token from cookies")
        return False
    
    # Step 3: Test add to cart API endpoint
    print("\n3. Testing add to cart from favorites...")
    headers = {
        'Content-Type': 'application/json',
        'X-CSRFToken': csrf_token,
        'Referer': f"{base_url}/favorites/"
    }
    
    # Test with existing food item
    test_data = {
        'type': 'food',
        'id': '2',  # Known existing food item
        'quantity': 1
    }
    
    try:
        cart_response = session.post(
            f"{base_url}/api/add-to-cart/",
            headers=headers,
            json=test_data
        )
        
        print(f"   Status: {cart_response.status_code}")
        if cart_response.status_code == 200:
            result = cart_response.json()
            if result.get('success'):
                print(f"✅ Add to cart API working: {result['message']}")
                print(f"   Cart count: {result.get('cart_count', 'N/A')}")
            else:
                print(f"❌ Add to cart failed: {result.get('message')}")
        else:
            print(f"❌ API call failed: {cart_response.text}")
    except Exception as e:
        print(f"❌ Error testing add to cart: {e}")
    
    # Step 4: Test remove favorite API
    print("\n4. Testing remove favorite API...")
    try:
        # First get existing favorites to test with
        shell_command = 'from main.models import Favorite; print(Favorite.objects.first().id if Favorite.objects.exists() else "No favorites")'
        
        # For testing, let's try with a sample favorite ID
        remove_data = {
            'favorite_id': '1'  # This might not exist, but we're testing the endpoint
        }
        
        remove_response = session.post(
            f"{base_url}/api/remove-favorite/",
            headers=headers,
            json=remove_data
        )
        
        print(f"   Status: {remove_response.status_code}")
        if remove_response.status_code == 200:
            result = remove_response.json()
            print(f"   Response: {result}")
        else:
            print(f"   Response: {remove_response.text}")
            
    except Exception as e:
        print(f"❌ Error testing remove favorite: {e}")
    
    # Step 5: Check page structure
    print("\n5. Analyzing page structure...")
    if 'data-id="food-' in page_content:
        print("✅ Food items have correct data-id attributes")
    else:
        print("⚠️  Food items may not have correct data-id attributes")
        
    if 'addEventListener' in page_content:
        print("✅ JavaScript event listeners are set up")
    else:
        print("⚠️  JavaScript event listeners might not be properly set up")
    
    # Step 6: Recommendations
    print("\n" + "=" * 50)
    print("🔍 DIAGNOSIS AND RECOMMENDATIONS:")
    print("\nPossible reasons for non-functional buttons:")
    print("1. JavaScript errors in browser console")
    print("2. CSRF token not properly passed to AJAX calls")
    print("3. API endpoints returning errors")
    print("4. User not logged in (favorites require authentication)")
    print("5. No favorites exist for current user")
    
    print("\n✅ QUICK FIXES TO TRY:")
    print("1. Check browser developer tools console for errors")
    print("2. Ensure user is logged in before accessing favorites")
    print("3. Add some items to favorites first from menu page")
    print("4. Clear browser cache and cookies")
    print("5. Check that JavaScript is enabled")
    
    return True

if __name__ == "__main__":
    test_favorites_page_comprehensive()
