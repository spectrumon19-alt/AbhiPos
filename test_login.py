import requests
import json

def test_login():
    """Test login to get fresh tokens"""
    print("Testing login to get fresh tokens...")
    
    # Test admin login
    admin_login_data = {
        "username": "admin",
        "password": "admin123"
    }
    
    try:
        response = requests.post('http://localhost:5001/api/login', json=admin_login_data)
        if response.status_code == 200:
            admin_data = response.json()
            print(f"Admin login successful. Token: {admin_data['token'][:20]}...")
            print(f"User: {admin_data['user']}")
        else:
            print(f"Admin login failed: {response.status_code}")
            print(response.text)
            
        # Test cashier login
        cashier_login_data = {
            "username": "cashier",
            "password": "cashier123"
        }
        
        response = requests.post('http://localhost:5001/api/login', json=cashier_login_data)
        if response.status_code == 200:
            cashier_data = response.json()
            print(f"Cashier login successful. Token: {cashier_data['token'][:20]}...")
            print(f"User: {cashier_data['user']}")
        else:
            print(f"Cashier login failed: {response.status_code}")
            print(response.text)
            
    except Exception as e:
        print(f"Login test failed: {e}")

if __name__ == "__main__":
    test_login()