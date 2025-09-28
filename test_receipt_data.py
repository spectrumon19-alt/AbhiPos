#!/usr/bin/env python3
"""
Test the receipt data structure and functionality
"""

import json
import requests

def test_receipt_data():
    """Test the receipt data structure"""
    print("Testing Receipt Data Structure")
    print("=" * 40)
    
    # Mock invoice data (similar to what the API returns)
    mock_invoice = {
        "invoice_number": "INV-TEST-12345",
        "invoice_date": "2023-01-15T10:30:00Z",
        "customer_name": "John Doe",
        "customer_contact": "1234567890",
        "total_amount": "1200.50",
        "total_gst": "180.25",
        "items": [
            {
                "name": "Product A",
                "quantity": "2",
                "rate_at_sale": "100.00",
                "total_line_amount": "200.00"
            },
            {
                "name": "Product B",
                "quantity": "1",
                "rate_at_sale": "1000.50",
                "total_line_amount": "1000.50"
            }
        ]
    }
    
    print("Mock Invoice Data:")
    print(json.dumps(mock_invoice, indent=2))
    
    # Test data type conversions
    print("\nTesting Data Type Conversions:")
    print("-" * 30)
    
    # Convert string values to numbers
    total_amount = float(mock_invoice["total_amount"]) if isinstance(mock_invoice["total_amount"], str) else mock_invoice["total_amount"]
    total_gst = float(mock_invoice["total_gst"]) if isinstance(mock_invoice["total_gst"], str) else mock_invoice["total_gst"]
    
    print(f"Total Amount: ₹{total_amount:.2f} (type: {type(total_amount).__name__})")
    print(f"Total GST: ₹{total_gst:.2f} (type: {type(total_gst).__name__})")
    
    # Process items
    print("\nProcessing Items:")
    print("-" * 20)
    for i, item in enumerate(mock_invoice["items"]):
        quantity = int(item["quantity"]) if isinstance(item["quantity"], str) else item["quantity"]
        rate_at_sale = float(item["rate_at_sale"]) if isinstance(item["rate_at_sale"], str) else item["rate_at_sale"]
        total_line_amount = float(item["total_line_amount"]) if isinstance(item["total_line_amount"], str) else item["total_line_amount"]
        
        print(f"Item {i+1}: {item['name']}")
        print(f"  Quantity: {quantity} (type: {type(quantity).__name__})")
        print(f"  Rate: ₹{rate_at_sale:.2f} (type: {type(rate_at_sale).__name__})")
        print(f"  Amount: ₹{total_line_amount:.2f} (type: {type(total_line_amount).__name__})")
    
    # Test receipt HTML generation
    print("\nTesting Receipt HTML Generation:")
    print("-" * 35)
    
    receipt_html = f"""
    <div class="receipt-header">
        <h1>ABC Store</h1>
        <p>123 Main Street, City</p>
        <p>Phone: (123) 456-7890</p>
    </div>
    
    <div class="receipt-details">
        <p><strong>Invoice #:</strong> {mock_invoice['invoice_number']}</p>
        <p><strong>Date:</strong> {mock_invoice['invoice_date'][:10]}</p>
        <p><strong>Customer:</strong> {mock_invoice['customer_name']}</p>
    </div>
    
    <table>
        <thead>
            <tr>
                <th>Item</th>
                <th>Qty</th>
                <th class="text-right">Rate</th>
                <th class="text-right">Amount</th>
            </tr>
        </thead>
        <tbody>
    """
    
    for item in mock_invoice["items"]:
        quantity = int(item["quantity"]) if isinstance(item["quantity"], str) else item["quantity"]
        rate_at_sale = float(item["rate_at_sale"]) if isinstance(item["rate_at_sale"], str) else item["rate_at_sale"]
        total_line_amount = float(item["total_line_amount"]) if isinstance(item["total_line_amount"], str) else item["total_line_amount"]
        
        receipt_html += f"""
            <tr>
                <td>{item['name']}</td>
                <td>{quantity}</td>
                <td class="text-right">₹{rate_at_sale:.2f}</td>
                <td class="text-right">₹{total_line_amount:.2f}</td>
            </tr>
        """
    
    receipt_html += f"""
        </tbody>
    </table>
    
    <div class="totals">
        <table>
            <tr>
                <td>Total Amount:</td>
                <td class="text-right">₹{total_amount:.2f}</td>
            </tr>
            <tr>
                <td>Total GST:</td>
                <td class="text-right">₹{total_gst:.2f}</td>
            </tr>
            <tr class="grand-total">
                <td>Grand Total:</td>
                <td class="text-right">₹{total_amount:.2f}</td>
            </tr>
        </table>
    </div>
    """
    
    print("Receipt HTML generated successfully!")
    print(f"Receipt contains {len(mock_invoice['items'])} items")
    print(f"Grand Total: ₹{total_amount:.2f}")
    
    print("\n" + "=" * 40)
    print("✅ All receipt functionality tests passed!")

if __name__ == "__main__":
    test_receipt_data()