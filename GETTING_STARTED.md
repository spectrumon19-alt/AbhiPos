# POS System - Getting Started

## Overview

This document provides a step-by-step guide to get your Point of Sale system up and running.

## Quick Start

1. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Configure Database**:
   - Install PostgreSQL
   - Create a database
   - Update `.env` with your credentials

3. **Initialize Database**:
   ```bash
   python init_db.py
   ```

4. **Run Application**:
   ```bash
   python app.py
   ```

5. **Access Application**:
   Open your browser to `http://localhost:5000`

## Detailed Setup

### Step 1: Install Python Dependencies

Make sure you have all required packages installed:

```bash
pip install Flask Flask-CORS psycopg2-binary passlib PyJWT python-dotenv
```

Or use the requirements file:
```bash
pip install -r requirements.txt
```

### Step 2: Database Setup

1. Install PostgreSQL from https://www.postgresql.org/download/
2. Start the PostgreSQL service
3. Create a new database:
   ```sql
   CREATE DATABASE pos_db;
   ```
4. Update the `.env` file with your database credentials

### Step 3: Environment Configuration

Create a `.env` file in the project root with the following content:

```env
SECRET_KEY=your-very-secure-secret-key-here
DB_HOST=localhost
DB_NAME=pos_db
DB_USER=your_postgres_username
DB_PASSWORD=your_postgres_password
```

### Step 4: Initialize Database Schema

Run the database initialization script:

```bash
python init_db.py
```

This will create all necessary tables and insert sample data.

### Step 5: Start the Application

Run the Flask application:

```bash
python app.py
```

The application will start on `http://localhost:5000`

## Default Credentials

- **Admin User**:
  - Username: `admin`
  - Password: `admin123`

- **Cashier User**:
  - Username: `cashier`
  - Password: `cashier123`

## Application Features

### Sales Interface
- Product search with autocomplete
- Real-time invoice calculation
- GST (SGST/CGST) calculations
- Save and print functionality

### Purchase Management
- Supplier information tracking
- Stock receiving interface
- Purchase rate management

### Inventory Management
- Real-time stock tracking
- Low stock alerts
- Stock adjustment functionality

### Reporting
- Sales summary reports
- Date range filtering
- Top-selling products
- Visual charts

### Administration
- Product CRUD operations
- User management
- Invoice viewing and cancellation
- Role-based permissions

## File Structure

The application is organized as follows:

```
pos-system/
├── Backend (Python/Flask)
│   ├── app.py              # Main application
│   ├── db.py               # Database utilities
│   ├── auth.py             # Authentication
│   ├── routes/             # API endpoints
│   └── schema.sql          # Database schema
│
├── Frontend (HTML/CSS/JS)
│   ├── *.html              # Page templates
│   ├── styles.css          # Styling
│   └── sales.js            # Client logic
│
└── Configuration
    ├── .env                # Environment config
    └── requirements.txt    # Dependencies
```

## API Endpoints

### Authentication
- `POST /api/login` - User authentication

### Products
- `GET /api/products` - List/search products
- `POST /api/products` - Create product
- `PUT /api/products/<id>` - Update product
- `DELETE /api/products/<id>` - Delete product

### Sales
- `POST /api/sales` - Create invoice
- `PUT /api/sales/<id>/cancel` - Cancel invoice

### Inventory
- `GET /api/inventory` - View stock levels
- `POST /api/inventory/update` - Adjust stock

### Reports
- `GET /api/reports/sales` - Sales reports

### Admin
- `GET /api/admin/users` - List users
- `POST /api/admin/users` - Create user
- `GET /api/admin/invoices` - List invoices

## Troubleshooting

### Common Issues

1. **Import errors**: Ensure all dependencies are installed
2. **Database connection errors**: Check PostgreSQL service and credentials
3. **Port conflicts**: Change port in `app.py` if 5000 is in use

### Testing

Run the test script to verify the application structure:

```bash
python test_app.py
```

## Next Steps

1. Customize the UI in the HTML files
2. Add more product fields as needed
3. Implement additional reports
4. Add more user roles if needed
5. Enhance security features