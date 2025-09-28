# POS System - Complete File List

## Backend Files (Python/Flask)

1. `app.py` - Main Flask application entry point
2. `db.py` - Database connection and initialization
3. `auth.py` - Authentication utilities (JWT, password hashing)
4. `schema.sql` - Database schema and sample data
5. `requirements.txt` - Python package dependencies
6. `init_db.py` - Database initialization script
7. `test_setup.py` - Setup verification script
8. Routes:
   - `routes/__init__.py` - Package initializer
   - `routes/auth.py` - Authentication routes
   - `routes/products.py` - Product management routes
   - `routes/sales.py` - Sales transaction routes
   - `routes/inventory.py` - Inventory management routes
   - `routes/reports.py` - Reporting routes
   - `routes/admin.py` - Admin routes

## Frontend Files (HTML/CSS/JavaScript)

1. `start.html` - Welcome page
2. `login.html` - User login page
3. `dashboard.html` - Main dashboard with navigation
4. `index.html` - Main sales interface
5. `purchase.html` - Purchase/stock receiving interface
6. `inventory.html` - Inventory management
7. `reports.html` - Sales reporting with charts
8. `admin.html` - Admin panel (product/user management)
9. `receipt.html` - Printable receipt template
10. `navigation.html` - Shared navigation menu
11. `styles.css` - Main stylesheet for all pages
12. `sales.js` - JavaScript for sales interface

## Configuration and Documentation

1. `.env.example` - Example environment variables file
2. `.env` - Environment variables (created by user)
3. `README.md` - Project documentation
4. `FILE_STRUCTURE.md` - Detailed file structure explanation
5. `setup.sh` - Setup script for Unix/Linux/Mac
6. `setup.bat` - Setup script for Windows
7. `run.sh` - Run script for Unix/Linux/Mac
8. `run.bat` - Run script for Windows

## Database Schema

The system includes the following tables:
- `users` - User accounts with roles (Admin/Cashier)
- `products` - Product information (name, SKU, rates, etc.)
- `inventory` - Stock quantities for products
- `sales_invoices` - Sales transaction headers
- `sales_invoice_items` - Line items for sales transactions

## Key Features Implemented

1. **User Authentication**
   - Secure login with JWT tokens
   - Role-based access control (Admin/Cashier)

2. **Sales Management**
   - Product search with autocomplete
   - GST calculations (SGST/CGST)
   - Real-time invoice total calculation
   - Save and print functionality

3. **Purchase Management**
   - Supplier information tracking
   - Stock receiving functionality
   - Purchase rate management

4. **Inventory Management**
   - Real-time stock tracking
   - Low stock alerts
   - Stock adjustment functionality

5. **Product Management**
   - Full CRUD operations
   - SKU management
   - GST rate configuration

6. **Reporting**
   - Sales summary reports
   - Date range filtering
   - Top-selling products
   - Visual charts with Chart.js

7. **Administration**
   - User management
   - Invoice cancellation
   - System configuration

## Security Features

- Password hashing with passlib
- JWT token-based authentication
- Protected API endpoints
- Role-based access control

## Responsive Design

- Mobile-friendly interface
- Tablet-optimized layouts
- Desktop-responsive grids
- Touch-friendly controls