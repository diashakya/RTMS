#!/usr/bin/env python3
"""
Test script for favorites functionality with existing food item
"""
import requests
import json

def test_with_existing_food():
    """Test add to cart with existing food item"""
    base_url = "http://127.0.0.1:8000"
    
    print("🧪 Testing Add to Cart with existing food item (ID: 2)...")
    
    # Create a session
    session = requests.Session()
    
    # Get CSRF token from menu page
    menu_response = session.get(f"{base_url}/menu/")
    csrf_token = menu_response.cookies.get('csrftoken')
    
    if not csrf_token:
        print("❌ Could not get CSRF token")
        return
    
    print(f"✅ CSRF token obtained: {csrf_token[:10]}...")
    
    # Test add to cart API
    headers = {
        'Content-Type': 'application/json',
        'X-CSRFToken': csrf_token,
        'Referer': f"{base_url}/favorites/"
    }
    
    data = {
        'type': 'food',
        'id': '2',  # Using existing food item ID
        'quantity': 1
    }
    
    try:
        response = session.post(
            f"{base_url}/api/add-to-cart/",
            headers=headers,
            json=data
        )
        
        print(f"Status Code: {response.status_code}")
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Add to cart successful: {result}")
        else:
            print(f"❌ Add to cart failed: {response.text}")
            
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    test_with_existing_food()
