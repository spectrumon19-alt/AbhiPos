import requests

def test_frontend():
    """Test if frontend files are accessible"""
    base_url = 'http://127.0.0.1:5001'
    
    try:
        # Test the login page
        print("Testing login page...")
        response = requests.get(f'{base_url}/login.html', timeout=5)
        print(f"Login page status: {response.status_code}")
        
        # Test the main page
        print("Testing main page...")
        response = requests.get(f'{base_url}/index.html', timeout=5)
        print(f"Main page status: {response.status_code}")
        
        # Test CSS
        print("Testing CSS...")
        response = requests.get(f'{base_url}/styles.css', timeout=5)
        print(f"CSS status: {response.status_code}")
        
    except requests.exceptions.ConnectionError as e:
        print(f"Connection error: {e}")
    except requests.exceptions.Timeout as e:
        print(f"Timeout error: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")

if __name__ == "__main__":
    print("Testing frontend accessibility...")
    test_frontend()