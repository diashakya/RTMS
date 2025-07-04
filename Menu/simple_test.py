#!/usr/bin/env python3
"""
Simplified Test Script for Restaurant Management System
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

def simple_functionality_test():
    """Run a simple test of core functionality"""
    print("🚀 Simple Restaurant Management System Test")
    print("=" * 50)
    
    client = Client()
    
    # Test 1: Basic pages load
    print("📄 Testing basic page access...")
    pages = [
        ('/', 'Home'),
        ('/menu/', 'Menu'),
        ('/about/', 'About'),
        ('/contact/', 'Contact')
    ]
    
    for url, name in pages:
        try:
            response = client.get(url)
            status = "✅ PASS" if response.status_code == 200 else f"❌ FAIL ({response.status_code})"
            print(f"   {name:<10} {status}")
        except Exception as e:
            print(f"   {name:<10} ❌ ERROR: {str(e)}")
    
    # Test 2: Food API
    print("\n🍔 Testing Food API...")
    try:
        foods = Foods.objects.all()[:3]
        for food in foods:
            response = client.get(f'/api/foods/{food.id}/')
            if response.status_code == 200:
                data = json.loads(response.content)
                print(f"   ✅ {food.title} API working")
            else:
                print(f"   ❌ {food.title} API failed ({response.status_code})")
    except Exception as e:
        print(f"   ❌ Food API error: {str(e)}")
    
    # Test 3: Anonymous cart functionality
    print("\n🛒 Testing Cart (Anonymous)...")
    try:
        food = Foods.objects.first()
        
        # Test adding to cart
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
                status = "✅ PASS" if response.status_code == 200 else f"❌ FAIL ({response.status_code})"
                print(f"   Cart page: {status}")
            else:
                print(f"   ❌ Add to cart failed: {data.get('message', 'Unknown error')}")
        else:
            print(f"   ❌ Add to cart request failed: {response.status_code}")
    except Exception as e:
        print(f"   ❌ Cart test error: {str(e)}")
    
    # Test 4: Database state
    print("\n📊 Database Status...")
    try:
        food_count = Foods.objects.count()
        user_count = User.objects.count()
        order_count = Order.objects.count()
        cart_count = Cart.objects.count()
        
        print(f"   Foods: {food_count}")
        print(f"   Users: {user_count}")
        print(f"   Orders: {order_count}")
        print(f"   Carts: {cart_count}")
    except Exception as e:
        print(f"   ❌ Database error: {str(e)}")
    
    print("\n" + "=" * 50)
    print("✅ Simple test completed! Check results above.")

if __name__ == "__main__":
    simple_functionality_test()
