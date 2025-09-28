from flask import Blueprint, request, jsonify
from db import get_db_connection
from auth import token_required
from psycopg2.extras import RealDictCursor
from datetime import datetime

reports_bp = Blueprint('reports', __name__)

@reports_bp.route('/reports/sales', methods=['GET'])
@token_required
def get_sales_report(payload):
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    
    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    
    try:
        # Build query based on date filters
        base_query = """
            SELECT 
                DATE(si.invoice_date) as sale_date,
                COUNT(si.invoice_id) as total_invoices,
                SUM(si.total_amount) as total_sales,
                SUM(si.total_gst) as total_gst_collected
            FROM sales_invoices si
            WHERE si.status = 'Completed'
        """
        
        params = []
        if start_date:
            base_query += " AND si.invoice_date >= %s"
            params.append(start_date)
            
        if end_date:
            base_query += " AND si.invoice_date <= %s"
            params.append(end_date)
            
        base_query += " GROUP BY DATE(si.invoice_date) ORDER BY sale_date"
        
        cur.execute(base_query, params)
        daily_sales = cur.fetchall()
        
        # Calculate overall totals
        total_sales = sum(row['total_sales'] if row['total_sales'] else 0 for row in daily_sales)
        total_gst = sum(row['total_gst_collected'] if row['total_gst_collected'] else 0 for row in daily_sales)
        total_invoices = sum(row['total_invoices'] for row in daily_sales)
        
        # Get top selling products
        product_query = """
            SELECT 
                p.name,
                SUM(sii.quantity) as total_quantity_sold,
                SUM(sii.total_line_amount) as total_value_sold
            FROM sales_invoice_items sii
            JOIN products p ON sii.product_id = p.product_id
            JOIN sales_invoices si ON sii.invoice_id = si.invoice_id
            WHERE si.status = 'Completed'
        """
        
        product_params = []
        if start_date:
            product_query += " AND si.invoice_date >= %s"
            product_params.append(start_date)
            
        if end_date:
            product_query += " AND si.invoice_date <= %s"
            product_params.append(end_date)
            
        product_query += " GROUP BY p.product_id, p.name ORDER BY total_quantity_sold DESC LIMIT 10"
        
        cur.execute(product_query, product_params)
        top_products = cur.fetchall()
        
        return jsonify({
            'summary': {
                'total_sales': total_sales,
                'total_gst': total_gst,
                'total_invoices': total_invoices
            },
            'daily_sales': daily_sales,
            'top_products': top_products
        }), 200
    except Exception as e:
        return jsonify({'message': 'Failed to generate sales report', 'error': str(e)}), 500
    finally:
        cur.close()
        conn.close()