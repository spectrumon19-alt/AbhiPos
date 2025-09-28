import requests
import json

def test_update_product():
    """Test the update product API endpoint"""
    # Use a valid admin token
    token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjo3LCJyb2xlIjoiQWRtaW4iLCJleHAiOjE3NTkxNTExMTR9.uFLQhd-lGpoksXhSdjLo5W7oP8xkbgeaO5IrhQ9SMSM"
    
    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json'
    }
    
    # First, get a product to update
    try:
        print("Getting products...")
        response = requests.get('http://localhost:5001/api/products', headers=headers)
        
        if response.status_code == 200:
            products = response.json()
            if products:
                product_id = products[0]['product_id']
                print(f"Found product ID: {product_id}")
                
                # Update the product
                update_data = {
                    "name": f"Updated Product {int(time.time())}",
                    "sku": f"UPD-{int(time.time())}",
                    "pack_size": "Updated Pack",
                    "gst_rate": 15.00,
                    "purchase_rate": 75.00,
                    "selling_rate": 95.00
                }
                
                print("Updating product...")
                response = requests.put(f'http://localhost:5001/api/products/{product_id}', 
                                      headers=headers, 
                                      json=update_data)
                
                if response.status_code == 200:
                    updated_product = response.json()
                    print("Product updated successfully!")
                    print(json.dumps(updated_product, indent=2, default=str))
                else:
                    print(f"Failed to update product: {response.status_code}")
                    print(response.text)
            else:
                print("No products found to update")
        else:
            print(f"Failed to get products: {response.status_code}")
            print(response.text)
            
    except Exception as e:
        print(f"Exception: {e}")

if __name__ == "__main__":
    import time
    test_update_product()