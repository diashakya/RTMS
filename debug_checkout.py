#!/usr/bin/env python
"""
Debug script to identify and fix NoneType iteration issues in checkout process
"""
import os
import django
import sys
import json
from datetime import datetime

# Add the Menu directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'Menu'))

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Menu.settings')
django.setup()

from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from main.models import Cart, CartItem, Foods, Special, Category

def debug_checkout_process():
    """Debug checkout process to identify NoneType iteration issues"""
    print("🔍 CHECKOUT EXCEPTION DEBUG SCRIPT")
    print("=" * 50)
    print(f"Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 50)
    
    # Create test client
    client = Client()
    
    # Test scenarios that could cause NoneType iteration
    test_scenarios = [
        "Empty cart checkout",
        "Cart with None items",
        "Cart items with None food/special",
        "Cart items with None quantities",
        "Cart items with None prices"
    ]
    
    print("\n🧪 TESTING POTENTIAL NONETYPE SCENARIOS")
    print("-" * 40)
    
    # Scenario 1: Empty cart checkout
    print("\n1. Testing empty cart checkout...")
    try:
        response = client.post('/api/checkout/', 
            json.dumps({
                'cart': [],
                'notes': 'Test order'
            }),
            content_type='application/json'
        )
        print(f"   ✅ Empty cart handled properly: {response.status_code}")
        if response.status_code == 200:
            result = response.json()
            print(f"   Response: {result}")
    except Exception as e:
        print(f"   ❌ Empty cart error: {e}")
    
    # Scenario 2: Cart with None/missing item IDs
    print("\n2. Testing cart with None item IDs...")
    try:
        response = client.post('/api/checkout/', 
            json.dumps({
                'cart': [
                    {'id': None, 'quantity': 1, 'price': 10.00},
                    {'quantity': 2, 'price': 15.00},  # Missing ID
                    {'id': '', 'quantity': 1, 'price': 5.00}  # Empty ID
                ],
                'notes': 'Test order'
            }),
            content_type='application/json'
        )
        print(f"   ✅ None item IDs handled: {response.status_code}")
        if response.status_code == 200:
            result = response.json()
            print(f"   Response: {result}")
    except Exception as e:
        print(f"   ❌ None item IDs error: {e}")
    
    # Scenario 3: Cart with None quantities/prices
    print("\n3. Testing cart with None quantities/prices...")
    try:
        # Create a test food item first
        category = Category.objects.get_or_create(name='Test Category')[0]
        food = Foods.objects.get_or_create(
            title='Test Food',
            defaults={
                'category': category,
                'price': 10.00,
                'description': 'Test food item'
            }
        )[0]
        
        response = client.post('/api/checkout/', 
            json.dumps({
                'cart': [
                    {'id': food.id, 'quantity': None, 'price': None},
                    {'id': food.id, 'quantity': 0, 'price': 0},
                    {'id': food.id}  # Missing quantity and price
                ],
                'notes': 'Test order'
            }),
            content_type='application/json'
        )
        print(f"   ✅ None quantities/prices handled: {response.status_code}")
        if response.status_code == 200:
            result = response.json()
            print(f"   Response: {result}")
    except Exception as e:
        print(f"   ❌ None quantities/prices error: {e}")
    
    print("\n🔍 EXAMINING CART MODEL METHODS")
    print("-" * 40)
    
    # Test Cart model methods with edge cases
    try:
        # Create test user and cart
        user = User.objects.get_or_create(username='testuser')[0]
        cart = Cart.objects.get_or_create(user=user)[0]
        
        print(f"\n4. Testing cart.total_price with no items...")
        total_price = cart.total_price
        print(f"   ✅ Cart total_price: {total_price}")
        
        print(f"\n5. Testing cart.total_items with no items...")
        total_items = cart.total_items
        print(f"   ✅ Cart total_items: {total_items}")
        
        # Add a cart item with potential None values
        cart_item = CartItem.objects.create(
            cart=cart,
            food=food,
            quantity=None  # This could cause issues
        )
        
        print(f"\n6. Testing cart with None quantity item...")
        total_price = cart.total_price
        total_items = cart.total_items
        print(f"   ✅ Cart total_price with None quantity: {total_price}")
        print(f"   ✅ Cart total_items with None quantity: {total_items}")
        
        # Test CartItem properties
        print(f"\n7. Testing CartItem properties...")
        print(f"   item_price: {cart_item.item_price}")
        print(f"   total_price: {cart_item.total_price}")
        print(f"   item_name: {cart_item.item_name}")
        
    except Exception as e:
        print(f"   ❌ Cart model error: {e}")
    
    print("\n🔍 CHECKING FOR COMMON ITERATION ISSUES")
    print("-" * 40)
    
    # Check for potential issues in views
    from main.views import get_or_create_cart
    
    try:
        print("\n8. Testing get_or_create_cart with mock request...")
        class MockRequest:
            def __init__(self):
                self.user = user
                self.session = {}
        
        mock_request = MockRequest()
        cart = get_or_create_cart(mock_request)
        print(f"   ✅ get_or_create_cart successful: {cart}")
        
        # Test cart.items.all() with None cart
        print("\n9. Testing cart.items.all() access...")
        if cart:
            items = cart.items.all()
            print(f"   ✅ cart.items.all() successful: {list(items)}")
            
            # Test iteration over items
            print("\n10. Testing iteration over cart items...")
            for item in items:
                print(f"   Item: {item}, Food: {item.food}, Quantity: {item.quantity}")
        
    except Exception as e:
        print(f"   ❌ get_or_create_cart error: {e}")
    
    print("\n" + "=" * 50)
    print("🎯 CHECKOUT DEBUG COMPLETED")
    print("=" * 50)

if __name__ == "__main__":
    debug_checkout_process()
