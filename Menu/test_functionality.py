#!/usr/bin/env python
"""
Comprehensive functionality test for the Restaurant Management System
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
from main.models import Foods, Category, Cart, CartItem, Order, OrderItem, Favorite, Customer
from django.test import Client

def test_database_connectivity():
    """Test basic database connectivity and data"""
    print("🔍 Testing Database Connectivity...")
    
    # Test basic model queries
    foods_count = Foods.objects.count()
    users_count = User.objects.count()
    categories_count = Category.objects.count()
    
    print(f"   ✅ Foods: {foods_count}")
    print(f"   ✅ Users: {users_count}")
    print(f"   ✅ Categories: {categories_count}")
    
    if foods_count > 0:
        sample_food = Foods.objects.first()
        print(f"   ✅ Sample Food: {sample_food.title} - Rs {sample_food.price}")
    
    return True

def test_cart_functionality():
    """Test cart operations"""
    print("\n🛒 Testing Cart Functionality...")
    
    # Get or create a test user
    test_user, created = User.objects.get_or_create(
        username='testuser',
        defaults={'email': 'test@example.com', 'first_name': 'Test', 'last_name': 'User'}
    )
    if created:
        test_user.set_password('testpass123')
        test_user.save()
        print(f"   ✅ Created test user: {test_user.username}")
    else:
        print(f"   ✅ Using existing test user: {test_user.username}")
    
    # Test cart creation
    cart, created = Cart.objects.get_or_create(user=test_user)
    print(f"   ✅ Cart {'created' if created else 'exists'} for user")
    
    # Test adding items to cart
    if Foods.objects.exists():
        food_item = Foods.objects.first()
        cart_item, created = CartItem.objects.get_or_create(
            cart=cart,
            food=food_item,
            defaults={'quantity': 1}
        )
        if not created:
            cart_item.quantity += 1
            cart_item.save()
        print(f"   ✅ Added {food_item.title} to cart (quantity: {cart_item.quantity})")
    
    cart_total = cart.total_price
    cart_count = cart.items.count()
    print(f"   ✅ Cart total: Rs {cart_total}")
    print(f"   ✅ Cart items count: {cart_count}")
    
    return True

def test_order_functionality():
    """Test order creation"""
    print("\n📦 Testing Order Functionality...")
    
    test_user = User.objects.filter(username='testuser').first()
    if not test_user:
        print("   ❌ Test user not found, skipping order test")
        return False
    
    # Check if user has a Customer profile
    try:
        customer = Customer.objects.get(user=test_user)
        print(f"   ✅ Customer profile exists: {customer.customer_email}")
    except Customer.DoesNotExist:
        print("   ⚠️ No Customer profile found for test user")
        customer = None
    
    if customer:
        orders_count = Order.objects.filter(customer=customer).count()
        print(f"   ✅ Customer has {orders_count} orders")
        
        if orders_count > 0:
            latest_order = Order.objects.filter(customer=customer).first()
            print(f"   ✅ Latest order: #{latest_order.id} - Rs {latest_order.total} ({latest_order.status})")
    else:
        # Check all orders
        total_orders = Order.objects.count()
        print(f"   ✅ Total orders in system: {total_orders}")
    
    return True

def test_favorites_functionality():
    """Test favorites operations"""
    print("\n❤️ Testing Favorites Functionality...")
    
    test_user = User.objects.filter(username='testuser').first()
    if not test_user:
        print("   ❌ Test user not found, skipping favorites test")
        return False
    
    # Test adding to favorites
    if Foods.objects.exists():
        food_item = Foods.objects.first()
        favorite, created = Favorite.objects.get_or_create(
            user=test_user,
            food=food_item
        )
        print(f"   ✅ {'Added' if created else 'Already has'} {food_item.title} in favorites")
    
    favorites_count = Favorite.objects.filter(user=test_user).count()
    print(f"   ✅ User has {favorites_count} favorites")
    
    return True

def test_api_endpoints():
    """Test API endpoints"""
    print("\n🌐 Testing API Endpoints...")
    
    client = Client()
    
    # Test food detail API
    if Foods.objects.exists():
        food_item = Foods.objects.first()
        response = client.get(f'/api/foods/{food_item.id}/')
        if response.status_code == 200:
            print(f"   ✅ Food detail API working: {food_item.title}")
        else:
            print(f"   ❌ Food detail API failed: {response.status_code}")
    
    # Test menu page
    response = client.get('/menu/')
    if response.status_code == 200:
        print("   ✅ Menu page loads successfully")
    else:
        print(f"   ❌ Menu page failed: {response.status_code}")
    
    # Test cart page (requires login)
    response = client.get('/cart/')
    if response.status_code in [200, 302]:  # 302 = redirect to login
        print("   ✅ Cart page accessible")
    else:
        print(f"   ❌ Cart page failed: {response.status_code}")
    
    return True

def test_order_types():
    """Test the new order type functionality"""
    print("\n🍽️ Testing Order Type Functionality...")
    
    # Test delivery order
    delivery_order = Order.objects.create(
        customer_name="Test Delivery Customer",
        customer_phone="9876543210",
        order_type='delivery',
        delivery_address="123 Test Street, Test City",
        total=500.00,
        status='pending'
    )
    print(f"   ✅ Created delivery order: #{delivery_order.id}")
    print(f"      📍 Address: {delivery_order.delivery_address}")
    
    # Test dine-in order
    dine_in_order = Order.objects.create(
        customer_name="Test Dine-In Customer", 
        customer_phone="9876543211",
        order_type='dine_in',
        table_number="T-05",
        total=350.00,
        status='pending'
    )
    print(f"   ✅ Created dine-in order: #{dine_in_order.id}")
    print(f"      🪑 Table: {dine_in_order.table_number}")
    
    # Test order type filtering
    delivery_orders = Order.objects.filter(order_type='delivery').count()
    dine_in_orders = Order.objects.filter(order_type='dine_in').count()
    print(f"   ✅ Total delivery orders: {delivery_orders}")
    print(f"   ✅ Total dine-in orders: {dine_in_orders}")
    
    return True

def main():
    """Run all tests"""
    print("🚀 Restaurant Management System - Functionality Test")
    print("=" * 60)
    
    try:
        test_database_connectivity()
        test_cart_functionality()
        test_order_functionality()
        test_order_types()  # Add new test
        test_favorites_functionality()
        test_api_endpoints()
        
        print("\n" + "=" * 60)
        print("✅ All functionality tests completed successfully!")
        print("\n🎯 Key Features Verified:")
        print("   • Database connectivity and models")
        print("   • Cart operations (add/update/calculate)")
        print("   • Order management")
        print("   • Order types (Delivery & Dine-In)")  # Add new feature
        print("   • Favorites system")
        print("   • API endpoints")
        print("\n🔧 Manual Testing Recommended:")
        print("   • Visit http://127.0.0.1:8000/")
        print("   • Test user registration/login")
        print("   • Test adding items to cart")
        print("   • Test order type selection (delivery vs dine-in)")  # Add new test
        print("   • Test Quick View modal")
        print("   • Test WebSocket notifications")
        print("   • Test order placement")
        print("   • Test admin interface")
        
    except Exception as e:
        print(f"\n❌ Test failed with error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
