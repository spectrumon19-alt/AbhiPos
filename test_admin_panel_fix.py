# Test the fixed admin panel logic in Python

# Mock product data (simulating API response with string values)
mock_products = [
    {
        "product_id": 1,
        "name": "Test Product A",
        "sku": "TPA-001",
        "pack_size": "1 kg",
        "gst_rate": "18.00",  # String from API
        "purchase_rate": "80.00",  # String from API
        "selling_rate": "100.00",  # String from API
        "stock_quantity": "100"  # String from API
    },
    {
        "product_id": 2,
        "name": "Test Product B",
        "sku": "TPB-002",
        "pack_size": "500 g",
        "gst_rate": "12.00",  # String from API
        "purchase_rate": None,
        "selling_rate": "50.00",  # String from API
        "stock_quantity": "50"  # String from API
    }
]

print("Testing product rendering with string values...")
print("=" * 50)

for product in mock_products:
    print(f"\nProduct: {product['name']}")
    
    # Convert string values to numbers for proper formatting (FIXED LOGIC)
    gst_rate = float(product['gst_rate']) if isinstance(product['gst_rate'], str) else product['gst_rate']
    purchase_rate = None
    if product['purchase_rate']:
        purchase_rate = float(product['purchase_rate']) if isinstance(product['purchase_rate'], str) else product['purchase_rate']
    selling_rate = float(product['selling_rate']) if isinstance(product['selling_rate'], str) else product['selling_rate']
    stock_quantity = int(product['stock_quantity']) if isinstance(product['stock_quantity'], str) else product['stock_quantity']
    
    print(f"  SKU: {product['sku'] or '-'}")
    print(f"  Pack Size: {product['pack_size'] or '-'}")
    print(f"  GST Rate: {gst_rate}%")
    print(f"  Purchase Rate: ₹{purchase_rate:.2f}" if purchase_rate else "  Purchase Rate: ₹-")
    print(f"  Selling Rate: ₹{selling_rate:.2f}")
    print(f"  Stock Quantity: {stock_quantity or 0}")

print("\n" + "=" * 50)
print("✓ All products rendered successfully with the fix!")

# Test invoice data
mock_invoices = [
    {
        "invoice_id": 1,
        "invoice_number": "INV-001",
        "invoice_date": "2023-01-15T10:30:00Z",
        "customer_name": "John Doe",
        "total_amount": "1200.50",  # String from API
        "status": "Completed",
        "created_by": "admin"
    }
]

print("\nTesting invoice rendering with string values...")
print("=" * 50)

for invoice in mock_invoices:
    print(f"\nInvoice: {invoice['invoice_number']}")
    
    # Convert string values to numbers for proper formatting (FIXED LOGIC)
    total_amount = float(invoice['total_amount']) if isinstance(invoice['total_amount'], str) else invoice['total_amount']
    
    print(f"  Date: {invoice['invoice_date']}")
    print(f"  Customer: {invoice['customer_name'] or '-'}")
    print(f"  Total Amount: ₹{total_amount:.2f}")
    print(f"  Status: {invoice['status']}")
    print(f"  Created By: {invoice['created_by']}")

print("\n" + "=" * 50)
print("✓ All invoices rendered successfully with the fix!")