import requests
import json

def test_fixed_invoice_structure():
    """Test the fixed invoice structure returned by the API"""
    # Use a valid token
    token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjo3LCJyb2xlIjoiQWRtaW4iLCJleHAiOjE3NTkxNTExMTR9.uFLQhd-lGpoksXhSdjLo5W7oP8xkbgeaO5IrhQ9SMSM"
    
    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json'
    }
    
    # Create a test invoice to examine its structure
    invoice_data = {
        "invoice_number": "INV-TEST-FIXED-" + str(int(time.time())),
        "customer_name": "Test Customer",
        "customer_contact": "1234567890",
        "mode_of_payment": "Cash",
        "items": [
            {
                "product_id": 1,
                "quantity": 2
            }
        ]
    }
    
    try:
        print("Creating test invoice with fixed structure...")
        response = requests.post('http://localhost:5001/api/sales', headers=headers, json=invoice_data)
        
        if response.status_code == 201:
            invoice = response.json()
            print("Invoice created successfully!")
            print("\nInvoice structure:")
            print(json.dumps(invoice, indent=2, default=str))
            
            print("\nChecking items for product names:")
            if invoice.get('items'):
                for i, item in enumerate(invoice['items']):
                    print(f"  Item {i+1}:")
                    print(f"    Name: {item.get('name', 'MISSING')}")
                    print(f"    Quantity: {item.get('quantity')}")
                    print(f"    Rate: {item.get('rate_at_sale')}")
                    print(f"    Amount: {item.get('total_line_amount')}")
                    
            print("\nTesting receipt generation with this data...")
            # Test if we can generate a receipt with this data
            total_amount = float(invoice['total_amount'])
            total_gst = float(invoice['total_gst'])
            print(f"Total Amount: ₹{total_amount:.2f}")
            print(f"Total GST: ₹{total_gst:.2f}")
            print(f"Number of items: {len(invoice.get('items', []))}")
            
        else:
            print(f"Failed to create invoice: {response.status_code}")
            print(response.text)
            
    except Exception as e:
        print(f"Exception: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    import time
    test_fixed_invoice_structure()