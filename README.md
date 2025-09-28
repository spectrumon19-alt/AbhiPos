# Point of Sale (POS) System

A complete web-based Point of Sale system with Python backend, PostgreSQL database, and HTML/CSS/JavaScript frontend.

## Features

- **User Authentication**: Secure login with JWT tokens
- **Sales Management**: Process sales transactions with GST calculations
- **Purchase Management**: Record incoming stock from suppliers
- **Inventory Management**: Track stock levels and receive new stock
- **Product Management**: Add, edit, and delete products
- **User Management**: Create and manage users with different roles
- **Reporting**: Generate sales reports with charts
- **Invoice Cancellation**: Admins can cancel invoices and restore stock
- **Printable Receipts**: Generate printable receipts for customers

## Technology Stack

- **Backend**: Python with Flask
- **Database**: PostgreSQL
- **Frontend**: HTML5, CSS3, JavaScript (no frameworks)
- **Authentication**: JWT tokens
- **Password Security**: passlib for password hashing
- **Charts**: Chart.js for reporting

## Setup Instructions

### Prerequisites

1. Python 3.7 or higher
2. PostgreSQL database
3. Node.js and npm (for any frontend build tools if needed)

### Installation

1. Clone the repository:
   ```
   git clone <repository-url>
   cd pos-system
   ```

2. Create a virtual environment:
   ```
   # On Windows
   python -m venv venv
   venv\Scripts\activate
   
   # On macOS/Linux
   python3 -m venv venv
   source venv/bin/activate
   ```

3. Install Python dependencies:
   ```
   pip install -r requirements.txt
   ```

4. Set up the PostgreSQL database:
   - Create a new database in PostgreSQL
   - Update the database connection details in the `.env` file
   - Run the schema.sql script to create tables:
     ```
     psql -U <username> -d <database_name> -f schema.sql
     ```

5. Create a `.env` file with the following variables:
   ```
   SECRET_KEY=your-secret-key-here
   DB_HOST=localhost
   DB_NAME=pos_db
   DB_USER=your_database_username
   DB_PASSWORD=your_database_password
   ```

### Running the Application

1. Start the Flask server:
   ```
   python app.py
   ```

2. Open your browser and navigate to `http://localhost:5000`

3. Login with the default credentials:
   - Admin: username `admin`, password `admin123`
   - Cashier: username `cashier`, password `cashier123`

## Project Structure

```
pos-system/
├── app.py              # Main Flask application
├── schema.sql          # Database schema
├── requirements.txt    # Python dependencies
├── .env                # Environment variables (create this file)
├── db.py               # Database connection utilities
├── auth.py             # Authentication utilities
├── routes/             # API route handlers
│   ├── __init__.py
│   ├── auth.py         # Authentication routes
│   ├── products.py     # Product management routes
│   ├── sales.py        # Sales transaction routes
│   ├── inventory.py    # Inventory management routes
│   ├── reports.py      # Reporting routes
│   └── admin.py        # Admin routes
├── index.html          # Main sales interface
├── login.html          # Login page
├── dashboard.html      # Dashboard with navigation
├── purchase.html       # Purchase/stock receiving
├── inventory.html      # Inventory management
├── reports.html        # Sales reporting
├── admin.html          # Admin panel
├── receipt.html        # Printable receipt template
├── styles.css          # Main stylesheet
└── sales.js            # Sales interface JavaScript
```

## API Endpoints

### Authentication
- `POST /api/login` - User login
- `GET /api/users/me` - Get current user info

### Products
- `GET /api/products?q=<search>` - Search products
- `POST /api/products` - Create product (Admin only)
- `PUT /api/products/<id>` - Update product (Admin only)
- `DELETE /api/products/<id>` - Delete product (Admin only)

### Sales
- `POST /api/sales` - Create sales invoice
- `PUT /api/sales/<invoice_id>/cancel` - Cancel invoice (Admin only)

### Inventory
- `GET /api/inventory` - Get inventory levels
- `POST /api/inventory/update` - Update inventory (Admin only)

### Reports
- `GET /api/reports/sales?start_date=<>&end_date<>` - Get sales report

### Admin
- `GET /api/admin/users` - Get all users (Admin only)
- `POST /api/admin/users` - Create user (Admin only)
- `PUT /api/admin/users/<id>/reset-password` - Reset user password (Admin only)
- `GET /api/admin/invoices` - Get all invoices (Admin only)

## Security Features

- Passwords are hashed using passlib
- JWT tokens for session management
- Role-based access control (Admin/Cashier)
- Protected API endpoints with token verification

## Responsive Design

The frontend is built with responsive design principles using:
- CSS Flexbox and Grid
- Media queries for different screen sizes
- Mobile-friendly interface

## License

This project is for educational purposes. Feel free to modify and extend it for your needs.