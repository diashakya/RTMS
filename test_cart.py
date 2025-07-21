#!/usr/bin/env python3
"""
Quick test script to check cart functionality
"""
import os
import sys
import django

# Add the Menu directory to Python path
sys.path.append('c:/Users/ASUS/OneDrive/Desktop/RTMS1/Menu')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Menu.settings')

django.setup()

from main.models import Foods, Cart, CartItem, Category, Customer
from django.contrib.auth.models import User

def test_cart_functionality():
    print("Testing cart functionality...")
    
    # Check if we have any foods
    foods = Foods.objects.all()
    print(f"Found {foods.count()} food items")
    
    if foods.exists():
        food = foods.first()
        print(f"Testing with food: {food.title}")
        
        # Create a test cart with session key
        cart, created = Cart.objects.get_or_create(
            session_key='test_session_key_123',
            defaults={}
        )
        print(f"Cart created: {created}")
        
        # Add an item to cart
        cart_item, item_created = CartItem.objects.get_or_create(
            cart=cart,
            food=food,
            defaults={'quantity': 2}
        )
        print(f"Cart item created: {item_created}")
        print(f"Cart item: {cart_item}")
        
        # List all cart items
        cart_items = CartItem.objects.filter(cart=cart)
        print(f"Cart items count: {cart_items.count()}")
        for item in cart_items:
            print(f"  - {item.item_name}: {item.quantity} x Rs {item.item_price} = Rs {item.total_price}")

if __name__ == "__main__":
    test_cart_functionality()
