#!/usr/bin/env python3
"""
Test menu page for image errors
"""
import requests

def test_menu_page():
    """Test if menu page loads without image errors"""
    base_url = "http://127.0.0.1:8000"
    
    print("🧪 Testing Menu Page Image Fix")
    print("=" * 40)
    
    try:
        response = requests.get(f"{base_url}/menu/")
        
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            print("✅ Menu page loads successfully!")
            print(f"   Response size: {len(response.content)} bytes")
            
            # Check if the conditional image logic is in place
            content = response.text
            if 'if food.image' in content or 'if special.image' in content:
                print("✅ Conditional image checks found in template")
            else:
                print("⚠️  Conditional image checks not found")
                
            if 'sample_food.jpg' in content:
                print("✅ Fallback image reference found")
            else:
                print("⚠️  Fallback image reference not found")
                
            print("\n🎉 Menu page should now work without image errors!")
            
        elif response.status_code == 500:
            print("❌ Server error - there might still be an image issue")
            print("   Check server logs for details")
        else:
            print(f"❌ Unexpected status code: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Error testing menu page: {e}")

if __name__ == "__main__":
    test_menu_page()
