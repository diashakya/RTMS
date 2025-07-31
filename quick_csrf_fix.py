#!/usr/bin/env python3
"""
Quick CSRF Token Fix & Test Script
"""
import os
import sys

def quick_csrf_fix():
    """Apply immediate CSRF fixes"""
    print("🔧 QUICK CSRF TOKEN FIX")
    print("=" * 40)
    
    # Solution options
    print("📋 Choose a solution:")
    print("1. Replace cart template with fixed version (RECOMMENDED)")
    print("2. Run CSRF token fixer script")
    print("3. Manual fix instructions")
    print("4. Test current cart functionality")
    
    choice = input("\nEnter choice (1-4): ").strip()
    
    if choice == "1":
        replace_cart_template()
    elif choice == "2":
        run_csrf_fixer()
    elif choice == "3":
        show_manual_instructions()
    elif choice == "4":
        test_cart_functionality()
    else:
        print("Invalid choice")

def replace_cart_template():
    """Replace cart template with fixed version"""
    import shutil
    
    source = r"c:\Users\ASUS\OneDrive\Desktop\RTMS1\Menu\main\templates\main\cart_fixed.html"
    dest = r"c:\Users\ASUS\OneDrive\Desktop\RTMS1\Menu\main\templates\main\cart.html"
    
    try:
        # Backup current template
        backup = dest + ".backup"
        if os.path.exists(dest):
            shutil.copy2(dest, backup)
            print(f"✅ Backed up current template to: {backup}")
        
        # Replace with fixed version
        if os.path.exists(source):
            shutil.copy2(source, dest)
            print(f"✅ Replaced cart template with fixed version")
            print("🎉 CSRF tokens should now work in the cart!")
        else:
            print(f"❌ Fixed template not found at: {source}")
    except Exception as e:
        print(f"❌ Error: {e}")

def run_csrf_fixer():
    """Run the CSRF fixer script"""
    try:
        import subprocess
        script_path = r"c:\Users\ASUS\OneDrive\Desktop\RTMS1\fix_cart_csrf.py"
        if os.path.exists(script_path):
            result = subprocess.run([sys.executable, script_path], capture_output=True, text=True)
            print(result.stdout)
            if result.stderr:
                print("Errors:", result.stderr)
        else:
            print(f"❌ Fixer script not found at: {script_path}")
    except Exception as e:
        print(f"❌ Error running fixer: {e}")

def show_manual_instructions():
    """Show manual fix instructions"""
    print("\n🛠️ MANUAL CSRF TOKEN FIX INSTRUCTIONS")
    print("=" * 50)
    print("""
1. Open: c:\\Users\\ASUS\\OneDrive\\Desktop\\RTMS1\\Menu\\main\\templates\\main\\cart.html

2. Find ALL forms that have method="post" and add {% csrf_token %} right after the opening <form> tag.

   BEFORE:
   <form method="post">
       <input type="hidden" name="update_quantity" value="1">
   
   AFTER:
   <form method="post">
       {% csrf_token %}
       <input type="hidden" name="update_quantity" value="1">

3. Look for these specific forms:
   - Update quantity form
   - Remove item form  
   - Checkout form

4. Save the file and refresh your browser

5. Test the update and remove buttons again

IMPORTANT: Every POST form MUST have {% csrf_token %} right after the opening form tag!
    """)

def test_cart_functionality():
    """Test cart functionality"""
    print("\n🧪 TESTING CART FUNCTIONALITY")
    print("=" * 40)
    
    print("To test your cart:")
    print("1. Start Django server: python manage.py runserver")
    print("2. Go to: http://127.0.0.1:8000/cart/")
    print("3. Add some items to cart first from menu")
    print("4. Try updating quantity")
    print("5. Try removing items")
    print("\nIf you still get CSRF errors:")
    print("- Check that {% csrf_token %} is in ALL POST forms")
    print("- Clear browser cookies")
    print("- Try in an incognito/private browser window")

if __name__ == "__main__":
    quick_csrf_fix()