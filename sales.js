// sales.js

// Global variables
let currentUser = null;
let invoiceItems = [];
let searchResults = [];
let currentSelectedProduct = null; // Move this to the top

// DOM Elements
let productSearchInput, searchResultsDiv, quantityInput, addItemBtn, invoiceItemsBody;
let customerNameInput, customerContactInput, totalAmountSpan, totalGstSpan, grandTotalSpan;
let savePrintBtn, clearBtn, logoutBtn, usernameSpan;

// Debug logging function
function debugLog(message, data = null) {
    console.log(`[POS DEBUG] ${message}`, data);
}

// Helper function to convert API string values to numbers
function convertProductNumbers(product) {
    return {
        ...product,
        gst_rate: parseFloat(product.gst_rate),
        selling_rate: parseFloat(product.selling_rate),
        purchase_rate: product.purchase_rate ? parseFloat(product.purchase_rate) : null
    };
}

// Initialize DOM elements
function initDOMElements() {
    debugLog("Initializing DOM elements");
    
    productSearchInput = document.getElementById('product-search-input');
    searchResultsDiv = document.getElementById('search-results');
    quantityInput = document.getElementById('quantity-input');
    addItemBtn = document.getElementById('add-item-btn');
    invoiceItemsBody = document.getElementById('invoice-items-body');
    customerNameInput = document.getElementById('customer-name');
    customerContactInput = document.getElementById('customer-contact');
    totalAmountSpan = document.getElementById('total-amount');
    totalGstSpan = document.getElementById('total-gst');
    grandTotalSpan = document.getElementById('grand-total');
    savePrintBtn = document.getElementById('save-print-btn');
    clearBtn = document.getElementById('clear-btn');
    logoutBtn = document.getElementById('logout-btn');
    usernameSpan = document.getElementById('username');
    
    // Check if all elements were found
    const elements = {
        productSearchInput,
        searchResultsDiv,
        quantityInput,
        addItemBtn,
        invoiceItemsBody,
        customerNameInput,
        customerContactInput,
        totalAmountSpan,
        totalGstSpan,
        grandTotalSpan,
        savePrintBtn,
        clearBtn,
        logoutBtn,
        usernameSpan
    };
    
    let allFound = true;
    for (const [name, element] of Object.entries(elements)) {
        if (!element) {
            debugLog(`ERROR: Element ${name} not found!`);
            allFound = false;
        }
    }
    
    if (allFound) {
        debugLog("All DOM elements initialized successfully");
    } else {
        debugLog("ERROR: Some DOM elements not found!");
    }
    
    return allFound;
}

// Check if user is logged in
document.addEventListener('DOMContentLoaded', function() {
    debugLog("DOM loaded, initializing sales page");
    
    // Initialize DOM elements
    if (!initDOMElements()) {
        debugLog("ERROR: Failed to initialize DOM elements");
        return;
    }
    
    // Attach event listeners
    attachEventListeners();
    
    const token = localStorage.getItem('pos_token');
    if (!token) {
        debugLog("No token found, redirecting to login");
        window.location.href = 'login.html';
        return;
    }
    
    // Verify token and get user info
    fetch('/api/users/me', {
        headers: {
            'Authorization': `Bearer ${token}`
        }
    })
    .then(response => {
        if (response.ok) {
            return response.json();
        } else {
            throw new Error('Invalid token');
        }
    })
    .then(user => {
        currentUser = user;
        usernameSpan.textContent = user.username;
        debugLog("User authenticated", user);
    })
    .catch(error => {
        debugLog("Auth error", error);
        console.error('Auth error:', error);
        localStorage.removeItem('pos_token');
        window.location.href = 'login.html';
    });
});

// Attach event listeners
function attachEventListeners() {
    debugLog("Attaching event listeners");
    
    try {
        // Product search functionality
        if (productSearchInput) {
            productSearchInput.addEventListener('input', function() {
                const query = this.value.trim();
                debugLog("Product search input changed", query);
                
                if (query.length < 1) {
                    searchResultsDiv.innerHTML = '';
                    searchResults = [];
                    return;
                }
                
                // In a real app, this would be an API call
                // For demo purposes, we'll simulate with sample data
                setTimeout(() => {
                    // Simulate API delay
                    searchProducts(query);
                }, 300);
            });
            debugLog("Product search event listener attached");
        }
        
        // Add item to invoice
        if (addItemBtn) {
            addItemBtn.addEventListener('click', function() {
                debugLog("Add Item button clicked");
                debugLog("Current selected product", currentSelectedProduct);
                
                try {
                    if (!currentSelectedProduct) {
                        debugLog("No product selected");
                        alert('Please select a product first');
                        return;
                    }
                    
                    const quantity = parseInt(quantityInput.value) || 1;
                    debugLog("Adding item with quantity", quantity);
                    
                    // Ensure currentSelectedProduct has proper numeric values
                    const productToAdd = convertProductNumbers(currentSelectedProduct);
                    
                    // Check if product is already in invoice
                    const existingItemIndex = invoiceItems.findIndex(item => item.product_id === productToAdd.product_id);
                    debugLog("Existing item index", existingItemIndex);
                    
                    if (existingItemIndex >= 0) {
                        // Update quantity if product already exists
                        debugLog("Updating existing item quantity");
                        invoiceItems[existingItemIndex].quantity += quantity;
                    } else {
                        // Add new item
                        debugLog("Adding new item");
                        const item = {
                            product_id: productToAdd.product_id,
                            name: productToAdd.name,
                            pack_size: productToAdd.pack_size,
                            gst_rate: productToAdd.gst_rate, // Already converted to number
                            selling_rate: productToAdd.selling_rate, // Already converted to number
                            quantity: quantity
                        };
                        invoiceItems.push(item);
                        debugLog("Item added to invoice", item);
                    }
                    
                    renderInvoiceItems();
                    clearProductSelection();
                } catch (error) {
                    debugLog("Error in add item", error);
                    console.error('Add item error:', error);
                    alert('Error adding item: ' + error.message);
                }
            });
            debugLog("Add Item button event listener attached");
        }
        
        // Save and print functionality
        if (savePrintBtn) {
            savePrintBtn.addEventListener('click', function() {
                debugLog("Save & Print button clicked");
                if (invoiceItems.length === 0) {
                    alert('Please add at least one item to the invoice');
                    return;
                }
                
                const token = localStorage.getItem('pos_token');
                
                // Generate a simple invoice number (in real app, this would be server-generated)
                const invoiceNumber = 'INV-' + Date.now();
                
                // Prepare invoice data
                const invoiceData = {
                    invoice_number: invoiceNumber,
                    customer_name: customerNameInput.value,
                    customer_contact: customerContactInput.value,
                    mode_of_payment: 'Cash', // In a real app, this would be selectable
                    items: invoiceItems.map(item => ({
                        product_id: item.product_id,
                        quantity: item.quantity
                    }))
                };
                
                debugLog("Sending invoice data to server", invoiceData);
                
                fetch('/api/sales', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'Authorization': `Bearer ${token}`
                    },
                    body: JSON.stringify(invoiceData)
                })
                .then(response => {
                    debugLog("Server response", {
                        status: response.status,
                        statusText: response.statusText,
                        ok: response.ok
                    });
                    
                    if (response.ok) {
                        return response.json();
                    } else {
                        // Try to get error details
                        return response.text().then(text => {
                            debugLog("Error response body", text);
                            throw new Error(`HTTP ${response.status}: ${text}`);
                        });
                    }
                })
                .then(invoice => {
                    debugLog("Invoice saved successfully", invoice);
                    // Show success message
                    alert('Invoice saved successfully!');
                    
                    // Generate printable receipt
                    generateReceipt(invoice);
                    
                    // Clear the invoice
                    clearInvoice();
                })
                .catch(error => {
                    debugLog("Save error", error);
                    console.error('Save error:', error);
                    alert('Failed to save invoice. Please try again. Error: ' + error.message);
                });
            });
            debugLog("Save & Print button event listener attached");
        }
        
        // Clear button
        if (clearBtn) {
            clearBtn.addEventListener('click', clearInvoice);
            debugLog("Clear button event listener attached");
        }
        
        // Logout functionality
        if (logoutBtn) {
            logoutBtn.addEventListener('click', function() {
                localStorage.removeItem('pos_token');
                window.location.href = 'login.html';
            });
            debugLog("Logout button event listener attached");
        }
        
        // Close search results when clicking elsewhere
        document.addEventListener('click', function(event) {
            if (searchResultsDiv && !productSearchInput.contains(event.target) && !searchResultsDiv.contains(event.target)) {
                searchResultsDiv.innerHTML = '';
            }
        });
        
        debugLog("All event listeners attached successfully");
    } catch (error) {
        debugLog("ERROR attaching event listeners", error);
        console.error('Error attaching event listeners:', error);
    }
}

function searchProducts(query) {
    debugLog("Searching products", query);
    const token = localStorage.getItem('pos_token');
    
    fetch(`/api/products?q=${encodeURIComponent(query)}`, {
        headers: {
            'Authorization': `Bearer ${token}`
        }
    })
    .then(response => response.json())
    .then(products => {
        debugLog("Products search results", products);
        // Convert string values to numbers
        searchResults = products.map(product => convertProductNumbers(product));
        displaySearchResults();
    })
    .catch(error => {
        debugLog("Search error", error);
        console.error('Search error:', error);
    });
}

function displaySearchResults() {
    debugLog("Displaying search results", searchResults);
    if (searchResults.length === 0) {
        searchResultsDiv.innerHTML = '<div class="search-result-item">No products found</div>';
        return;
    }
    
    searchResultsDiv.innerHTML = '';
    
    searchResults.forEach((product, index) => {
        const resultItem = document.createElement('div');
        resultItem.className = 'search-result-item';
        // Ensure selling_rate is properly formatted as a number
        const sellingRate = typeof product.selling_rate === 'string' ? parseFloat(product.selling_rate) : product.selling_rate;
        resultItem.textContent = `${product.name} (${product.sku}) - ₹${sellingRate.toFixed(2)}`;
        resultItem.addEventListener('click', () => {
            selectProduct(product);
        });
        searchResultsDiv.appendChild(resultItem);
    });
}

function selectProduct(product) {
    debugLog("Product selected", product);
    // Set the selected product in a hidden field or variable
    // Ensure we're working with properly converted numeric values
    currentSelectedProduct = convertProductNumbers(product);
    if (productSearchInput) {
        productSearchInput.value = product.name;
    }
    if (searchResultsDiv) {
        searchResultsDiv.innerHTML = '';
    }
    
    // Ensure the Add Item button is enabled
    if (addItemBtn) {
        addItemBtn.disabled = false;
    }
}

function clearProductSelection() {
    debugLog("Clearing product selection");
    if (productSearchInput) {
        productSearchInput.value = '';
    }
    if (quantityInput) {
        quantityInput.value = '1';
    }
    currentSelectedProduct = null;
    if (searchResultsDiv) {
        searchResultsDiv.innerHTML = '';
    }
}

function renderInvoiceItems() {
    debugLog("Rendering invoice items", invoiceItems);
    if (!invoiceItemsBody) {
        debugLog("ERROR: invoiceItemsBody not found!");
        return;
    }
    
    invoiceItemsBody.innerHTML = '';
    
    let totalAmount = 0;
    let totalGst = 0;
    
    invoiceItems.forEach((item, index) => {
        // Ensure all numeric values are numbers
        const quantity = typeof item.quantity === 'string' ? parseInt(item.quantity) : item.quantity;
        const sellingRate = typeof item.selling_rate === 'string' ? parseFloat(item.selling_rate) : item.selling_rate;
        const gstRate = typeof item.gst_rate === 'string' ? parseFloat(item.gst_rate) : item.gst_rate;
        
        // Calculate item amounts
        const lineAmount = quantity * sellingRate;
        const taxableValue = lineAmount / (1 + (gstRate / 100));
        const itemGst = lineAmount - taxableValue;
        const sgst = itemGst / 2;
        const cgst = itemGst / 2;
        
        totalAmount += lineAmount;
        totalGst += itemGst;
        
        const row = document.createElement('tr');
        row.innerHTML = `
            <td>${index + 1}</td>
            <td>${item.name}</td>
            <td>${item.pack_size || '-'}</td>
            <td>${gstRate}%</td>
            <td>${quantity}</td>
            <td>₹${sellingRate.toFixed(2)}</td>
            <td>₹${taxableValue.toFixed(2)}</td>
            <td>₹${sgst.toFixed(2)}</td>
            <td>₹${cgst.toFixed(2)}</td>
            <td>₹${lineAmount.toFixed(2)}</td>
            <td><button class="remove-btn" data-index="${index}">Remove</button></td>
        `;
        
        invoiceItemsBody.appendChild(row);
    });
    
    // Update totals
    if (totalAmountSpan) {
        totalAmountSpan.textContent = `₹${totalAmount.toFixed(2)}`;
    }
    if (totalGstSpan) {
        totalGstSpan.textContent = `₹${totalGst.toFixed(2)}`;
    }
    if (grandTotalSpan) {
        grandTotalSpan.textContent = `₹${(totalAmount).toFixed(2)}`;
    }
    
    // Add event listeners to remove buttons
    document.querySelectorAll('.remove-btn').forEach(button => {
        button.addEventListener('click', function() {
            const index = parseInt(this.getAttribute('data-index'));
            invoiceItems.splice(index, 1);
            renderInvoiceItems();
        });
    });
}

function generateReceipt(invoice) {
    // In a real implementation, this would open a print-friendly page
    // For now, we'll just log the invoice data
    console.log('Receipt data:', invoice);
    alert('In a complete implementation, this would generate a printable receipt.');
}

function clearInvoice() {
    debugLog("Clearing invoice");
    invoiceItems = [];
    renderInvoiceItems();
    if (customerNameInput) {
        customerNameInput.value = '';
    }
    if (customerContactInput) {
        customerContactInput.value = '';
    }
    clearProductSelection();
}