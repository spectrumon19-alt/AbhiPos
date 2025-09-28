import requests
import json

def test_products_api():
    """Test the products API endpoint directly"""
    # Use a valid token from our previous tests
    token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjo3LCJyb2xlIjoiQWRtaW4iLCJleHAiOjE3NTkxNTExMTR9.uFLQhd-lGpoksXhSdjLo5W7oP8xkbgeaO5IrhQ9SMSM"
    
    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json'
    }
    
    try:
        print("Testing products API endpoint...")
        
        response = requests.get('http://localhost:5001/api/products', headers=headers)
        
        print(f"Response Status: {response.status_code}")
        print(f"Response Headers: {response.headers}")
        
        if response.status_code == 200:
            products = response.json()
            print(f"Successfully loaded {len(products)} products")
            print("First product:")
            if products:
                print(json.dumps(products[0], indent=2, default=str))
        else:
            print(f"Error loading products: {response.status_code}")
            print(f"Response text: {response.text}")
            
    except Exception as e:
        print(f"Exception: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_products_api()