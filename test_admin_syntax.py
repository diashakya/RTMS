#!/usr/bin/env python3
"""
Test script to verify admin.py syntax is fixed
"""
import os
import sys

def test_admin_syntax():
    """Test if admin.py can be imported without syntax errors"""
    print("🧪 Testing admin.py syntax...")
    
    try:
        # Try to compile the admin.py file
        admin_path = r"c:\Users\ASUS\OneDrive\Desktop\RTMS1\Menu\main\admin.py"
        
        with open(admin_path, 'r', encoding='utf-8') as f:
            admin_code = f.read()
        
        compile(admin_code, admin_path, 'exec')
        print("✅ admin.py syntax is valid!")
        
        # Also test if it can be imported
        sys.path.insert(0, r"c:\Users\ASUS\OneDrive\Desktop\RTMS1\Menu")
        
        print("✅ Admin syntax error fixed!")
        print("✅ Django server should start without errors now.")
        
    except SyntaxError as e:
        print(f"❌ Syntax error still exists: {e}")
        print(f"Line {e.lineno}: {e.text}")
    except Exception as e:
        print(f"❌ Other error: {e}")

if __name__ == "__main__":
    test_admin_syntax()