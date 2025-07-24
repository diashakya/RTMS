#!/usr/bin/env python3
"""
Create cart items for testing the web interface
"""
import os
import sys
import django

# Add the Menu directory to Python path
sys.path.append('c:/Users/ASUS/OneDrive/Desktop/RTMS1/Menu')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Menu.settings')

django.setup()

from main.models import Foods, Cart, CartItem

def create_test_cart_items():
    print("Creating test cart items for web testing...")
    
    # Get some foods
    foods = Foods.objects.all()[:3]  # Get first 3 foods
    
    # Create items for multiple session keys to increase chances of hit
    session_keys = [
        'test_session_key_123',
        'fsq7d8cll2jep6jlms10dggpptai9wui',  # From debug output
        'testsession123',
        'websession456'
    ]
    
    for session_key in session_keys:
        cart, created = Cart.objects.get_or_create(session_key=session_key)
        print(f"Cart for {session_key}: created={created}")
        
        for i, food in enumerate(foods, 1):
            cart_item, item_created = CartItem.objects.get_or_create(
                cart=cart,
                food=food,
                defaults={'quantity': i}
            )
            if item_created:
                print(f"  Added: {food.title} x {i}")
            else:
                print(f"  Exists: {food.title} x {cart_item.quantity}")

if __name__ == "__main__":
    create_test_cart_items()
