# POS System - File Structure

This document explains the organization of files in the POS System project.

## Backend Files (Python/Flask)

```
pos-system/
├── app.py                 # Main Flask application entry point
├── db.py                  # Database connection and initialization
├── auth.py                # Authentication utilities (JWT, password hashing)
├── schema.sql             # Database schema and sample data
├── requirements.txt       # Python package dependencies
├── .env                   # Environment variables (created by user)
├── .env.example           # Example environment variables file
├── setup.sh               # Setup script for Unix/Linux/Mac
├── setup.bat              # Setup script for Windows
├── run.sh                 # Run script for Unix/Linux/Mac
├── run.bat                # Run script for Windows
├── test_setup.py          # Setup verification script
├── README.md              # Project documentation
├── routes/                # API route handlers
│   ├── __init__.py        # Package initializer
│   ├── auth.py            # Authentication routes (/api/login, /api/users/me)
│   ├── products.py        # Product management routes (/api/products)
│   ├── sales.py           # Sales transaction routes (/api/sales)
│   ├── inventory.py       # Inventory management routes (/api/inventory)
│   ├── reports.py         # Reporting routes (/api/reports/sales)
│   └── admin.py           # Admin routes (/api/admin/*)
```

## Frontend Files (HTML/CSS/JavaScript)

```
pos-system/
├── index.html             # Main sales interface
├── login.html             # User login page
├── dashboard.html         # Main dashboard with navigation
├── purchase.html          # Purchase/stock receiving interface
├── inventory.html         # Inventory management
├── reports.html           # Sales reporting with charts
├── admin.html             # Admin panel (product/user management)
├── receipt.html           # Printable receipt template
├── navigation.html        # Shared navigation menu
├── styles.css             # Main stylesheet for all pages
├── sales.js               # JavaScript for sales interface
```

## Key Features by File

### Authentication
- `auth.py` - Password hashing, JWT token generation/verification
- `routes/auth.py` - Login endpoint and user info endpoint

### Product Management
- `routes/products.py` - CRUD operations for products
- `admin.html` - UI for product management

### Sales Processing
- `routes/sales.py` - Create sales invoices with GST calculations
- `index.html` - Main sales interface
- `sales.js` - Client-side logic for sales

### Purchase/Inventory
- `routes/inventory.py` - Inventory queries and updates
- `purchase.html` - UI for receiving stock
- `inventory.html` - Inventory viewing

### Reporting
- `routes/reports.py` - Sales reporting with date filters
- `reports.html` - Reporting dashboard with charts

### Administration
- `routes/admin.py` - User management, invoice viewing
- `admin.html` - Admin panel UI

## Database Schema

The `schema.sql` file contains:
- Users table (user management)
- Products table (product information)
- Inventory table (stock tracking)
- Sales invoices table (transaction headers)
- Sales invoice items table (transaction details)

## Environment Variables

The `.env` file should contain:
- `SECRET_KEY` - For JWT token signing
- `DB_HOST` - Database server address
- `DB_NAME` - Database name
- `DB_USER` - Database username
- `DB_PASSWORD` - Database password