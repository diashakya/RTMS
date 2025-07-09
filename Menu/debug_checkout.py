#!/usr/bin/env python
"""
Debug script to isolate the checkout NoneType error
"""
import os
import django
import sys
from pathlib import Path

# Add the project directory to Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Menu.settings')
django.setup()

from django.contrib.auth.models import User
from django.test import Client
from main.models import Foods, Category, Cart, CartItem, Customer
import traceback

def debug_checkout():
    """Debug the checkout process step by step"""
    print("🔍 Debug Checkout Process...")
    
    client = Client()
    
    try:
        # 1. Create test user
        print("1. Creating test user...")
        test_user, created = User.objects.get_or_create(
            username='debug_user',
            defaults={
                'email': 'debug@test.com',
                'first_name': 'Debug',
                'last_name': 'User',
                'password': 'testpass123'
            }
        )
        if created:
            test_user.set_password('testpass123')
            test_user.save()
        print(f"   ✅ User: {test_user.username}")
        
        # 2. Login
        print("2. Logging in...")
        login_result = client.login(username='debug_user', password='testpass123')
        print(f"   ✅ Login: {login_result}")
        
        # 3. Create cart with item
        print("3. Creating cart with item...")
        cart, created = Cart.objects.get_or_create(user=test_user)
        print(f"   ✅ Cart created: {created}")
        
        # Add item to cart if none exist
        if cart.items.count() == 0 and Foods.objects.exists():
            food_item = Foods.objects.first()
            CartItem.objects.create(cart=cart, food=food_item, quantity=1)
            print(f"   ✅ Added {food_item.title} to cart")
        
        print(f"   ✅ Cart has {cart.items.count()} items")
        print(f"   ✅ Cart total: Rs {cart.total_price}")
        
        # 4. Access cart page
        print("4. Accessing cart page...")
        response = client.get('/cart/')
        print(f"   ✅ Cart page status: {response.status_code}")
        
        # Safely check for context
        if hasattr(response, 'context') and response.context is not None:
            if 'checkout_form' in response.context:
                print("   ✅ Checkout form available")
            else:
                print("   ❌ No checkout form in context")
                print(f"   Available context keys: {list(response.context.keys())}")
        else:
            print("   ❌ No context available in response")
            print(f"   Response type: {type(response)}")
            print(f"   Response content preview: {response.content[:200]}")
            # Still try to continue with the test
        
        # 5. Test simple checkout data
        print("5. Testing checkout data...")
        checkout_data = {
            'order_type': 'delivery',
            'customer_firstname': 'Debug',
            'customer_lastname': 'Customer',
            'customer_mobileno': '9876543210',
            'customer_email': 'debug@test.com',
            'customer_address': '123 Debug Street',
            'payment_method': 'cash',
            'order_notes': 'Debug order',
            'checkout': 'true'
        }
        
        print("6. Submitting checkout form...")
        response = client.post('/cart/', checkout_data)
        print(f"   ✅ Checkout response status: {response.status_code}")
        
        if response.status_code == 302:
            print(f"   ✅ Redirected to: {response.url}")
        elif response.status_code == 200:
            print("   ✅ Form processed successfully")
        else:
            print(f"   ❌ Unexpected status code: {response.status_code}")
            
        return True
        
    except Exception as e:
        print(f"   ❌ Error: {e}")
        print(f"   ❌ Traceback:")
        traceback.print_exc()
        return False

if __name__ == "__main__":
    debug_checkout()
