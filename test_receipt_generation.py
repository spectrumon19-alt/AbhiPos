import requests
import json

def test_receipt_generation():
    """Test the receipt generation process"""
    # Use a valid token
    token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjo3LCJyb2xlIjoiQWRtaW4iLCJleHAiOjE3NTkxNTExMTR9.uFLQhd-lGpoksXhSdjLo5W7oP8xkbgeaO5IrhQ9SMSM"
    
    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json'
    }
    
    # Create a test invoice
    invoice_data = {
        "invoice_number": "INV-TEST-RECEIPT-" + str(int(time.time())),
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
        print("Creating test invoice for receipt testing...")
        response = requests.post('http://localhost:5001/api/sales', headers=headers, json=invoice_data)
        
        if response.status_code == 201:
            invoice = response.json()
            print("Invoice created successfully!")
            print("\nInvoice structure:")
            print(json.dumps(invoice, indent=2, default=str))
            
            print("\nChecking items data:")
            items = invoice.get('items', [])
            print(f"Items type: {type(items)}")
            print(f"Items count: {len(items) if items else 0}")
            
            if items:
                for i, item in enumerate(items):
                    print(f"  Item {i+1}:")
                    print(f"    Name: {item.get('name', 'MISSING')}")
                    print(f"    Quantity: {item.get('quantity')}")
                    print(f"    Rate: {item.get('rate_at_sale')}")
                    print(f"    Amount: {item.get('total_line_amount')}")
            
            # Test receipt generation logic
            print("\nTesting receipt generation logic...")
            total_amount = float(invoice['total_amount'])
            total_gst = float(invoice['total_gst'])
            print(f"Total Amount: ₹{total_amount:.2f}")
            print(f"Total GST: ₹{total_gst:.2f}")
            
            # Check if we can properly iterate through items
            print("\nTesting item iteration:")
            try:
                for item in items:
                    print(f"Processing item: {item.get('name', 'Unknown')}")
            except Exception as e:
                print(f"Error iterating items: {e}")
                
        else:
            print(f"Failed to create invoice: {response.status_code}")
            print(response.text)
            
    except Exception as e:
        print(f"Exception: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    import time
    test_receipt_generation()