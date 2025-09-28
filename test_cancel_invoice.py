import requests
import json

def test_cancel_invoice():
    """Test the cancel invoice API endpoint"""
    # Use a valid token from our previous tests
    token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjo3LCJyb2xlIjoiQWRtaW4iLCJleHAiOjE3NTkxNTExMTR9.uFLQhd-lGpoksXhSdjLo5W7oP8xkbgeaO5IrhQ9SMSM"
    
    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json'
    }
    
    # Try to cancel the invoice we just created (invoice_id: 11)
    try:
        response = requests.put('http://localhost:5001/api/sales/11/cancel', headers=headers)
        
        print(f"Cancel Response Status: {response.status_code}")
        
        if response.status_code == 200:
            print("Invoice cancelled successfully!")
            print("Response data:")
            print(json.dumps(response.json(), indent=2))
        else:
            print(f"Error cancelling invoice: {response.status_code}")
            print(f"Response text: {response.text}")
            
    except Exception as e:
        print(f"Exception: {e}")

if __name__ == "__main__":
    test_cancel_invoice()