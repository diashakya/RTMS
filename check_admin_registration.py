#!/usr/bin/env python3
"""
Check admin.py files and Contact model registration
"""
import os
import glob

def find_admin_files():
    """Find all admin.py files in the project"""
    print("🔍 Finding all admin.py files...")
    print("=" * 40)
    
    project_root = r"c:\Users\ASUS\OneDrive\Desktop\RTMS1"
    
    # Search for admin.py files
    admin_files = []
    for root, dirs, files in os.walk(project_root):
        for file in files:
            if file == 'admin.py' or file.startswith('admin') and file.endswith('.py'):
                admin_files.append(os.path.join(root, file))
    
    print(f"Found {len(admin_files)} admin files:")
    for i, file_path in enumerate(admin_files, 1):
        rel_path = os.path.relpath(file_path, project_root)
        print(f"{i}. {rel_path}")
        
        # Check if it contains Contact
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                if 'Contact' in content:
                    print(f"   ✅ Contains Contact references")
                else:
                    print(f"   ❌ No Contact references")
        except:
            print(f"   ❌ Error reading file")
    
    return admin_files

def check_main_admin():
    """Check the main admin.py file"""
    print("\n🔍 Checking main admin.py file...")
    print("=" * 35)
    
    main_admin = r"c:\Users\ASUS\OneDrive\Desktop\RTMS1\Menu\main\admin.py"
    
    if not os.path.exists(main_admin):
        print("❌ Main admin.py file not found!")
        return False
    
    try:
        with open(main_admin, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Check for Contact model import
        if 'from .models import' in content and 'Contact' in content:
            print("✅ Contact model imported")
        else:
            print("❌ Contact model NOT imported")
        
        # Check for Contact admin registration
        if '@admin.register(Contact)' in content:
            print("✅ Contact admin registered with decorator")
        elif 'admin.site.register(Contact' in content:
            print("✅ Contact admin registered with function")
        else:
            print("❌ Contact admin NOT registered")
        
        # Check for ContactAdmin class
        if 'class ContactAdmin' in content:
            print("✅ ContactAdmin class defined")
        else:
            print("❌ ContactAdmin class NOT defined")
        
        return True
        
    except Exception as e:
        print(f"❌ Error reading admin file: {e}")
        return False

def fix_admin_registration():
    """Fix admin registration if needed"""
    print("\n🔧 Checking admin registration...")
    print("=" * 35)
    
    main_admin = r"c:\Users\ASUS\OneDrive\Desktop\RTMS1\Menu\main\admin.py"
    
    try:
        with open(main_admin, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Check if Contact is in imports
        if 'Contact' not in content:
            print("⚠️ Need to add Contact to imports and registration")
            return False
        
        # Check if Contact admin is registered
        if '@admin.register(Contact)' in content or 'admin.site.register(Contact' in content:
            print("✅ Contact admin is properly registered")
            return True
        else:
            print("⚠️ Contact admin registration may be missing")
            return False
            
    except Exception as e:
        print(f"❌ Error checking admin: {e}")
        return False

def check_models():
    """Check if Contact model exists"""
    print("\n🔍 Checking Contact model...")
    print("=" * 30)
    
    models_file = r"c:\Users\ASUS\OneDrive\Desktop\RTMS1\Menu\main\models.py"
    
    if not os.path.exists(models_file):
        print("❌ models.py file not found!")
        return False
    
    try:
        with open(models_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        if 'class Contact' in content:
            print("✅ Contact model exists")
            
            # Check required fields
            required_fields = ['name', 'email', 'phone', 'message', 'submitted_at', 'is_read']
            for field in required_fields:
                if field in content:
                    print(f"✅ {field} field found")
                else:
                    print(f"❌ {field} field missing")
            
            return True
        else:
            print("❌ Contact model NOT found")
            return False
            
    except Exception as e:
        print(f"❌ Error reading models file: {e}")
        return False

def check_django_setup():
    """Check if Django can import the models and admin"""
    print("\n🧪 Testing Django imports...")
    print("=" * 30)
    
    try:
        import sys
        import os
        
        # Add Django project to path
        sys.path.insert(0, r'c:\Users\ASUS\OneDrive\Desktop\RTMS1\Menu')
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Menu.settings')
        
        import django
        django.setup()
        
        # Try to import Contact model
        try:
            from main.models import Contact
            print("✅ Contact model imports successfully")
        except ImportError as e:
            print(f"❌ Error importing Contact model: {e}")
            return False
        
        # Try to import admin
        try:
            from main import admin
            print("✅ Admin module imports successfully")
        except ImportError as e:
            print(f"❌ Error importing admin module: {e}")
            return False
        
        # Check if Contact is registered in admin
        from django.contrib import admin as django_admin
        if Contact in django_admin.site._registry:
            print("✅ Contact model is registered in admin site")
        else:
            print("❌ Contact model is NOT registered in admin site")
            return False
        
        return True
        
    except Exception as e:
        print(f"❌ Django setup error: {e}")
        return False

if __name__ == "__main__":
    print("🔍 ADMIN REGISTRATION CHECKER")
    print("=" * 50)
    
    # Find all admin files
    admin_files = find_admin_files()
    
    # Check main admin
    main_admin_ok = check_main_admin()
    
    # Check models
    models_ok = check_models()
    
    # Check admin registration
    admin_reg_ok = fix_admin_registration()
    
    # Test Django imports
    django_ok = check_django_setup()
    
    print("\n📊 SUMMARY")
    print("=" * 20)
    print(f"Admin files found: {len(admin_files)}")
    print(f"Main admin.py: {'✅' if main_admin_ok else '❌'}")
    print(f"Contact model: {'✅' if models_ok else '❌'}")
    print(f"Admin registration: {'✅' if admin_reg_ok else '❌'}")
    print(f"Django imports: {'✅' if django_ok else '❌'}")
    
    if all([main_admin_ok, models_ok, admin_reg_ok, django_ok]):
        print("\n🎉 Everything looks good!")
        print("Your Contact admin should be visible at:")
        print("http://127.0.0.1:8000/admin/main/contact/")
    else:
        print("\n⚠️ Some issues found. Check the details above.")
        
    print("\n🚀 Next steps:")
    print("1. Run: python manage.py makemigrations")
    print("2. Run: python manage.py migrate") 
    print("3. Start server: python manage.py runserver")
    print("4. Visit admin: http://127.0.0.1:8000/admin/")