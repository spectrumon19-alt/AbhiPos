import requests
import json

def test_invoice_structure():
    """Test the actual invoice structure returned by the API"""
    # Use a valid token
    token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjo3LCJyb2xlIjoiQWRtaW4iLCJleHAiOjE3NTkxNTExMTR9.uFLQhd-lGpoksXhSdjLo5W7oP8xkbgeaO5IrhQ9SMSM"
    
    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json'
    }
    
    # Create a test invoice to examine its structure
    invoice_data = {
        "invoice_number": "INV-TEST-" + str(int(time.time())),
        "customer_name": "Test Customer",
        "customer_contact": "1234567890",
        "mode_of_payment": "Cash",
        "items": [
            {
                "product_id": 1,
                "quantity": 2
            },
            {
                "product_id": 2,
                "quantity": 1
            }
        ]
    }
    
    try:
        print("Creating test invoice...")
        response = requests.post('http://localhost:5001/api/sales', headers=headers, json=invoice_data)
        
        if response.status_code == 201:
            invoice = response.json()
            print("Invoice created successfully!")
            print("\nInvoice structure:")
            print(json.dumps(invoice, indent=2, default=str))
            
            print("\nItems data type:", type(invoice.get('items')))
            print("Items content:", invoice.get('items'))
            
            if invoice.get('items'):
                if isinstance(invoice['items'], list):
                    print(f"Items is a list with {len(invoice['items'])} elements")
                    for i, item in enumerate(invoice['items']):
                        print(f"  Item {i+1}: {type(item)} - {item}")
                elif isinstance(invoice['items'], str):
                    print("Items is a string, attempting to parse as JSON...")
                    try:
                        parsed_items = json.loads(invoice['items'])
                        print(f"Parsed items: {parsed_items}")
                    except json.JSONDecodeError as e:
                        print(f"Failed to parse items as JSON: {e}")
        else:
            print(f"Failed to create invoice: {response.status_code}")
            print(response.text)
            
    except Exception as e:
        print(f"Exception: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    import time
    test_invoice_structure()