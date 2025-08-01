#!/usr/bin/env python3
"""
Ensure Contact model is properly registered in admin
"""
import os
import sys

def ensure_contact_admin():
    """Ensure Contact model is registered in admin"""
    print("🔧 Ensuring Contact Admin Registration")
    print("=" * 40)
    
    admin_file = r"c:\Users\ASUS\OneDrive\Desktop\RTMS1\Menu\main\admin.py"
    
    try:
        # Read current admin.py
        with open(admin_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Check what's already there
        has_contact_import = 'Contact' in content and 'from .models import' in content
        has_contact_decorator = '@admin.register(Contact)' in content
        has_contact_function = 'admin.site.register(Contact' in content
        has_contact_admin_class = 'class ContactAdmin' in content
        
        print(f"Contact import: {'✅' if has_contact_import else '❌'}")
        print(f"@admin.register decorator: {'✅' if has_contact_decorator else '❌'}")
        print(f"admin.site.register function: {'✅' if has_contact_function else '❌'}")
        print(f"ContactAdmin class: {'✅' if has_contact_admin_class else '❌'}")
        
        # If everything is there, we're good
        if all([has_contact_import, has_contact_decorator, has_contact_admin_class]):
            print("✅ Contact admin is properly configured!")
            return True
        
        # If not, let's fix it
        modified = False
        
        # Fix import if missing
        if not has_contact_import:
            if 'from .models import' in content:
                # Add Contact to existing import
                content = content.replace(
                    'from .models import Special, Foods, Category, Favorite, Order, OrderItem, Customer, Cart, CartItem',
                    'from .models import Special, Foods, Category, Favorite, Order, OrderItem, Customer, Cart, CartItem, Contact'
                )
                modified = True
                print("✅ Added Contact to imports")
            else:
                # Add new import line
                content = "from .models import Contact\n" + content
                modified = True
                print("✅ Added Contact import")
        
        # Add registration at the end if missing
        if not has_contact_decorator and not has_contact_function:
            contact_admin_code = """
# Contact Admin Registration
@admin.register(Contact) 
class ContactAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'phone', 'submitted_at', 'is_read', 'message_preview')
    list_filter = ('is_read', 'submitted_at')
    search_fields = ('name', 'email', 'phone')
    readonly_fields = ('submitted_at',)
    list_editable = ('is_read',)
    ordering = ('-submitted_at',)
    
    def message_preview(self, obj):
        return obj.message[:50] + "..." if len(obj.message) > 50 else obj.message
    message_preview.short_description = "Message Preview"

"""
            # Add before the last lines
            lines = content.split('\n')
            insert_index = -1
            for i, line in enumerate(lines):
                if 'admin.site.site_header' in line:
                    insert_index = i
                    break
            
            if insert_index > 0:
                lines.insert(insert_index, contact_admin_code)
                content = '\n'.join(lines)
                modified = True
                print("✅ Added ContactAdmin class")
        
        # Write back if modified
        if modified:
            with open(admin_file, 'w', encoding='utf-8') as f:
                f.write(content)
            print("✅ Admin file updated")
        
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_admin_registration():
    """Test if admin registration works"""
    print("\n🧪 Testing Admin Registration")
    print("=" * 30)
    
    try:
        # Setup Django
        sys.path.insert(0, r'c:\Users\ASUS\OneDrive\Desktop\RTMS1\Menu')
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Menu.settings')
        
        import django
        django.setup()
        
        # Import models and admin
        from main.models import Contact
        from django.contrib import admin
        
        # Check if Contact is registered
        if Contact in admin.site._registry:
            print("✅ Contact model is registered in admin")
            admin_class = admin.site._registry[Contact]
            print(f"✅ Admin class: {admin_class.__class__.__name__}")
            return True
        else:
            print("❌ Contact model is NOT registered in admin")
            
            # Try to register it manually
            try:
                from main.admin import ContactAdmin
                admin.site.register(Contact, ContactAdmin)
                print("✅ Manually registered Contact admin")
                return True
            except Exception as e:
                print(f"❌ Failed to manually register: {e}")
                return False
        
    except Exception as e:
        print(f"❌ Error testing registration: {e}")
        return False

if __name__ == "__main__":
    print("🛠️ CONTACT ADMIN REGISTRATION FIXER")
    print("=" * 50)
    
    # Ensure admin is properly configured
    if ensure_contact_admin():
        print("\n✅ Admin configuration complete")
    else:
        print("\n❌ Failed to configure admin")
        exit(1)
    
    # Test the registration
    if test_admin_registration():
        print("\n🎉 Contact admin is working!")
        print("\n🚀 You can now:")
        print("1. Run: python manage.py makemigrations")
        print("2. Run: python manage.py migrate")
        print("3. Start server: python manage.py runserver") 
        print("4. Visit: http://127.0.0.1:8000/admin/main/contact/")
    else:
        print("\n❌ Registration test failed")
        print("Please check the error messages above.")