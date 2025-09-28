import requests
import json

def test_api_endpoints():
    """Test the API endpoints"""
    base_url = 'http://127.0.0.1:5001'
    
    try:
        # Test the root endpoint
        print("Testing root endpoint...")
        response = requests.get(f'{base_url}/', timeout=5)
        print(f"Root endpoint status: {response.status_code}")
        
        # Test the login endpoint
        print("Testing login endpoint...")
        login_data = {
            "username": "admin",
            "password": "admin123"
        }
        response = requests.post(f'{base_url}/api/login', 
                               json=login_data, 
                               timeout=5)
        print(f"Login endpoint status: {response.status_code}")
        if response.status_code == 200:
            print("Login successful!")
            print(f"Response: {response.json()}")
        else:
            print(f"Login failed: {response.text}")
            
    except requests.exceptions.ConnectionError as e:
        print(f"Connection error: {e}")
    except requests.exceptions.Timeout as e:
        print(f"Timeout error: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")

if __name__ == "__main__":
    print("Testing API endpoints...")
    test_api_endpoints()