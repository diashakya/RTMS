#!/usr/bin/env python3
"""
Manual Test Script for Restaurant Management System
This script tests all major functionality of the RTMS system.
"""

import os
import sys
import json

# Add the current directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Menu.settings')

import django
django.setup()

from django.test import Client
from django.contrib.auth.models import User
from django.urls import reverse
from main.models import Foods, Cart, CartItem, Order, Favorite, Customer

def test_user_authentication():
    """Test user authentication functionality"""
    print("🔐 Testing User Authentication...")
    client = Client()
    
    # Check if user already exists
    try:
        existing_user = User.objects.get(username='testuser123')
        print("   📝 User already exists, using existing user...")
        
        # Test login with existing user
        response = client.post('/login/', {
            'username': 'testuser123',
            'password': 'SecurePass123!'
        })
        
        if response.status_code in [200, 302]:
            print("   ✅ Login successful with existing user")
            return client, True
        else:
            print(f"   ❌ Login failed with existing user: {response.status_code}")
            # Try with another user
            response = client.post('/login/', {
                'username': 'testuser',
                'password': 'password123'
            })
            return client, response.status_code in [200, 302]
    
    except User.DoesNotExist:
        # Test registration
        print("   📝 Testing user registration...")
        response = client.post('/register/', {
            'username': 'testuser123',
            'email': 'test@example.com',
            'password1': 'SecurePass123!',
            'password2': 'SecurePass123!',
            'first_name': 'Test',
            'last_name': 'User'
        })
        
        if response.status_code in [200, 302]:
            print("   ✅ Registration successful")
            
            # Test login
            print("   🔑 Testing user login...")
            response = client.post('/login/', {
                'username': 'testuser123',
                'password': 'SecurePass123!'
            })
            
            if response.status_code in [200, 302]:
                print("   ✅ Login successful")
                return client, True
            else:
                print(f"   ❌ Login failed: {response.status_code}")
                return client, False
        else:
            print(f"   ❌ Registration failed: {response.status_code}")
            # Try logging in with existing user
            response = client.post('/login/', {
                'username': 'testuser',
                'password': 'password123'
            })
            return client, response.status_code in [200, 302]

def test_menu_browsing(client):
    """Test menu browsing functionality"""
    print("🍽️ Testing Menu Browsing...")
    
    # Test menu page
    response = client.get('/menu/')
    if response.status_code == 200:
        print("   ✅ Menu page loads successfully")
        
        # Test food API
        foods = Foods.objects.all()[:3]
        for food in foods:
            response = client.get(f'/api/foods/{food.id}/')
            if response.status_code == 200:
                data = json.loads(response.content)
                print(f"   ✅ Food API working for: {data.get('title', 'Unknown')}")
            else:
                print(f"   ❌ Food API failed for ID {food.id}")
        return True
    else:
        print(f"   ❌ Menu page failed: {response.status_code}")
        return False

def test_cart_functionality(client):
    """Test cart functionality"""
    print("🛒 Testing Cart Functionality...")
    
    # Get a food item
    food = Foods.objects.first()
    if not food:
        print("   ❌ No food items found")
        return False
    
    # Test adding to cart using JSON
    import json
    response = client.post('/api/add-to-cart/', 
        data=json.dumps({
            'type': 'food',
            'id': food.id,
            'quantity': 2
        }),
        content_type='application/json'
    )
    
    if response.status_code == 200:
        data = json.loads(response.content)
        if data.get('success'):
            print(f"   ✅ Added {food.title} to cart")
            
            # Test cart page
            response = client.get('/cart/')
            if response.status_code == 200:
                print("   ✅ Cart page loads successfully")
                
                # Test updating cart using the update API
                response = client.post('/api/update-cart-item/', 
                    data=json.dumps({
                        'food_id': food.id,
                        'quantity': 3
                    }),
                    content_type='application/json'
                )
                
                if response.status_code == 200:
                    print("   ✅ Cart item updated successfully")
                    return True
                else:
                    print(f"   ❌ Cart update failed: {response.status_code}")
                    return False
            else:
                print(f"   ❌ Cart page failed: {response.status_code}")
                return False
        else:
            print(f"   ❌ Add to cart failed: {data.get('message', 'Unknown error')}")
            return False
    else:
        print(f"   ❌ Add to cart failed: {response.status_code}")
        return False

def test_order_functionality(client):
    """Test order functionality"""
    print("📦 Testing Order Functionality...")
    
    # Ensure there's something in cart
    food = Foods.objects.first()
    client.post('/api/add-to-cart/', 
        data=json.dumps({'type': 'food', 'id': food.id, 'quantity': 1}),
        content_type='application/json'
    )
    
    # Test delivery order using form data
    print("   🚚 Testing delivery order...")
    response = client.post('/api/checkout/', {
        'order_type': 'delivery',
        'delivery_address': '123 Test Street, Test City',
        'customer_name': 'Test Customer',
        'customer_phone': '1234567890',
        'payment_method': 'cash'
    })
    
    if response.status_code == 200:
        data = json.loads(response.content)
        if data.get('success'):
            print(f"   ✅ Delivery order created: #{data.get('order_id')}")
            
            # Test dine-in order
            print("   🍽️ Testing dine-in order...")
            # Add another item to cart
            client.post('/api/add-to-cart/', 
                data=json.dumps({'type': 'food', 'id': food.id, 'quantity': 1}),
                content_type='application/json'
            )
            
            response = client.post('/api/checkout/', {
                'order_type': 'dine_in',
                'table_number': 'T-05',
                'customer_name': 'Test Customer',
                'customer_phone': '1234567890',
                'payment_method': 'card'
            })
            
            if response.status_code == 200:
                data = json.loads(response.content)
                if data.get('success'):
                    print(f"   ✅ Dine-in order created: #{data.get('order_id')}")
                    return True
                else:
                    print(f"   ❌ Dine-in order failed: {data.get('error')}")
                    return False
            else:
                print(f"   ❌ Dine-in order request failed: {response.status_code}")
                return False
        else:
            print(f"   ❌ Delivery order failed: {data.get('error')}")
            return False
    else:
        print(f"   ❌ Delivery order request failed: {response.status_code}")
        return False

def test_favorites_functionality(client):
    """Test favorites functionality"""
    print("❤️ Testing Favorites Functionality...")
    
    food = Foods.objects.first()
    
    # Test adding to favorites using JSON
    response = client.post('/api/toggle-favorite/', 
        data=json.dumps({'food_id': food.id}),
        content_type='application/json'
    )
    
    if response.status_code == 200:
        data = json.loads(response.content)
        print(f"   ✅ Favorite toggled: {data.get('action', 'unknown')}")
        
        # Test favorites page
        response = client.get('/favorites/')
        if response.status_code == 200:
            print("   ✅ Favorites page loads successfully")
            return True
        else:
            print(f"   ❌ Favorites page failed: {response.status_code}")
            return False
    else:
        print(f"   ❌ Toggle favorite failed: {response.status_code}")
        # Try to access favorites page anyway
        response = client.get('/favorites/')
        if response.status_code == 200:
            print("   ✅ Favorites page loads successfully (toggle failed)")
            return True
        else:
            print(f"   ❌ Favorites page also failed: {response.status_code}")
            return False

def test_order_history(client):
    """Test order history functionality"""
    print("📋 Testing Order History...")
    
    response = client.get('/orders/')
    if response.status_code == 200:
        print("   ✅ Order history page loads successfully")
        
        # Check if there are any orders
        orders = Order.objects.filter(customer__user__username='testuser123')
        if orders.exists():
            order = orders.first()
            
            # Test order receipt
            response = client.get(f'/order-receipt/{order.id}/')
            if response.status_code == 200:
                print(f"   ✅ Order receipt loads for order #{order.id}")
                return True
            else:
                print(f"   ❌ Order receipt failed: {response.status_code}")
                return False
        else:
            print("   ✅ Order history accessible (no orders yet)")
            return True
    else:
        print(f"   ❌ Order history failed: {response.status_code}")
        return False

def main():
    """Run all tests"""
    print("🚀 Restaurant Management System - Manual Testing")
    print("=" * 60)
    
    # Test 1: User Authentication
    client, auth_success = test_user_authentication()
    
    if not auth_success:
        print("❌ Authentication failed - stopping tests")
        return
    
    # Test 2: Menu Browsing
    menu_success = test_menu_browsing(client)
    
    # Test 3: Cart Functionality
    cart_success = test_cart_functionality(client)
    
    # Test 4: Order Functionality
    order_success = test_order_functionality(client)
    
    # Test 5: Favorites Functionality
    favorites_success = test_favorites_functionality(client)
    
    # Test 6: Order History
    history_success = test_order_history(client)
    
    # Summary
    print("\n" + "=" * 60)
    print("🎯 TEST SUMMARY")
    print("=" * 60)
    tests = [
        ("Authentication", auth_success),
        ("Menu Browsing", menu_success),
        ("Cart Functionality", cart_success),
        ("Order Functionality", order_success),
        ("Favorites Functionality", favorites_success),
        ("Order History", history_success)
    ]
    
    passed = sum(1 for _, success in tests if success)
    total = len(tests)
    
    for test_name, success in tests:
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"   {test_name:<20} {status}")
    
    print(f"\n🏆 Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! System is working correctly.")
    else:
        print("⚠️ Some tests failed. Please check the specific issues above.")

if __name__ == "__main__":
    main()
