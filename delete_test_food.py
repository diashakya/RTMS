#!/usr/bin/env python3
"""
Quick script to delete test food items programmatically
"""
import os
import sys
import django

# Add the project directory to Python path
sys.path.append(r'c:\Users\ASUS\OneDrive\Desktop\RTMS1\Menu')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Menu.settings')
django.setup()

from main.models import Foods, Category

def delete_test_food():
    """Delete the test food item directly"""
    print("🗑️ Deleting Test Food Item")
    print("=" * 30)
    
    try:
        # Find and delete the test food
        test_food = Foods.objects.get(title="Test Food")
        print(f"✅ Found: {test_food.title}")
        print(f"   Price: Rs {test_food.price}")
        print(f"   Category: {test_food.category}")
        
        # Delete it
        test_food.delete()
        print(f"✅ Successfully deleted 'Test Food'")
        
    except Foods.DoesNotExist:
        print("❌ 'Test Food' not found - it may already be deleted")
    
    # Show remaining food count
    total_foods = Foods.objects.count()
    print(f"\n📊 Total food items remaining: {total_foods}")
    
    # List all foods
    print(f"\n📝 Current food items:")
    for food in Foods.objects.all()[:10]:  # Show first 10
        print(f"   - {food.title} (Rs {food.price})")

def list_foods():
    """List all food items"""
    print("📝 All Food Items:")
    print("=" * 30)
    
    foods = Foods.objects.all()
    for i, food in enumerate(foods, 1):
        print(f"{i:2d}. {food.title:<25} Rs {food.price:>6.2f} | {food.category}")
    
    print(f"\nTotal: {foods.count()} items")

if __name__ == "__main__":
    choice = input("Choose action:\n1. Delete 'Test Food'\n2. List all foods\nEnter 1 or 2: ")
    
    if choice == "1":
        delete_test_food()
    elif choice == "2":
        list_foods()
    else:
        print("Invalid choice")