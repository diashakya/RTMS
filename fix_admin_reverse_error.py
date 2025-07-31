#!/usr/bin/env python3
"""
Quick script to fix the NoReverseMatch error in admin
"""
import shutil
import os

def fix_admin_reverse_error():
    """Replace broken admin.py with working version"""
    print("🔧 Fixing NoReverseMatch Error in Admin")
    print("=" * 40)
    
    source = r"c:\Users\ASUS\OneDrive\Desktop\RTMS1\Menu\main\admin_simple_fix.py"
    dest = r"c:\Users\ASUS\OneDrive\Desktop\RTMS1\Menu\main\admin.py"
    backup = dest + ".broken_backup"
    
    try:
        # Backup the broken file
        if os.path.exists(dest):
            shutil.copy2(dest, backup)
            print(f"✅ Backed up broken admin.py to: {backup}")
        
        # Replace with working version
        if os.path.exists(source):
            shutil.copy2(source, dest)
            print(f"✅ Replaced admin.py with working version")
            print("🎉 NoReverseMatch error should be fixed!")
        else:
            print(f"❌ Fixed admin file not found at: {source}")
            return False
        
        print("\n📋 What was fixed:")
        print("- Removed problematic order_actions method temporarily")
        print("- Kept all essential admin functionality")
        print("- Added enhanced actions for order management")
        print("- Maintained proper imports and structure")
        
        print("\n🚀 Next steps:")
        print("1. Restart Django server: python manage.py runserver")
        print("2. Visit: http://127.0.0.1:8000/admin/main/order/")
        print("3. Admin should now load without errors")
        
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def verify_urls():
    """Check if required URLs exist"""
    print("\n🔍 Checking URL Configuration...")
    
    urls_file = r"c:\Users\ASUS\OneDrive\Desktop\RTMS1\Menu\main\urls.py"
    
    try:
        with open(urls_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        if 'send_status_email' in content:
            print("✅ send_status_email URL pattern exists")
        else:
            print("⚠️ send_status_email URL pattern missing")
        
        if 'order_receipt' in content:
            print("✅ order_receipt URL pattern exists")
        else:
            print("⚠️ order_receipt URL pattern missing")
            
    except Exception as e:
        print(f"❌ Error checking URLs: {e}")

if __name__ == "__main__":
    print("🚨 FIXING NOREVERSEMATCH ERROR")
    print("=" * 50)
    
    # Fix the admin file
    if fix_admin_reverse_error():
        print("\n✅ Admin Fix: SUCCESS")
    else:
        print("\n❌ Admin Fix: FAILED")
    
    # Check URL configuration
    verify_urls()
    
    print("\n💡 If you still see NoReverseMatch errors:")
    print("- Check that Django server restarted properly")
    print("- Clear browser cache and try in incognito mode")
    print("- Verify all imports in views.py are working")
    print("- Check terminal for any other error messages")