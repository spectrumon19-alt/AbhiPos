import requests
import json
import time

def test_sales_api():
    """Test the sales API endpoint directly"""
    # Use a valid token from our previous tests
    token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjo3LCJyb2xlIjoiQWRtaW4iLCJleHAiOjE3NTkxNTExMTR9.uFLQhd-lGpoksXhSdjLo5W7oP8xkbgeaO5IrhQ9SMSM"
    
    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json'
    }
    
    # Sample invoice data
    invoice_data = {
        "invoice_number": "INV-TEST-" + str(int(time.time())),
        "customer_name": "Test Customer",
        "customer_contact": "1234567890",
        "mode_of_payment": "Cash",
        "items": [
            {
                "product_id": 1,
                "quantity": 1
            }
        ]
    }
    
    try:
        print("Sending invoice data:")
        print(json.dumps(invoice_data, indent=2))
        
        response = requests.post('http://localhost:5001/api/sales', headers=headers, json=invoice_data)
        
        print(f"\nResponse Status: {response.status_code}")
        print(f"Response Headers: {response.headers}")
        
        if response.status_code == 201:
            print("Invoice saved successfully!")
            print("Response data:")
            print(json.dumps(response.json(), indent=2))
        else:
            print(f"Error saving invoice: {response.status_code}")
            print(f"Response text: {response.text}")
            
    except Exception as e:
        print(f"Exception: {e}")

if __name__ == "__main__":
    import time
    test_sales_api()