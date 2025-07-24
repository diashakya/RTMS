#!/usr/bin/env python3
"""
Test order type functionality in cart
"""
import os
import sys
import django

# Add the Menu directory to Python path
sys.path.append('c:/Users/ASUS/OneDrive/Desktop/RTMS1/Menu')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Menu.settings')

django.setup()

from django.test import Client
from main.models import Foods, Cart, CartItem

def test_order_type_display():
    print("Testing order type display and functionality...")
    
    # Create a test client
    client = Client()
    
    # Get a food item
    food = Foods.objects.first()
    print(f"Using food: {food.title}")
    
    # Visit cart page and add an item
    response = client.get('/cart/')
    session = client.session
    
    # Create cart with items
    cart, created = Cart.objects.get_or_create(session_key=session.session_key)
    cart_item, item_created = CartItem.objects.get_or_create(
        cart=cart,
        food=food,
        defaults={'quantity': 2}
    )
    
    # Get cart page with items
    response = client.get('/cart/')
    print(f"Cart page status: {response.status_code}")
    
    # Check if order type options are in the response
    content = response.content.decode()
    
    print("\n--- Checking Order Type Display ---")
    delivery_check = 'value="delivery"' in content and 'Delivery' in content
    dine_in_check = 'value="dine_in"' in content and 'Dine In' in content
    
    print(f"✅ Delivery option found: {delivery_check}")
    print(f"✅ Dine In option found: {dine_in_check}")
    
    # Check payment methods
    print("\n--- Checking Payment Methods ---")
    cash_check = 'value="cash"' in content and 'Cash Payment' in content
    card_check = 'value="card"' in content and 'Card Payment' in content
    wallet_check = 'value="wallet"' in content and 'Digital Wallet' in content
    
    print(f"✅ Cash payment option found: {cash_check}")
    print(f"✅ Card payment option found: {card_check}")
    print(f"✅ Wallet payment option found: {wallet_check}")
    
    # Test form submission with delivery
    print("\n--- Testing Delivery Order Submission ---")
    csrf_token = None
    import re
    match = re.search(rb'name="csrfmiddlewaretoken" value="([^"]+)"', response.content)
    if match:
        csrf_token = match.group(1).decode()
    
    if csrf_token:
        checkout_data = {
            'csrfmiddlewaretoken': csrf_token,
            'order_type': 'delivery',
            'customer_firstname': 'John',
            'customer_lastname': 'Doe',
            'customer_mobileno': '9841234567',
            'customer_email': 'john@example.com',
            'customer_address': '123 Test Street, Kathmandu',
            'payment_method': 'cash',
            'checkout': 'Place Order'
        }
        
        response = client.post('/cart/', checkout_data)
        print(f"Delivery order response: {response.status_code}")
        
        if response.status_code == 302:
            print("✅ Order placed successfully!")
        else:
            print("❌ Order placement failed")
            # Print any form errors
            if hasattr(response, 'context') and response.context and 'checkout_form' in response.context:
                form = response.context['checkout_form']
                if form.errors:
                    print(f"Form errors: {form.errors}")
    
    # Test with dine in
    print("\n--- Testing Dine In Order Submission ---")
    # Create new cart item for dine in test
    cart_item2, _ = CartItem.objects.get_or_create(
        cart=cart,
        food=Foods.objects.all()[1] if Foods.objects.count() > 1 else food,
        defaults={'quantity': 1}
    )
    
    if csrf_token:
        checkout_data_dine = {
            'csrfmiddlewaretoken': csrf_token,
            'order_type': 'dine_in',
            'customer_firstname': 'Jane',
            'customer_lastname': 'Smith',
            'customer_mobileno': '9851234567',
            'customer_email': 'jane@example.com',
            'table_number': 'T-05',
            'payment_method': 'card',
            'checkout': 'Place Order'
        }
        
        response = client.post('/cart/', checkout_data_dine)
        print(f"Dine in order response: {response.status_code}")
        
        if response.status_code == 302:
            print("✅ Dine in order placed successfully!")
        else:
            print("❌ Dine in order placement failed")

if __name__ == "__main__":
    test_order_type_display()
