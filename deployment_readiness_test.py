#!/usr/bin/env python3
"""
Comprehensive Deployment Readiness Test for POS System
This script tests all critical components of the POS system to ensure it's ready for deployment.
"""

import requests
import json
import time

# Test configuration
BASE_URL = 'http://localhost:5001'
ADMIN_TOKEN = None
CASHIER_TOKEN = None
HEADERS_ADMIN = {'Authorization': 'Bearer ', 'Content-Type': 'application/json'}
HEADERS_CASHIER = {'Authorization': 'Bearer ', 'Content-Type': 'application/json'}

def login_users():
    """Login to get fresh tokens"""
    global ADMIN_TOKEN, CASHIER_TOKEN, HEADERS_ADMIN, HEADERS_CASHIER
    
    print("Logging in users to get fresh tokens...")
    
    # Login admin
    admin_login_data = {
        "username": "admin",
        "password": "admin123"
    }
    
    try:
        response = requests.post(f'{BASE_URL}/api/login', json=admin_login_data)
        if response.status_code == 200:
            admin_data = response.json()
            ADMIN_TOKEN = admin_data['token']
            HEADERS_ADMIN = {'Authorization': f'Bearer {ADMIN_TOKEN}', 'Content-Type': 'application/json'}
            print("  ✓ Admin login successful")
        else:
            print(f"  ✗ Admin login failed: {response.status_code}")
            return False
            
        # Login cashier
        cashier_login_data = {
            "username": "cashier",
            "password": "cashier123"
        }
        
        response = requests.post(f'{BASE_URL}/api/login', json=cashier_login_data)
        if response.status_code == 200:
            cashier_data = response.json()
            CASHIER_TOKEN = cashier_data['token']
            HEADERS_CASHIER = {'Authorization': f'Bearer {CASHIER_TOKEN}', 'Content-Type': 'application/json'}
            print("  ✓ Cashier login successful")
        else:
            print(f"  ✗ Cashier login failed: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"  ✗ Login failed: {e}")
        return False
        
    return True

def test_auth():
    """Test authentication endpoints"""
    print("Testing Authentication...")
    
    # Test user info
    try:
        response = requests.get(f'{BASE_URL}/api/users/me', headers=HEADERS_ADMIN)
        if response.status_code == 200:
            print("  ✓ Admin authentication successful")
        else:
            print(f"  ✗ Admin authentication failed: {response.status_code}")
            return False
            
        response = requests.get(f'{BASE_URL}/api/users/me', headers=HEADERS_CASHIER)
        if response.status_code == 200:
            print("  ✓ Cashier authentication successful")
        else:
            print(f"  ✗ Cashier authentication failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"  ✗ Authentication test failed: {e}")
        return False
        
    return True

def test_products():
    """Test products endpoints"""
    print("Testing Products...")
    
    try:
        # Test get all products
        response = requests.get(f'{BASE_URL}/api/products', headers=HEADERS_ADMIN)
        if response.status_code == 200:
            products = response.json()
            print(f"  ✓ Retrieved {len(products)} products")
        else:
            print(f"  ✗ Failed to retrieve products: {response.status_code}")
            return False
            
        # Test search products
        response = requests.get(f'{BASE_URL}/api/products?q=Product', headers=HEADERS_ADMIN)
        if response.status_code == 200:
            products = response.json()
            print(f"  ✓ Product search returned {len(products)} results")
        else:
            print(f"  ✗ Product search failed: {response.status_code}")
            return False
            
        # Test create product (admin only)
        product_data = {
            "name": f"Test Product {int(time.time())}",
            "sku": f"TEST-{int(time.time())}",
            "pack_size": "1 piece",
            "gst_rate": 18.00,
            "purchase_rate": 50.00,
            "selling_rate": 75.00,
            "initial_stock": 10
        }
        
        response = requests.post(f'{BASE_URL}/api/products', headers=HEADERS_ADMIN, json=product_data)
        if response.status_code == 201:
            product = response.json()
            print(f"  ✓ Created test product: {product['name']}")
            return product['product_id']  # Return product ID for cleanup
        else:
            print(f"  ✗ Failed to create product: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"  ✗ Products test failed: {e}")
        return False

def test_inventory():
    """Test inventory endpoints"""
    print("Testing Inventory...")
    
    try:
        # Test get inventory
        response = requests.get(f'{BASE_URL}/api/inventory', headers=HEADERS_ADMIN)
        if response.status_code == 200:
            inventory = response.json()
            print(f"  ✓ Retrieved inventory data for {len(inventory)} products")
        else:
            print(f"  ✗ Failed to retrieve inventory: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"  ✗ Inventory test failed: {e}")
        return False
        
    return True

def test_sales():
    """Test sales endpoints"""
    print("Testing Sales...")
    
    try:
        # Get products to use for sale
        response = requests.get(f'{BASE_URL}/api/products', headers=HEADERS_CASHIER)
        if response.status_code != 200:
            print(f"  ✗ Failed to get products for sale: {response.status_code}")
            return False
            
        products = response.json()
        if len(products) == 0:
            print("  ✗ No products available for sale")
            return False
            
        # Create a test sale
        invoice_data = {
            "invoice_number": f"INV-TEST-{int(time.time())}",
            "customer_name": "Test Customer",
            "customer_contact": "1234567890",
            "mode_of_payment": "Cash",
            "items": [
                {
                    "product_id": products[0]['product_id'],
                    "quantity": 1
                }
            ]
        }
        
        response = requests.post(f'{BASE_URL}/api/sales', headers=HEADERS_CASHIER, json=invoice_data)
        if response.status_code == 201:
            invoice = response.json()
            print(f"  ✓ Created test sale: {invoice['invoice_number']}")
            return invoice['invoice_id']  # Return invoice ID for cancellation test
        else:
            print(f"  ✗ Failed to create sale: {response.status_code}")
            print(f"  Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"  ✗ Sales test failed: {e}")
        return False

def test_admin_functions():
    """Test admin-only functions"""
    print("Testing Admin Functions...")
    
    try:
        # Test get users (admin only)
        response = requests.get(f'{BASE_URL}/api/admin/users', headers=HEADERS_ADMIN)
        if response.status_code == 200:
            users = response.json()
            print(f"  ✓ Retrieved {len(users)} users")
        else:
            print(f"  ✗ Failed to retrieve users: {response.status_code}")
            return False
            
        # Test get invoices (admin only)
        response = requests.get(f'{BASE_URL}/api/admin/invoices', headers=HEADERS_ADMIN)
        if response.status_code == 200:
            invoices = response.json()
            print(f"  ✓ Retrieved {len(invoices)} invoices")
        else:
            print(f"  ✗ Failed to retrieve invoices: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"  ✗ Admin functions test failed: {e}")
        return False
        
    return True

def test_frontend_access():
    """Test frontend page access"""
    print("Testing Frontend Access...")
    
    pages = [
        ('Dashboard', '/dashboard.html'),
        ('Sales', '/index.html'),
        ('Purchase', '/purchase.html'),
        ('Inventory', '/inventory.html'),
        ('Reports', '/reports.html'),
        ('Admin', '/admin.html')
    ]
    
    try:
        for name, path in pages:
            response = requests.get(f'{BASE_URL}{path}')
            if response.status_code == 200:
                print(f"  ✓ {name} page accessible")
            else:
                print(f"  ✗ {name} page not accessible: {response.status_code}")
                return False
                
    except Exception as e:
        print(f"  ✗ Frontend access test failed: {e}")
        return False
        
    return True

def cleanup_test_data(product_id=None, invoice_id=None):
    """Clean up test data"""
    print("Cleaning up test data...")
    
    try:
        if product_id:
            response = requests.delete(f'{BASE_URL}/api/products/{product_id}', headers=HEADERS_ADMIN)
            if response.status_code == 200:
                print(f"  ✓ Cleaned up test product {product_id}")
            else:
                print(f"  - Could not clean up test product {product_id}: {response.status_code}")
                
        # Note: We don't delete invoices as they're meant to be permanent records
        # In a real deployment, we might want to cancel test invoices instead
        
    except Exception as e:
        print(f"  - Cleanup failed: {e}")

def main():
    """Main test function"""
    print("POS System Deployment Readiness Test")
    print("=" * 50)
    
    # Track what we need to clean up
    test_product_id = None
    test_invoice_id = None
    
    try:
        # Login to get fresh tokens
        login_ok = login_users()
        if not login_ok:
            print("\n❌ Login failed. System not ready for deployment.")
            return False
        
        # Run all tests
        auth_ok = test_auth()
        if not auth_ok:
            print("\n❌ Authentication failed. System not ready for deployment.")
            return False
            
        frontend_ok = test_frontend_access()
        if not frontend_ok:
            print("\n❌ Frontend access failed. System not ready for deployment.")
            return False
            
        products_ok = test_products()
        if products_ok:
            test_product_id = products_ok  # Store product ID for cleanup
        else:
            print("\n❌ Products module has issues. System not ready for deployment.")
            return False
            
        inventory_ok = test_inventory()
        if not inventory_ok:
            print("\n❌ Inventory module has issues. System not ready for deployment.")
            return False
            
        sales_ok = test_sales()
        if sales_ok:
            test_invoice_id = sales_ok  # Store invoice ID
        else:
            print("\n❌ Sales module has issues. System not ready for deployment.")
            return False
            
        admin_ok = test_admin_functions()
        if not admin_ok:
            print("\n❌ Admin functions have issues. System not ready for deployment.")
            return False
            
        # If we get here, all tests passed
        print("\n" + "=" * 50)
        print("✅ ALL TESTS PASSED!")
        print("✅ POS System is ready for deployment!")
        print("=" * 50)
        return True
        
    except Exception as e:
        print(f"\n❌ Unexpected error during testing: {e}")
        return False
        
    finally:
        # Clean up test data
        cleanup_test_data(test_product_id, test_invoice_id)

if __name__ == "__main__":
    main()