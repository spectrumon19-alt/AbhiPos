import requests
import json

def test_complete_system():
    """Test the complete POS system"""
    base_url = 'http://127.0.0.1:5001'
    
    try:
        print("=== Testing Complete POS System ===\n")
        
        # 1. Test frontend accessibility
        print("1. Testing frontend files...")
        response = requests.get(f'{base_url}/login.html', timeout=5)
        assert response.status_code == 200, "Login page not accessible"
        print("   ✓ Login page accessible")
        
        response = requests.get(f'{base_url}/index.html', timeout=5)
        assert response.status_code == 200, "Main page not accessible"
        print("   ✓ Main page accessible")
        
        response = requests.get(f'{base_url}/styles.css', timeout=5)
        assert response.status_code == 200, "CSS not accessible"
        print("   ✓ CSS accessible")
        
        # 2. Test API login
        print("\n2. Testing API login...")
        login_data = {
            "username": "admin",
            "password": "admin123"
        }
        response = requests.post(f'{base_url}/api/login', 
                               json=login_data, 
                               timeout=5)
        assert response.status_code == 200, "Login failed"
        login_result = response.json()
        token = login_result['token']
        print("   ✓ Login successful")
        print(f"   ✓ Token received: {token[:20]}...")
        
        # 3. Test protected API endpoint
        print("\n3. Testing protected API endpoint...")
        headers = {'Authorization': f'Bearer {token}'}
        response = requests.get(f'{base_url}/api/products', 
                              headers=headers, 
                              timeout=5)
        assert response.status_code == 200, "Products endpoint failed"
        products = response.json()
        print("   ✓ Products endpoint accessible")
        print(f"   ✓ Found {len(products)} products")
        
        # 4. Test inventory endpoint
        print("\n4. Testing inventory endpoint...")
        response = requests.get(f'{base_url}/api/inventory', 
                              headers=headers, 
                              timeout=5)
        assert response.status_code == 200, "Inventory endpoint failed"
        inventory = response.json()
        print("   ✓ Inventory endpoint accessible")
        print(f"   ✓ Found {len(inventory)} inventory items")
        
        print("\n=== All Tests Passed! ===")
        print("The POS system is working correctly.")
        print("You can now access the application at http://localhost:5001")
        
    except AssertionError as e:
        print(f"\n✗ Test failed: {e}")
    except requests.exceptions.ConnectionError as e:
        print(f"\n✗ Connection error: {e}")
        print("Make sure the Flask application is running on port 5001")
    except requests.exceptions.Timeout as e:
        print(f"\n✗ Timeout error: {e}")
    except Exception as e:
        print(f"\n✗ Unexpected error: {e}")

if __name__ == "__main__":
    test_complete_system()