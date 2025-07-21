#!/usr/bin/env python3
"""
Test cart button functionality using Django test client
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

def test_cart_buttons():
    print("Testing cart buttons with Django test client...")
    
    # Create a test client (handles sessions and cookies automatically)
    client = Client()
    
    # Get a food item
    food = Foods.objects.first()
    print(f"Using food: {food.title}")
    
    # First, visit the cart page to establish a session
    response = client.get('/cart/')
    print(f"Initial cart GET: {response.status_code}")
    
    # Get the session and add an item manually
    session = client.session
    print(f"Session key: {session.session_key}")
    
    # Create cart with the session key
    cart, created = Cart.objects.get_or_create(session_key=session.session_key)
    cart_item, item_created = CartItem.objects.get_or_create(
        cart=cart,
        food=food,
        defaults={'quantity': 3}
    )
    
    print(f"Cart item created: {item_created}, quantity: {cart_item.quantity}")
    
    # Now test the cart page with items
    response = client.get('/cart/')
    print(f"Cart GET with items: {response.status_code}")
    
    # Extract CSRF token from the response
    csrf_token = None
    if b'csrfmiddlewaretoken' in response.content:
        import re
        match = re.search(rb'name="csrfmiddlewaretoken" value="([^"]+)"', response.content)
        if match:
            csrf_token = match.group(1).decode()
            print(f"CSRF token found: {csrf_token[:20]}...")
    
    if csrf_token:
        # Test update quantity
        print("\n--- Testing UPDATE QUANTITY ---")
        update_data = {
            'csrfmiddlewaretoken': csrf_token,
            'cart_item_id': cart_item.id,
            'quantity': 5,
            'update_quantity': 'Update'
        }
        response = client.post('/cart/', update_data)
        print(f"Update quantity response: {response.status_code} -> {response.url if hasattr(response, 'url') else 'No redirect'}")
        
        # Check if quantity was updated
        cart_item.refresh_from_db()
        print(f"New quantity: {cart_item.quantity}")
        
        # Test remove item
        print("\n--- Testing REMOVE ITEM ---")
        remove_data = {
            'csrfmiddlewaretoken': csrf_token,
            'cart_item_id': cart_item.id,
            'remove_item': 'Remove'
        }
        response = client.post('/cart/', remove_data)
        print(f"Remove item response: {response.status_code} -> {response.url if hasattr(response, 'url') else 'No redirect'}")
        
        # Check if item was removed
        try:
            cart_item.refresh_from_db()
            print(f"Item still exists with quantity: {cart_item.quantity}")
        except CartItem.DoesNotExist:
            print("Item was successfully removed!")
    else:
        print("ERROR: Could not find CSRF token in response")

if __name__ == "__main__":
    test_cart_buttons()
