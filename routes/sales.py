from flask import Blueprint, request, jsonify
from db import get_db_connection
from auth import token_required
from psycopg2.extras import RealDictCursor
import math

sales_bp = Blueprint('sales', __name__)

def calculate_invoice_item(quantity, selling_rate, gst_rate):
    """Calculate invoice item details based on quantity, rate and GST"""
    # S.Amount (Total Line Amount) = Quantity * Selling Rate
    total_line_amount = quantity * selling_rate
    
    # S.Exclusive GST (Taxable Value) = S.Amount / (1 + (GST Rate / 100))
    exclusive_gst_amount = total_line_amount / (1 + (gst_rate / 100))
    
    # Total GST = S.Amount - S.Exclusive GST
    total_gst = total_line_amount - exclusive_gst_amount
    
    # SGST = Total GST / 2
    sgst = total_gst / 2
    
    # CGST = Total GST / 2
    cgst = total_gst / 2
    
    return {
        'total_line_amount': round(total_line_amount, 2),
        'exclusive_gst_amount': round(exclusive_gst_amount, 2),
        'total_gst': round(total_gst, 2),
        'sgst': round(sgst, 2),
        'cgst': round(cgst, 2)
    }

@sales_bp.route('/sales', methods=['POST'])
@token_required
def create_sale(payload):
    data = request.get_json()
    user_id = payload.get('user_id')
    
    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    
    try:
        # Create sales invoice
        cur.execute("""
            INSERT INTO sales_invoices (
                invoice_number, customer_name, customer_contact, 
                user_id, mode_of_payment, total_amount, total_gst, status
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            RETURNING invoice_id, invoice_number, invoice_date
        """, (
            data.get('invoice_number'),
            data.get('customer_name'),
            data.get('customer_contact'),
            user_id,
            data.get('mode_of_payment'),
            0,  # Will be updated after calculating items
            0,  # Will be updated after calculating items
            'Completed'
        ))
        
        invoice = cur.fetchone()
        if not invoice:
            raise Exception('Failed to create invoice')
        invoice_id = invoice['invoice_id']
        
        # Process each item
        items = data.get('items', [])
        total_invoice_amount = 0
        total_invoice_gst = 0
        
        for item in items:
            product_id = item.get('product_id')
            quantity = item.get('quantity')
            
            # Get product details
            cur.execute("""
                SELECT selling_rate, gst_rate FROM products WHERE product_id = %s
            """, (product_id,))
            
            product = cur.fetchone()
            if not product:
                raise Exception(f"Product with ID {product_id} not found")
            
            selling_rate = product['selling_rate']
            gst_rate = product['gst_rate']
            
            # Calculate item details
            calc = calculate_invoice_item(quantity, selling_rate, gst_rate)
            
            # Insert invoice item
            cur.execute("""
                INSERT INTO sales_invoice_items (
                    invoice_id, product_id, quantity, rate_at_sale, 
                    gst_rate_at_sale, exclusive_gst_amount, sgst, cgst, total_line_amount
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, (
                invoice_id, product_id, quantity, selling_rate,
                gst_rate, calc['exclusive_gst_amount'], calc['sgst'], 
                calc['cgst'], calc['total_line_amount']
            ))
            
            # Update totals
            total_invoice_amount += calc['total_line_amount']
            total_invoice_gst += calc['total_gst']
            
            # Update inventory (decrement stock)
            cur.execute("""
                UPDATE inventory 
                SET stock_quantity = stock_quantity - %s 
                WHERE product_id = %s
            """, (quantity, product_id))
            
            # Check if update was successful
            if cur.rowcount == 0:
                raise Exception(f"Failed to update inventory for product {product_id}")
        
        # Update invoice with calculated totals
        cur.execute("""
            UPDATE sales_invoices 
            SET total_amount = %s, total_gst = %s
            WHERE invoice_id = %s
        """, (total_invoice_amount, total_invoice_gst, invoice_id))
        
        # Commit transaction
        conn.commit()
        
        # Fetch the complete invoice with items
        cur.execute("""
            SELECT 
                si.*, 
                u.username as created_by,
                json_agg(sii.*) as items
            FROM sales_invoices si
            JOIN users u ON si.user_id = u.user_id
            JOIN sales_invoice_items sii ON si.invoice_id = sii.invoice_id
            WHERE si.invoice_id = %s
            GROUP BY si.invoice_id, u.username
        """, (invoice_id,))
        
        result = cur.fetchone()
        
        return jsonify(result), 201
    except Exception as e:
        if conn:
            conn.rollback()
        return jsonify({'message': 'Failed to create sale', 'error': str(e)}), 500
    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()

@sales_bp.route('/sales/<int:invoice_id>/cancel', methods=['PUT'])
@token_required
def cancel_sale(payload, invoice_id):
    # Check if user is admin
    if payload.get('role') != 'Admin':
        return jsonify({'message': 'Admin access required'}), 403
        
    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    
    try:
        # Check if invoice exists and is not already cancelled
        cur.execute("""
            SELECT status FROM sales_invoices WHERE invoice_id = %s
        """, (invoice_id,))
        
        invoice = cur.fetchone()
        if not invoice:
            return jsonify({'message': 'Invoice not found'}), 404
            
        if invoice['status'] == 'Cancelled':
            return jsonify({'message': 'Invoice is already cancelled'}), 400
        
        # Get all items in the invoice
        cur.execute("""
            SELECT product_id, quantity FROM sales_invoice_items WHERE invoice_id = %s
        """, (invoice_id,))
        
        items = cur.fetchall()
        
        # Update inventory (increment stock for each item)
        for item in items:
            cur.execute("""
                UPDATE inventory 
                SET stock_quantity = stock_quantity + %s 
                WHERE product_id = %s
            """, (item['quantity'], item['product_id']))
            
            # Check if update was successful
            if cur.rowcount == 0:
                raise Exception(f"Failed to update inventory for product {item['product_id']}")
        
        # Update invoice status to cancelled
        cur.execute("""
            UPDATE sales_invoices 
            SET status = 'Cancelled' 
            WHERE invoice_id = %s
        """, (invoice_id,))
        
        # Commit transaction
        conn.commit()
        
        return jsonify({'message': 'Invoice cancelled successfully'}), 200
    except Exception as e:
        if conn:
            conn.rollback()
        return jsonify({'message': 'Failed to cancel sale', 'error': str(e)}), 500
    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()