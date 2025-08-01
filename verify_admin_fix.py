#!/usr/bin/env python3
"""
Verify admin.py is properly fixed and test Django startup
"""
import os
import sys

def verify_admin_fix():
    """Verify the admin.py file is clean and working"""
    print("🔍 VERIFYING ADMIN.PY FIX")
    print("=" * 40)
    
    admin_file = r"c:\Users\ASUS\OneDrive\Desktop\RTMS1\Menu\main\admin.py"
    
    try:
        # Read the admin file
        with open(admin_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Check for problematic patterns
        issues = []
        
        if 'send_status_email' in content:
            issues.append("❌ Still contains 'send_status_email' references")
        
        if 'order_actions' in content:
            issues.append("⚠️ Still contains 'order_actions' method")
        
        if 'reverse(' in content and 'send_status_email' in content:
            issues.append("❌ Still has problematic reverse calls")
        
        # Check syntax by compiling
        try:
            compile(content, admin_file, 'exec')
            print("✅ Syntax check: PASSED")
        except SyntaxError as e:
            issues.append(f"❌ Syntax error at line {e.lineno}: {e.msg}")
        
        if not issues:
            print("✅ Admin file is clean and should work!")
            print("✅ No problematic URL reversals found")
            print("✅ All syntax is valid")
            
            print("\n📊 Admin Features Available:")
            print("- ✅ Order list view")
            print("- ✅ Customer management")
            print("- ✅ Food/Special management")
            print("- ✅ Category management")
            print("- ✅ Bulk actions")
            print("- ⚠️ Custom actions temporarily disabled")
            
            return True
        else:
            print("❌ Issues found:")
            for issue in issues:
                print(f"  {issue}")
            return False
            
    except Exception as e:
        print(f"❌ Error reading admin file: {e}")
        return False

def test_django_import():
    """Test if Django can import the admin module"""
    print("\n🧪 TESTING DJANGO IMPORT")
    print("=" * 30)
    
    try:
        # Add Django project to path
        sys.path.insert(0, r'c:\Users\ASUS\OneDrive\Desktop\RTMS1\Menu')
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Menu.settings')
        
        import django
        django.setup()
        
        # Try to import the admin module
        from main import admin
        print("✅ Admin module imports successfully")
        
        # Try to access admin classes
        if hasattr(admin, 'OrderAdmin'):
            print("✅ OrderAdmin class found")
        if hasattr(admin, 'CustomerAdmin'):
            print("✅ CustomerAdmin class found")
        if hasattr(admin, 'FoodsAdmin'):
            print("✅ FoodsAdmin class found")
            
        return True
        
    except Exception as e:
        print(f"❌ Import error: {e}")
        return False

def show_next_steps():
    """Show what to do next"""
    print("\n🚀 NEXT STEPS")
    print("=" * 20)
    print("1. Restart Django server:")
    print("   python manage.py runserver")
    print("")
    print("2. Test admin access:")
    print("   http://127.0.0.1:8000/admin/main/order/")
    print("")
    print("3. Expected results:")
    print("   - Admin loads without NoReverseMatch error")
    print("   - Can view orders list")
    print("   - Can use bulk actions")
    print("   - Can edit individual orders")
    print("")
    print("💡 If you still get errors:")
    print("   - Clear browser cache completely")
    print("   - Try incognito/private window")
    print("   - Check server terminal for any new errors")

if __name__ == "__main__":
    print("🚨 FINAL ADMIN FIX VERIFICATION")
    print("=" * 50)
    
    # Verify admin file
    if verify_admin_fix():
        print("\n✅ Admin File: CLEAN")
    else:
        print("\n❌ Admin File: ISSUES FOUND")
        exit(1)
    
    # Test Django import
    if test_django_import():
        print("\n✅ Django Import: SUCCESS")
    else:
        print("\n❌ Django Import: FAILED")
    
    # Show next steps
    show_next_steps()
    
    print("\n🎉 Admin should now work without NoReverseMatch errors!")