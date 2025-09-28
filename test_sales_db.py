import psycopg2
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def test_sales_insert():
    """Test inserting a sales invoice directly into the database"""
    conn = None
    try:
        # Connect to database
        conn = psycopg2.connect(
            host=os.environ.get('DB_HOST', 'localhost'),
            database=os.environ.get('DB_NAME', 'pos_db'),
            user=os.environ.get('DB_USER', 'postgres'),
            password=os.environ.get('DB_PASSWORD', 'your_actual_password_here')
        )
        
        cur = conn.cursor()
        
        print("Connected to database successfully")
        
        # Check if required data exists
        cur.execute("SELECT COUNT(*) FROM products")
        result = cur.fetchone()
        product_count = result[0] if result else 0
        print(f"Products in database: {product_count}")
        
        cur.execute("SELECT COUNT(*) FROM inventory")
        result = cur.fetchone()
        inventory_count = result[0] if result else 0
        print(f"Inventory records: {inventory_count}")
        
        cur.execute("SELECT COUNT(*) FROM users")
        result = cur.fetchone()
        user_count = result[0] if result else 0
        print(f"Users in database: {user_count}")
        
        # Get a valid user ID
        cur.execute("SELECT user_id FROM users LIMIT 1")
        user_result = cur.fetchone()
        if not user_result:
            print("No users found in database")
            return
            
        user_id = user_result[0]
        print(f"Using user_id: {user_id}")
        
        # Get a valid product
        cur.execute("SELECT product_id, selling_rate, gst_rate FROM products LIMIT 1")
        product_result = cur.fetchone()
        if not product_result:
            print("No products found in database")
            return
            
        product_id, selling_rate, gst_rate = product_result
        print(f"Using product_id: {product_id}, selling_rate: {selling_rate}, gst_rate: {gst_rate}")
        
        # Test the sales invoice insertion
        print("Testing sales invoice insertion...")
        
        # Insert sales invoice
        cur.execute("""
            INSERT INTO sales_invoices (
                invoice_number, customer_name, customer_contact, 
                user_id, mode_of_payment, total_amount, total_gst, status
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            RETURNING invoice_id
        """, (
            'INV-TEST-001',
            'Test Customer',
            '1234567890',
            user_id,
            'Cash',
            0,  # Will be updated
            0,  # Will be updated
            'Completed'
        ))
        
        result = cur.fetchone()
        invoice_id = result[0] if result else None
        if not invoice_id:
            print("Failed to create invoice")
            return
            
        print(f"Created invoice with ID: {invoice_id}")
        
        # Insert invoice item
        quantity = 1
        # Calculate values (same as in the backend)
        total_line_amount = quantity * selling_rate
        exclusive_gst_amount = total_line_amount / (1 + (gst_rate / 100))
        total_gst = total_line_amount - exclusive_gst_amount
        sgst = total_gst / 2
        cgst = total_gst / 2
        
        cur.execute("""
            INSERT INTO sales_invoice_items (
                invoice_id, product_id, quantity, rate_at_sale, 
                gst_rate_at_sale, exclusive_gst_amount, sgst, cgst, total_line_amount
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, (
            invoice_id, product_id, quantity, selling_rate,
            gst_rate, exclusive_gst_amount, sgst, 
            cgst, total_line_amount
        ))
        
        print("Inserted invoice item successfully")
        
        # Update invoice totals
        cur.execute("""
            UPDATE sales_invoices 
            SET total_amount = %s, total_gst = %s
            WHERE invoice_id = %s
        """, (total_line_amount, total_gst, invoice_id))
        
        print("Updated invoice totals successfully")
        
        # Update inventory
        cur.execute("""
            UPDATE inventory 
            SET stock_quantity = stock_quantity - %s 
            WHERE product_id = %s
        """, (quantity, product_id))
        
        if cur.rowcount == 0:
            print("Warning: No inventory record updated")
        else:
            print("Updated inventory successfully")
        
        # Commit transaction
        conn.commit()
        print("Transaction committed successfully")
        
        # Clean up - delete test records
        cur.execute("DELETE FROM sales_invoice_items WHERE invoice_id = %s", (invoice_id,))
        cur.execute("DELETE FROM sales_invoices WHERE invoice_id = %s", (invoice_id,))
        conn.commit()
        print("Cleaned up test records")
        
        cur.close()
        conn.close()
        print("Database test completed successfully!")
        
    except Exception as e:
        print(f"Database test error: {e}")
        if conn:
            conn.rollback()
            conn.close()

if __name__ == "__main__":
    test_sales_insert()