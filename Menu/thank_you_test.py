#!/usr/bin/env python3
"""
Thank You Page Test Script
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

def test_thank_you_page():
    """Test thank you page functionality"""
    print("🎉 Testing Thank You Page")
    print("=" * 40)
    
    client = Client()
    
    # Test 1: Thank you page without order ID
    print("📄 Testing thank you page (no order)...")
    response = client.get('/thank-you/')
    status = "✅ PASS" if response.status_code == 200 else f"❌ FAIL ({response.status_code})"
    print(f"   Without order ID: {status}")
    
    # Test 2: Thank you page with valid order ID
    print("\n📦 Testing thank you page (with order)...")
    try:
        # Get an existing order
        order = Order.objects.first()
        if order:
            response = client.get(f'/thank-you/{order.id}/')
            status = "✅ PASS" if response.status_code == 200 else f"❌ FAIL ({response.status_code})"
            print(f"   With order #{order.id}: {status}")
            
            if response.status_code == 200:
                content = response.content.decode('utf-8')
                if f"Order #{order.id}" in content:
                    print("   ✅ Order details displayed correctly")
                else:
                    print("   ⚠️ Order details might not be displaying")
                    
                if "Thank You for Your Order!" in content:
                    print("   ✅ Thank you message displayed")
                else:
                    print("   ❌ Thank you message missing")
        else:
            print("   ⚠️ No orders found in database")
    except Exception as e:
        print(f"   ❌ Error testing with order: {str(e)}")
    
    # Test 3: Thank you page with invalid order ID
    print("\n🚫 Testing thank you page (invalid order)...")
    response = client.get('/thank-you/999999/')
    status = "✅ PASS" if response.status_code == 200 else f"❌ FAIL ({response.status_code})"
    print(f"   Invalid order ID: {status}")
    
    # Test 4: Check order statistics
    print("\n📊 Order Statistics:")
    total_orders = Order.objects.count()
    recent_orders = Order.objects.all().order_by('-created_at')[:3]
    
    print(f"   Total orders: {total_orders}")
    if recent_orders:
        print("   Recent orders:")
        for order in recent_orders:
            order_location = order.delivery_address if order.order_type == 'delivery' else f"Table {order.table_number}"
            print(f"      • #{order.id}: {order.order_type.title()} - {order_location}")
    
    print("\n" + "=" * 40)
    print("✅ Thank you page test completed!")

if __name__ == "__main__":
    test_thank_you_page()
