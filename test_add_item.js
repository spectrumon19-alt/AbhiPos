// test_add_item.js - Test script to verify Add Item button functionality

// This script will simulate the actions needed to test the Add Item button
console.log("Testing Add Item button functionality...");

// Wait for the page to load
window.addEventListener('DOMContentLoaded', function() {
    console.log("Page loaded, checking for required elements...");
    
    // Check if required elements exist
    const productSearchInput = document.getElementById('product-search-input');
    const addItemBtn = document.getElementById('add-item-btn');
    const invoiceItemsBody = document.getElementById('invoice-items-body');
    
    if (!productSearchInput || !addItemBtn || !invoiceItemsBody) {
        console.error("Missing required elements on the page");
        return;
    }
    
    console.log("All required elements found");
    
    // Simulate selecting a product
    // In a real test, we would need to mock the API response
    window.currentSelectedProduct = {
        product_id: 1,
        name: "Test Product",
        pack_size: "1 kg",
        gst_rate: 18.00,
        selling_rate: 100.00
    };
    
    console.log("Simulated product selection:", window.currentSelectedProduct);
    
    // Simulate clicking the Add Item button
    console.log("Simulating Add Item button click...");
    addItemBtn.click();
    
    // Check if the item was added to the invoice
    setTimeout(() => {
        const rows = invoiceItemsBody.querySelectorAll('tr');
        if (rows.length > 0) {
            console.log("SUCCESS: Item was added to the invoice!");
            console.log(`Found ${rows.length} item(s) in the invoice`);
        } else {
            console.error("FAILURE: No items found in the invoice");
        }
    }, 100);
});