# How to Use Other Modules in the POS System

## Overview
The POS system consists of several interconnected modules that handle different aspects of business operations. Each module has both frontend (HTML/JavaScript) and backend (Python/Flask) components.

## Available Modules

### 1. Sales Module
- **Frontend**: [index.html](file:///c%3A/Users/abhis/OneDrive/Desktop/t/webAppPOS/qodo/index.html) or [sales.html](file:///c%3A/Users/abhis/OneDrive/Desktop/t/webAppPOS/qodo/index.html)
- **Backend**: [routes/sales.py](file:///c%3A/Users/abhis/OneDrive/Desktop/t/webAppPOS/qodo/routes/sales.py)
- **Functionality**: Process sales transactions, generate invoices, manage customers
- **Access**: Click "Sales" in the navigation menu

### 2. Purchase Module
- **Frontend**: [purchase.html](file:///c%3A/Users/abhis/OneDrive/Desktop/t/webAppPOS/qodo/purchase.html)
- **Backend**: [routes/purchase.py](file:///c%3A/Users/abhis/OneDrive/Desktop/t/webAppPOS/qodo/routes/purchase.py)
- **Functionality**: Record incoming stock from suppliers, manage purchase orders
- **Access**: Click "Purchase" in the navigation menu

### 3. Inventory Module
- **Frontend**: [inventory.html](file:///c%3A/Users/abhis/OneDrive/Desktop/t/webAppPOS/qodo/inventory.html)
- **Backend**: [routes/inventory.py](file:///c%3A/Users/abhis/OneDrive/Desktop/t/webAppPOS/qodo/routes/inventory.py)
- **Functionality**: View current stock levels, track low stock items
- **Access**: Click "Inventory" in the navigation menu

### 4. Reports Module
- **Frontend**: [reports.html](file:///c%3A/Users/abhis/OneDrive/Desktop/t/webAppPOS/qodo/reports.html)
- **Backend**: [routes/reports.py](file:///c%3A/Users/abhis/OneDrive/Desktop/t/webAppPOS/qodo/routes/reports.py)
- **Functionality**: Generate sales reports, view performance metrics
- **Access**: Click "Reports" in the navigation menu

### 5. Admin Module
- **Frontend**: [admin.html](file:///c%3A/Users/abhis/OneDrive/Desktop/t/webAppPOS/qodo/admin.html)
- **Backend**: [routes/admin.py](file:///c%3A/Users/abhis/OneDrive/Desktop/t/webAppPOS/qodo/routes/admin.py)
- **Functionality**: Manage products, users, and system settings (Admin access required)
- **Access**: Click "Admin" in the navigation menu (only visible to Admin users)

## How to Navigate Between Modules

### Using the Navigation Menu
1. All modules can be accessed through the main navigation menu
2. The navigation menu is available on most pages
3. Simply click on the module name to navigate to that section

### Using Direct Links
You can also navigate directly to modules using these URLs:
- Dashboard: `http://localhost:5001/dashboard.html`
- Sales: `http://localhost:5001/index.html`
- Purchase: `http://localhost:5001/purchase.html`
- Inventory: `http://localhost:5001/inventory.html`
- Reports: `http://localhost:5001/reports.html`
- Admin: `http://localhost:5001/admin.html`

## Module-Specific Instructions

### Sales Module
1. Search for products using the search bar
2. Select a product from the search results
3. Enter quantity and click "Add Item"
4. Repeat for all items in the transaction
5. Enter customer information (optional)
6. Click "Save & Print" to complete the sale

### Purchase Module
1. Search for suppliers or select from existing suppliers
2. Add products to the purchase order
3. Enter quantities and prices
4. Review the purchase order
5. Click "Save Purchase" to record the transaction

### Inventory Module
1. View current stock levels for all products
2. Search for specific products using the search bar
3. Low stock items are highlighted
4. Refresh the inventory data using the "Refresh Inventory" button

### Reports Module
1. Select the type of report you want to generate
2. Choose date range if applicable
3. Click "Generate Report" to view the data
4. Export reports if needed

### Admin Module
1. Manage products (add, edit, delete)
2. Manage users (add, edit, change roles)
3. View system logs and audit trails
4. Configure system settings

## User Roles and Permissions

### Regular Users
- Can access Sales, Purchase, Inventory, and Reports modules
- Cannot access Admin module

### Admin Users
- Have full access to all modules
- Can manage products and users
- Can configure system settings

## API Endpoints

Each module has corresponding API endpoints:

### Authentication
- `POST /api/login` - User login
- `GET /api/users/me` - Get current user info

### Products
- `GET /api/products` - Get all products
- `GET /api/products?q=search_term` - Search products
- `POST /api/products` - Create new product (Admin only)
- `PUT /api/products/<id>` - Update product (Admin only)
- `DELETE /api/products/<id>` - Delete product (Admin only)

### Sales
- `POST /api/sales` - Create new sale
- `PUT /api/sales/<id>/cancel` - Cancel sale (Admin only)

### Inventory
- `GET /api/inventory` - Get inventory data
- `POST /api/inventory/update` - Update inventory (Admin only)

### Reports
- `GET /api/reports/sales-summary` - Get sales summary
- `GET /api/reports/top-products` - Get top selling products

### Admin
- `GET /api/admin/users` - Get all users (Admin only)
- `POST /api/admin/users` - Create new user (Admin only)
- `PUT /api/admin/users/<id>` - Update user (Admin only)

## Troubleshooting Common Issues

### Module Not Loading
1. Check if the server is running
2. Verify the URL is correct
3. Check browser console for errors
4. Ensure you have proper permissions

### Data Not Displaying
1. Check network tab in browser developer tools
2. Verify API endpoints are returning data
3. Check database connectivity
4. Ensure you're logged in with proper credentials

### Permission Errors
1. Verify your user role
2. Contact administrator if you need additional permissions
3. Check if the feature requires Admin access

## Best Practices

1. Always log out when finished using the system
2. Use strong passwords for security
3. Regularly refresh data to ensure you have the latest information
4. Back up data regularly
5. Keep your browser updated for security