#!/usr/bin/env python3
"""
Order Type Test Script for Restaurant Management System
Tests the delivery and dine-in order functionality
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
from main.models import Foods, Cart, CartItem, Order

def test_order_types():
    """Test delivery and dine-in order types"""
    print("🚀 Order Type Functionality Test")
    print("=" * 50)
    
    client = Client()
    
    # Get or create a test user
    print("👤 Setting up test user...")
    try:
        user = User.objects.get(username='testuser')
        print("   ✅ Using existing testuser")
    except User.DoesNotExist:
        user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='password123'
        )
        print("   ✅ Created new testuser")
    
    # Login
    login_success = client.login(username='testuser', password='password123')
    print(f"   Login: {'✅ Success' if login_success else '❌ Failed'}")
    
    # Add item to cart
    print("\n🛒 Setting up cart...")
    food = Foods.objects.first()
    response = client.post('/api/add-to-cart/', 
        data=json.dumps({
            'type': 'food',
            'id': food.id,
            'quantity': 1
        }),
        content_type='application/json'
    )
    
    if response.status_code == 200:
        data = json.loads(response.content)
        if data.get('success'):
            print(f"   ✅ Added {food.title} to cart")
        else:
            print(f"   ❌ Failed to add to cart: {data.get('message')}")
    else:
        print(f"   ❌ Cart request failed: {response.status_code}")
    
    # Test cart page
    print("\n🛒 Testing cart page...")
    response = client.get('/cart/')
    if response.status_code == 200:
        print("   ✅ Cart page loads successfully")
        print("   📋 Page should show:")
        print("      • Order type selection")
        print("      • Cart items with quantity controls")
        print("      • Order total calculation")
        print("      • Checkout button")
    else:
        print(f"   ❌ Cart page failed: {response.status_code}")
    
    # Check existing orders for order types
    print("\n📦 Checking existing orders...")
    delivery_orders = Order.objects.filter(order_type='delivery').count()
    dine_in_orders = Order.objects.filter(order_type='dine_in').count()
    total_orders = Order.objects.count()
    
    print(f"   📊 Order Statistics:")
    print(f"      • Total orders: {total_orders}")
    print(f"      • Delivery orders: {delivery_orders}")
    print(f"      • Dine-in orders: {dine_in_orders}")
    
    # Show sample orders
    recent_orders = Order.objects.all().order_by('-created_at')[:3]
    if recent_orders:
        print(f"   📋 Recent Orders:")
        for order in recent_orders:
            order_location = order.delivery_address if order.order_type == 'delivery' else f"Table {order.table_number}"
            print(f"      • #{order.id}: {order.order_type.title()} - {order_location} - Rs {order.total}")
    
    print("\n" + "=" * 50)
    print("✅ Order type test completed!")
    print("\n🎯 Manual Testing Recommendations:")
    print("   1. Visit http://127.0.0.1:8000/cart/ in browser")
    print("   2. Select 'Delivery' - verify address field appears")
    print("   3. Select 'Dine In' - verify table number field appears")
    print("   4. Test form submission with both order types")
    print("   5. Check admin panel for order management")

if __name__ == "__main__":
    test_order_types()
