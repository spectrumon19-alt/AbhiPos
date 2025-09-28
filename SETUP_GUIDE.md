# POS System Setup Guide

## Prerequisites

1. Python 3.7 or higher
2. PostgreSQL database server
3. pip (Python package installer)

## Installation Steps

### 1. Install Python Dependencies

```bash
pip install -r requirements.txt
```

Or install packages individually:
```bash
pip install Flask==2.3.2
pip install Flask-CORS==4.0.0
pip install psycopg2-binary==2.9.7
pip install passlib==1.7.4
pip install PyJWT==2.8.0
pip install python-dotenv==1.0.0
```

### 2. Configure Database

1. Install PostgreSQL if not already installed
2. Create a new database (e.g., `pos_db`)
3. Update the `.env` file with your database credentials:

```env
SECRET_KEY=your-secret-key-here
DB_HOST=localhost
DB_NAME=pos_db
DB_USER=your_postgres_username
DB_PASSWORD=your_postgres_password
```

### 3. Initialize Database Schema

```bash
python init_db.py
```

### 4. Run the Application

```bash
python app.py
```

The application will start on `http://localhost:5000`

## Default User Accounts

- **Admin**: 
  - Username: `admin`
  - Password: `admin123`
  
- **Cashier**: 
  - Username: `cashier`
  - Password: `cashier123`

## Troubleshooting

### Common Issues

1. **Module not found errors**: Make sure all dependencies are installed
   ```bash
   pip install -r requirements.txt
   ```

2. **Database connection failed**: 
   - Check PostgreSQL is running
   - Verify credentials in `.env` file
   - Ensure the database exists

3. **Port already in use**:
   - Edit `app.py` to change the port
   - Or stop the existing process using port 5000

### Testing the API

You can test the API using curl or any HTTP client:

```bash
# Test login
curl -X POST http://localhost:5000/api/login \
  -H "Content-Type: application/json" \
  -d '{"username": "admin", "password": "admin123"}'
```

## File Structure

```
pos-system/
├── app.py              # Main Flask application
├── db.py               # Database utilities
├── auth.py             # Authentication utilities
├── schema.sql          # Database schema
├── requirements.txt    # Python dependencies
├── .env                # Environment variables
├── routes/             # API route handlers
├── *.html              # Frontend HTML files
├── styles.css          # CSS stylesheet
└── sales.js            # JavaScript for sales interface
```

## API Endpoints

### Authentication
- `POST /api/login` - User login

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