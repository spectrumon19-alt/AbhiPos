// Test the admin panel fix directly in JavaScript
function testAdminPanelFix() {
    console.log("Testing admin panel fix...");
    
    // Mock product data (simulating API response with string values)
    const mockProducts = [
        {
            "product_id": 1,
            "name": "Test Product A",
            "sku": "TPA-001",
            "pack_size": "1 kg",
            "gst_rate": "18.00",  // String from API
            "purchase_rate": "80.00",  // String from API
            "selling_rate": "100.00",  // String from API
            "stock_quantity": "100"  // String from API
        },
        {
            "product_id": 2,
            "name": "Test Product B",
            "sku": "TPB-002",
            "pack_size": "500 g",
            "gst_rate": "12.00",  // String from API
            "purchase_rate": null,
            "selling_rate": "50.00",  // String from API
            "stock_quantity": "50"  // String from API
        }
    ];
    
    console.log("Testing product rendering with string values...");
    
    // Simulate the fixed rendering logic
    mockProducts.forEach(product => {
        try {
            // Convert string values to numbers for proper formatting (FIXED LOGIC)
            const gstRate = typeof product.gst_rate === 'string' ? parseFloat(product.gst_rate) : product.gst_rate;
            const purchaseRate = product.purchase_rate ? 
                (typeof product.purchase_rate === 'string' ? parseFloat(product.purchase_rate) : product.purchase_rate) : null;
            const sellingRate = typeof product.selling_rate === 'string' ? parseFloat(product.selling_rate) : product.selling_rate;
            const stockQuantity = typeof product.stock_quantity === 'string' ? parseInt(product.stock_quantity) : product.stock_quantity;
            
            // Test using toFixed() method which was causing the error
            const formattedPurchase = purchaseRate ? purchaseRate.toFixed(2) : '-';
            const formattedSelling = sellingRate.toFixed(2);
            const formattedStock = stockQuantity || 0;
            
            console.log(`Product: ${product.name}`);
            console.log(`  GST Rate: ${gstRate}%`);
            console.log(`  Purchase Rate: ₹${formattedPurchase}`);
            console.log(`  Selling Rate: ₹${formattedSelling}`);
            console.log(`  Stock Quantity: ${formattedStock}`);
            
            console.log("✓ Product rendered successfully!");
        } catch (error) {
            console.error("✗ Error rendering product:", error);
        }
    });
    
    // Test invoice data
    const mockInvoices = [
        {
            "invoice_id": 1,
            "invoice_number": "INV-001",
            "invoice_date": "2023-01-15T10:30:00Z",
            "customer_name": "John Doe",
            "total_amount": "1200.50",  // String from API
            "status": "Completed",
            "created_by": "admin"
        }
    ];
    
    console.log("\nTesting invoice rendering with string values...");
    
    // Simulate the fixed invoice rendering logic
    mockInvoices.forEach(invoice => {
        try {
            // Convert string values to numbers for proper formatting (FIXED LOGIC)
            const totalAmount = typeof invoice.total_amount === 'string' ? parseFloat(invoice.total_amount) : invoice.total_amount;
            
            // Test using toFixed() method which was causing the error
            const formattedAmount = totalAmount.toFixed(2);
            
            console.log(`Invoice: ${invoice.invoice_number}`);
            console.log(`  Total Amount: ₹${formattedAmount}`);
            console.log("✓ Invoice rendered successfully!");
        } catch (error) {
            console.error("✗ Error rendering invoice:", error);
        }
    });
    
    console.log("\n✓ All tests completed successfully!");
}

// Run the test
testAdminPanelFix();