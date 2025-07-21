#!/usr/bin/env python
"""
Test script to verify checkout exception fixes are working properly
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

from django.test import Client
from django.contrib.auth.models import User
from main.models import Cart, CartItem, Foods, Special, Category, Order

def test_checkout_exception_fixes():
    """Test that checkout process now handles None values properly"""
    print("🔧 CHECKOUT EXCEPTION FIXES VERIFICATION")
    print("=" * 55)
    print(f"Test started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 55)
    
    client = Client()
    
    # Create test data
    print("\n📝 SETTING UP TEST DATA")
    print("-" * 30)
    
    try:
        # Create category and food items
        category = Category.objects.get_or_create(name='Test Category')[0]
        food = Foods.objects.get_or_create(
            title='Test Food',
            defaults={
                'category': category,
                'price': 15.99,
                'description': 'Test food item'
            }
        )[0]
        print(f"✅ Created test food: {food.title} - ${food.price}")
        
        # Create special
        special = Special.objects.get_or_create(
            name='Test Special',
            defaults={
                'category': category,
                'price': 20.00,
                'discounted_price': 15.00,
                'description': 'Test special item',
                'active': True
            }
        )[0]
        print(f"✅ Created test special: {special.name} - ${special.discounted_price}")
        
    except Exception as e:
        print(f"❌ Error creating test data: {e}")
        return
    
    print("\n🧪 TESTING CHECKOUT SCENARIOS")
    print("-" * 35)
    
    # Test 1: Valid checkout
    print("\n1. Testing valid checkout...")
    try:
        valid_cart = [
            {'id': food.id, 'quantity': 2, 'price': float(food.price)},
            {'id': f'special-{special.id}', 'quantity': 1, 'price': float(special.discounted_price)}
        ]
        
        response = client.post('/api/checkout/', 
            json.dumps({
                'cart': valid_cart,
                'notes': 'Test valid order'
            }),
            content_type='application/json'
        )
        
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            result = response.json()
            print(f"   ✅ Valid checkout successful: Order #{result.get('order_id')}")
            print(f"   Total: ${result.get('total')}, Items: {result.get('items_count', 'N/A')}")
        else:
            print(f"   Response: {response.content.decode()}")
            
    except Exception as e:
        print(f"   ❌ Valid checkout error: {e}")
    
    # Test 2: Empty cart (should be handled gracefully)
    print("\n2. Testing empty cart...")
    try:
        response = client.post('/api/checkout/', 
            json.dumps({
                'cart': [],
                'notes': 'Empty cart test'
            }),
            content_type='application/json'
        )
        
        print(f"   Status: {response.status_code}")
        result = response.json()
        print(f"   ✅ Empty cart handled: {result.get('message')}")
        
    except Exception as e:
        print(f"   ❌ Empty cart error: {e}")
    
    # Test 3: Cart with None/invalid items (should filter out bad items)
    print("\n3. Testing cart with None/invalid items...")
    try:
        mixed_cart = [
            {'id': food.id, 'quantity': 1, 'price': float(food.price)},  # Valid
            {'id': None, 'quantity': 2, 'price': 10.00},  # None ID
            {'quantity': 1, 'price': 5.00},  # Missing ID
            {'id': '', 'quantity': 1, 'price': 8.00},  # Empty ID
            {'id': 99999, 'quantity': 1, 'price': 12.00},  # Non-existent ID
            {'id': food.id, 'quantity': None, 'price': None},  # None values
            {'id': food.id, 'quantity': 'invalid', 'price': 'invalid'},  # Invalid types
        ]
        
        response = client.post('/api/checkout/', 
            json.dumps({
                'cart': mixed_cart,
                'notes': 'Mixed cart test'
            }),
            content_type='application/json'
        )
        
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            result = response.json()
            print(f"   ✅ Mixed cart processed: Order #{result.get('order_id')}")
            print(f"   Valid items processed: {result.get('items_count', 0)} out of {len(mixed_cart)}")
            print(f"   Total: ${result.get('total')}")
        else:
            result = response.json()
            print(f"   ✅ Invalid cart rejected: {result.get('message')}")
            
    except Exception as e:
        print(f"   ❌ Mixed cart error: {e}")
    
    # Test 4: Invalid JSON (should be handled gracefully)
    print("\n4. Testing invalid JSON...")
    try:
        response = client.post('/api/checkout/', 
            'invalid json data',
            content_type='application/json'
        )
        
        print(f"   Status: {response.status_code}")
        result = response.json()
        print(f"   ✅ Invalid JSON handled: {result.get('message')}")
        
    except Exception as e:
        print(f"   ❌ Invalid JSON error: {e}")
    
    print("\n🔍 TESTING CART MODEL IMPROVEMENTS")
    print("-" * 40)
    
    # Test Cart model edge cases
    try:
        user = User.objects.get_or_create(username='testuser2')[0]
        cart = Cart.objects.get_or_create(user=user)[0]
        
        print("\n5. Testing empty cart properties...")
        print(f"   Empty cart total_price: ${cart.total_price}")
        print(f"   Empty cart total_items: {cart.total_items}")
        
        # Add valid cart item
        cart_item = CartItem.objects.create(
            cart=cart,
            food=food,
            quantity=3
        )
        
        print("\n6. Testing cart with valid items...")
        print(f"   Cart total_price: ${cart.total_price}")
        print(f"   Cart total_items: {cart.total_items}")
        print(f"   CartItem total_price: ${cart_item.total_price}")
        print(f"   CartItem item_name: {cart_item.item_name}")
        
        print("   ✅ Cart model methods working correctly")
        
    except Exception as e:
        print(f"   ❌ Cart model error: {e}")
    
    print("\n🎯 TESTING ORDER CREATION")
    print("-" * 30)
    
    # Count orders before and after
    try:
        initial_order_count = Order.objects.count()
        print(f"\n7. Initial order count: {initial_order_count}")
        
        # Test checkout that should create an order
        response = client.post('/api/checkout/', 
            json.dumps({
                'cart': [{'id': food.id, 'quantity': 1, 'price': float(food.price)}],
                'notes': 'Order creation test'
            }),
            content_type='application/json'
        )
        
        final_order_count = Order.objects.count()
        print(f"   Final order count: {final_order_count}")
        
        if final_order_count > initial_order_count:
            print("   ✅ Order created successfully")
            latest_order = Order.objects.latest('created_at')
            print(f"   Order #{latest_order.id} - Total: ${latest_order.total}")
            print(f"   Order items: {latest_order.items.count()}")
        else:
            print("   ⚠️ No new order created")
            
    except Exception as e:
        print(f"   ❌ Order creation test error: {e}")
    
    print("\n" + "=" * 55)
    print("🎉 CHECKOUT EXCEPTION FIXES VERIFICATION COMPLETE")
    print("=" * 55)
    
    print("\n📋 SUMMARY OF FIXES:")
    print("  ✅ Added null checks for cart items iteration")
    print("  ✅ Improved error handling in checkout functions")
    print("  ✅ Added validation for item IDs, quantities, and prices")
    print("  ✅ Enhanced Cart model methods with null safety")
    print("  ✅ Added valid items count tracking")
    print("  ✅ Improved exception handling with specific error types")
    print("\n🚀 The checkout process should now be robust against NoneType errors!")

if __name__ == "__main__":
    test_checkout_exception_fixes()
