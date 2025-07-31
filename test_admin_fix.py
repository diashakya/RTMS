#!/usr/bin/env python3
"""
Test script to verify the NoReverseMatch error is fixed
"""
import os
import sys
import django

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Menu.settings')
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'Menu'))
django.setup()

def test_admin_urls():
    """Test if admin URLs are working correctly"""
    from django.urls import reverse
    from django.test import RequestFactory
    from main.models import Order
    
    print("🧪 Testing Admin URL Resolution...")
    
    try:
        # Test if send_status_email URL can be reversed
        url = reverse('send_status_email', args=[1])
        print(f"✅ send_status_email URL resolved: {url}")
        
        # Test admin URLs
        admin_url = reverse('admin:main_order_changelist')
        print(f"✅ Admin changelist URL resolved: {admin_url}")
        
        print("\n🎉 All URLs resolved successfully!")
        print("The NoReverseMatch error should be fixed.")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        print("There may still be issues with URL configuration.")

if __name__ == "__main__":
    test_admin_urls()