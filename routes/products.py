from flask import Blueprint, request, jsonify
from db import get_db_connection
from auth import token_required
from psycopg2.extras import RealDictCursor

products_bp = Blueprint('products', __name__)

@products_bp.route('/products', methods=['GET'])
@token_required
def get_products(payload):
    query = request.args.get('q', '')
    
    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    
    try:
        if query:
            search_query = f"%{query}%"
            cur.execute("""
                SELECT p.*, i.stock_quantity 
                FROM products p
                LEFT JOIN inventory i ON p.product_id = i.product_id
                WHERE p.name ILIKE %s OR p.sku ILIKE %s
                ORDER BY p.name
            """, (search_query, search_query))
        else:
            cur.execute("""
                SELECT p.*, i.stock_quantity 
                FROM products p
                LEFT JOIN inventory i ON p.product_id = i.product_id
                ORDER BY p.name
            """)
        
        products = cur.fetchall()
        return jsonify(products), 200
    except Exception as e:
        return jsonify({'message': 'Failed to fetch products', 'error': str(e)}), 500
    finally:
        cur.close()
        conn.close()

@products_bp.route('/products', methods=['POST'])
@token_required
def create_product(payload):
    # Check if user is admin
    if payload.get('role') != 'Admin':
        return jsonify({'message': 'Admin access required'}), 403
        
    data = request.get_json()
    
    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    
    try:
        cur.execute("""
            INSERT INTO products (name, pack_size, sku, gst_rate, purchase_rate, selling_rate)
            VALUES (%s, %s, %s, %s, %s, %s)
            RETURNING product_id
        """, (
            data.get('name'),
            data.get('pack_size'),
            data.get('sku'),
            data.get('gst_rate'),
            data.get('purchase_rate'),
            data.get('selling_rate')
        ))
        
        product_id = cur.fetchone()['product_id']
        
        # Initialize inventory for the new product
        cur.execute("""
            INSERT INTO inventory (product_id, stock_quantity)
            VALUES (%s, %s)
        """, (product_id, data.get('initial_stock', 0)))
        
        conn.commit()
        
        # Fetch the created product
        cur.execute("""
            SELECT p.*, i.stock_quantity 
            FROM products p
            LEFT JOIN inventory i ON p.product_id = i.product_id
            WHERE p.product_id = %s
        """, (product_id,))
        
        product = cur.fetchone()
        return jsonify(product), 201
    except Exception as e:
        conn.rollback()
        return jsonify({'message': 'Failed to create product', 'error': str(e)}), 500
    finally:
        cur.close()
        conn.close()

@products_bp.route('/products/<int:product_id>', methods=['PUT'])
@token_required
def update_product(payload, product_id):
    # Check if user is admin
    if payload.get('role') != 'Admin':
        return jsonify({'message': 'Admin access required'}), 403
        
    data = request.get_json()
    
    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    
    try:
        cur.execute("""
            UPDATE products 
            SET name = %s, pack_size = %s, sku = %s, gst_rate = %s, purchase_rate = %s, selling_rate = %s
            WHERE product_id = %s
        """, (
            data.get('name'),
            data.get('pack_size'),
            data.get('sku'),
            data.get('gst_rate'),
            data.get('purchase_rate'),
            data.get('selling_rate'),
            product_id
        ))
        
        if cur.rowcount == 0:
            return jsonify({'message': 'Product not found'}), 404
            
        conn.commit()
        
        # Fetch the updated product
        cur.execute("""
            SELECT p.*, i.stock_quantity 
            FROM products p
            LEFT JOIN inventory i ON p.product_id = i.product_id
            WHERE p.product_id = %s
        """, (product_id,))
        
        product = cur.fetchone()
        return jsonify(product), 200
    except Exception as e:
        conn.rollback()
        return jsonify({'message': 'Failed to update product', 'error': str(e)}), 500
    finally:
        cur.close()
        conn.close()

@products_bp.route('/products/<int:product_id>', methods=['DELETE'])
@token_required
def delete_product(payload, product_id):
    # Check if user is admin
    if payload.get('role') != 'Admin':
        return jsonify({'message': 'Admin access required'}), 403
        
    conn = get_db_connection()
    cur = conn.cursor()
    
    try:
        # Delete from inventory first (foreign key constraint)
        cur.execute("DELETE FROM inventory WHERE product_id = %s", (product_id,))
        
        # Delete the product
        cur.execute("DELETE FROM products WHERE product_id = %s", (product_id,))
        
        if cur.rowcount == 0:
            return jsonify({'message': 'Product not found'}), 404
            
        conn.commit()
        return jsonify({'message': 'Product deleted successfully'}), 200
    except Exception as e:
        conn.rollback()
        return jsonify({'message': 'Failed to delete product', 'error': str(e)}), 500
    finally:
        cur.close()
        conn.close()