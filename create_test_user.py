#!/usr/bin/env python3
"""
Quick script to create a test user for favorites testing
"""
import os
import sys
import django

# Add the project directory to Python path
sys.path.append(r'c:\Users\ASUS\OneDrive\Desktop\RTMS1\Menu')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Menu.settings')
django.setup()

from django.contrib.auth.models import User
from main.models import Favorite, Foods

def create_test_user_and_favorites():
    """Create test user and some favorites for testing"""
    print("🧪 Creating Test User and Favorites")
    print("=" * 40)
    
    # Create test user
    try:
        user = User.objects.get(username='testuser')
        print(f"✅ User already exists: {user.username}")
    except User.DoesNotExist:
        user = User.objects.create_user(
            username='testuser',
            password='testpass123',
            email='test@example.com'
        )
        print(f"✅ Created new user: {user.username}")
    
    print(f"   User ID: {user.id}")
    print(f"   Username: testuser")
    print(f"   Password: testpass123")
    
    # Add some favorites
    foods = Foods.objects.all()[:3]  # Get first 3 food items
    favorites_created = 0
    
    for food in foods:
        favorite, created = Favorite.objects.get_or_create(
            user=user,
            food=food
        )
        if created:
            favorites_created += 1
            print(f"✅ Added {food.title} to favorites")
    
    total_favorites = Favorite.objects.filter(user=user).count()
    print(f"\n📊 Summary:")
    print(f"   Total favorites for testuser: {total_favorites}")
    print(f"   New favorites created: {favorites_created}")
    
    print(f"\n🚀 Ready to test!")
    print(f"   1. Go to http://127.0.0.1:8000/login/")
    print(f"   2. Login with username: testuser, password: testpass123")
    print(f"   3. Visit http://127.0.0.1:8000/favorites/")
    print(f"   4. Test add to cart and remove buttons")

if __name__ == "__main__":
    create_test_user_and_favorites()
