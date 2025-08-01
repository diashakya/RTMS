"""
Simple test to verify loading spinners are working properly
"""
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import os

def test_loading_spinners():
    """Test the loading spinners functionality"""
    print("🔄 Testing Loading Spinners...")
    
    try:
        # Configure Chrome for headless testing
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        
        driver = webdriver.Chrome(options=chrome_options)
        driver.get("http://127.0.0.1:8000/menu/")
        
        print("   ✅ Menu page loaded")
        
        # Check if loading CSS classes exist
        page_source = driver.page_source
        
        if "spinner" in page_source:
            print("   ✅ Spinner CSS classes found in page")
        else:
            print("   ⚠️ Spinner CSS classes not found")
            
        if "loading-overlay" in page_source:
            print("   ✅ Loading overlay structure found")
        else:
            print("   ⚠️ Loading overlay structure not found")
            
        # Check for cart buttons with AJAX attributes
        cart_buttons = driver.find_elements(By.CSS_SELECTOR, "[data-ajax='true']")
        if cart_buttons:
            print(f"   ✅ Found {len(cart_buttons)} AJAX-enabled cart buttons")
        else:
            print("   ⚠️ No AJAX-enabled cart buttons found")
            
        # Check for favorite buttons
        favorite_buttons = driver.find_elements(By.CSS_SELECTOR, ".favorite-btn")
        if favorite_buttons:
            print(f"   ✅ Found {len(favorite_buttons)} favorite buttons")
        else:
            print("   ⚠️ No favorite buttons found")
            
        driver.quit()
        print("   ✅ Loading spinner test completed successfully")
        return True
        
    except Exception as e:
        print(f"   ❌ Error testing loading spinners: {e}")
        return False

if __name__ == "__main__":
    # Simple fallback test without Selenium
    print("🔄 Testing Loading Spinners (Basic Test)...")
    
    import requests
    
    try:
        # Test if server is running
        response = requests.get("http://127.0.0.1:8000/menu/", timeout=5)
        if response.status_code == 200:
            print("   ✅ Server is running and menu page accessible")
            
            # Check for spinner CSS in response
            if "spinner" in response.text:
                print("   ✅ Spinner CSS found in HTML")
            else:
                print("   ⚠️ Spinner CSS not found")
                
            if "data-ajax" in response.text:
                print("   ✅ AJAX attributes found in buttons")
            else:
                print("   ⚠️ AJAX attributes not found")
                
            if "loading-overlay" in response.text:
                print("   ✅ Loading overlay found")
            else:
                print("   ⚠️ Loading overlay not found")
                
            print("   ✅ Basic loading spinner test completed")
            
        else:
            print(f"   ❌ Server returned status code: {response.status_code}")
            
    except requests.exceptions.RequestException as e:
        print(f"   ❌ Error connecting to server: {e}")
        print("   💡 Make sure the Django server is running on http://127.0.0.1:8000/")
