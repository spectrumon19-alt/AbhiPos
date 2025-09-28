import requests
import time

def test_server():
    """Test if the Flask server is responding"""
    try:
        # Wait a moment for the server to fully start
        time.sleep(2)
        
        # Try to access the root endpoint
        response = requests.get('http://127.0.0.1:5001', timeout=5)
        print(f"Server responded with status code: {response.status_code}")
        print(f"Response headers: {response.headers}")
        return True
    except requests.exceptions.ConnectionError as e:
        print(f"Connection error: {e}")
        return False
    except requests.exceptions.Timeout as e:
        print(f"Timeout error: {e}")
        return False
    except Exception as e:
        print(f"Unexpected error: {e}")
        return False

if __name__ == "__main__":
    print("Testing connection to Flask server...")
    success = test_server()
    if success:
        print("✓ Server is accessible!")
    else:
        print("✗ Server is not accessible.")