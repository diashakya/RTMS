#!/usr/bin/env python3
"""
Script to fix CSRF token issues in cart template
"""
import os
import re

def fix_cart_template_csrf():
    """Add CSRF tokens to all forms in cart template"""
    cart_template_path = r"c:\Users\ASUS\OneDrive\Desktop\RTMS1\Menu\main\templates\main\cart.html"
    
    print("🔧 Fixing CSRF tokens in cart template...")
    
    try:
        # Read the current template
        with open(cart_template_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Pattern to find forms without CSRF tokens
        form_pattern = r'(<form[^>]*method=["\']post["\'][^>]*>)(?!\s*{%\s*csrf_token\s*%})'
        
        # Replace forms without CSRF tokens
        def add_csrf_token(match):
            form_tag = match.group(1)
            return f"{form_tag}\n                        {{% csrf_token %}}"
        
        # Apply the fix
        new_content = re.sub(form_pattern, add_csrf_token, content, flags=re.IGNORECASE)
        
        # Also ensure any missing CSRF tokens are added after form tags
        lines = new_content.split('\n')
        fixed_lines = []
        i = 0
        
        while i < len(lines):
            line = lines[i]
            fixed_lines.append(line)
            
            # If this line contains a POST form and next line doesn't have csrf_token
            if ('method="post"' in line.lower() or "method='post'" in line.lower()) and '<form' in line:
                # Check if next line has csrf_token
                if i + 1 < len(lines) and 'csrf_token' not in lines[i + 1]:
                    # Add CSRF token
                    indent = len(line) - len(line.lstrip())
                    csrf_line = ' ' * (indent + 4) + '{% csrf_token %}'
                    fixed_lines.append(csrf_line)
            
            i += 1
        
        final_content = '\n'.join(fixed_lines)
        
        # Write the fixed template
        with open(cart_template_path, 'w', encoding='utf-8') as f:
            f.write(final_content)
        
        print("✅ CSRF tokens added to cart template")
        
        # Count forms
        form_count = len(re.findall(r'<form[^>]*method=["\']post["\']', final_content, re.IGNORECASE))
        csrf_count = len(re.findall(r'{%\s*csrf_token\s*%}', final_content))
        
        print(f"📊 Summary:")
        print(f"   POST forms found: {form_count}")
        print(f"   CSRF tokens found: {csrf_count}")
        
        if csrf_count >= form_count:
            print("✅ All forms should now have CSRF tokens!")
        else:
            print("⚠️ Some forms might still be missing CSRF tokens")
        
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    fix_cart_template_csrf()