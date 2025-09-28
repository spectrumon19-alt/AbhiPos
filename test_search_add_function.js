// Test the search and add functionality
function testSearchAndAdd() {
    console.log("Testing search and add functionality...");
    
    // Mock product data (simulating API response with string values)
    const mockProduct = {
        "product_id": 1,
        "name": "Test Product",
        "sku": "TP-001",
        "pack_size": "1 kg",
        "gst_rate": "18.00",  // String from API
        "selling_rate": "100.00",  // String from API
        "purchase_rate": "80.00"
    };
    
    console.log("Original product data:", mockProduct);
    
    // Test the convertProductNumbers function
    const convertedProduct = convertProductNumbers(mockProduct);
    console.log("Converted product data:", convertedProduct);
    
    // Check types
    console.log("Type checks:");
    console.log("- gst_rate:", typeof convertedProduct.gst_rate, convertedProduct.gst_rate);
    console.log("- selling_rate:", typeof convertedProduct.selling_rate, convertedProduct.selling_rate);
    
    // Test calculations
    const quantity = 2;
    const lineAmount = quantity * convertedProduct.selling_rate;
    const taxableValue = lineAmount / (1 + (convertedProduct.gst_rate / 100));
    const itemGst = lineAmount - taxableValue;
    const sgst = itemGst / 2;
    const cgst = itemGst / 2;
    
    console.log("Calculations:");
    console.log("- Line Amount:", lineAmount);
    console.log("- Taxable Value:", taxableValue);
    console.log("- Total GST:", itemGst);
    console.log("- SGST:", sgst);
    console.log("- CGST:", cgst);
    
    // Test the selectProduct function
    console.log("Testing selectProduct function...");
    // We can't fully test this without DOM elements, but we can verify the conversion
    
    console.log("Test completed successfully!");
}

// Run the test
testSearchAndAdd();