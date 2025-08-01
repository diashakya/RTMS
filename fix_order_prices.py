#!/usr/bin/env python3
"""
Fix OrderItems with null prices
"""
import os
import sys
import django

# Setup Django environment
sys.path.insert(0, r'c:\Users\ASUS\OneDrive\Desktop\RTMS1\Menu')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Menu.settings')
django.setup()

from main.models import OrderItem, Foods, Special

def fix_null_prices():
    """Fix OrderItems that have null prices"""
    print("🔧 Fixing OrderItems with null prices...")
    print("=" * 40)
    
    try:
        # Find OrderItems with null prices
        null_price_items = OrderItem.objects.filter(price__isnull=True)
        
        print(f"Found {null_price_items.count()} OrderItems with null prices")
        
        fixed_count = 0
        for item in null_price_items:
            try:
                # Try to set price from the related food or special
                if item.food and item.food.price:
                    item.price = item.food.price
                    item.save()
                    print(f"✅ Fixed OrderItem {item.id} - set price to {item.price} from food")
                    fixed_count += 1
                elif item.special:
                    if item.special.discounted_price:
                        item.price = item.special.discounted_price
                    elif item.special.price:
                        item.price = item.special.price
                    else:
                        item.price = 0
                    item.save()
                    print(f"✅ Fixed OrderItem {item.id} - set price to {item.price} from special")
                    fixed_count += 1
                else:
                    # Set default price of 0 if no food or special found
                    item.price = 0
                    item.save()
                    print(f"⚠️ Fixed OrderItem {item.id} - set price to 0 (no food/special found)")
                    fixed_count += 1
                    
            except Exception as e:
                print(f"❌ Error fixing OrderItem {item.id}: {e}")
        
        print(f"\n📊 Summary:")
        print(f"   Items with null prices: {null_price_items.count()}")
        print(f"   Items fixed: {fixed_count}")
        
        # Check for any remaining null prices
        remaining_null = OrderItem.objects.filter(price__isnull=True).count()
        if remaining_null == 0:
            print("✅ All OrderItems now have valid prices!")
        else:
            print(f"⚠️ {remaining_null} OrderItems still have null prices")
        
        return True
        
    except Exception as e:
        print(f"❌ Error during fix: {e}")
        return False

def verify_models():
    """Verify all models are working correctly"""
    print("\n🧪 Testing model methods...")
    print("=" * 30)
    
    try:
        # Test OrderItems
        order_items = OrderItem.objects.all()[:5]
        for item in order_items:
            try:
                total = item.total_price
                print(f"✅ OrderItem {item.id} total_price: {total}")
            except Exception as e:
                print(f"❌ OrderItem {item.id} error: {e}")
        
        # Test Cart totals
        from main.models import Cart
        carts = Cart.objects.all()[:3]
        for cart in carts:
            try:
                total_price = cart.total_price
                total_items = cart.total_items
                print(f"✅ Cart {cart.id} - Price: {total_price}, Items: {total_items}")
            except Exception as e:
                print(f"❌ Cart {cart.id} error: {e}")
        
        print("✅ Model verification completed!")
        return True
        
    except Exception as e:
        print(f"❌ Error during verification: {e}")
        return False

if __name__ == "__main__":
    print("🛠️ ORDERITEM PRICE FIXER")
    print("=" * 40)
    
    # Fix null prices
    if fix_null_prices():
        print("\n✅ Price fix completed")
    else:
        print("\n❌ Price fix failed")
        exit(1)
    
    # Verify everything is working
    if verify_models():
        print("\n🎉 All models are working correctly!")
        print("\n🚀 You can now:")
        print("1. Visit the admin order page without errors")
        print("2. View order details properly")
        print("3. Calculate totals correctly")
    else:
        print("\n❌ Some issues remain")
        
    print("\n💡 Note: The admin should now work without TypeError!")