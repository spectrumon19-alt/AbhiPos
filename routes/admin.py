from flask import Blueprint, request, jsonify
from db import get_db_connection
from auth import token_required, admin_required, hash_password
from psycopg2.extras import RealDictCursor

admin_bp = Blueprint('admin', __name__)

@admin_bp.route('/admin/users', methods=['GET'])
@admin_required
def get_users(payload):
    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    
    try:
        cur.execute("""
            SELECT user_id, username, role, created_at FROM users
            ORDER BY created_at DESC
        """)
        
        users = cur.fetchall()
        return jsonify(users), 200
    except Exception as e:
        return jsonify({'message': 'Failed to fetch users', 'error': str(e)}), 500
    finally:
        cur.close()
        conn.close()

@admin_bp.route('/admin/users', methods=['POST'])
@admin_required
def create_user(payload):
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    role = data.get('role')
    
    if not username or not password or not role:
        return jsonify({'message': 'Username, password, and role are required'}), 400
    
    if role not in ['Admin', 'Cashier']:
        return jsonify({'message': 'Role must be either Admin or Cashier'}), 400
    
    conn = get_db_connection()
    cur = conn.cursor()
    
    try:
        # Hash the password
        hashed_password = hash_password(password)
        
        cur.execute("""
            INSERT INTO users (username, password_hash, role)
            VALUES (%s, %s, %s)
        """, (username, hashed_password, role))
        
        conn.commit()
        return jsonify({'message': 'User created successfully'}), 201
    except Exception as e:
        conn.rollback()
        return jsonify({'message': 'Failed to create user', 'error': str(e)}), 500
    finally:
        cur.close()
        conn.close()

@admin_bp.route('/admin/users/<int:user_id>/reset-password', methods=['PUT'])
@admin_required
def reset_user_password(payload, user_id):
    data = request.get_json()
    new_password = data.get('new_password')
    
    if not new_password:
        return jsonify({'message': 'New password is required'}), 400
    
    conn = get_db_connection()
    cur = conn.cursor()
    
    try:
        # Hash the new password
        hashed_password = hash_password(new_password)
        
        cur.execute("""
            UPDATE users 
            SET password_hash = %s 
            WHERE user_id = %s
        """, (hashed_password, user_id))
        
        if cur.rowcount == 0:
            return jsonify({'message': 'User not found'}), 404
            
        conn.commit()
        return jsonify({'message': 'Password reset successfully'}), 200
    except Exception as e:
        conn.rollback()
        return jsonify({'message': 'Failed to reset password', 'error': str(e)}), 500
    finally:
        cur.close()
        conn.close()

@admin_bp.route('/admin/invoices', methods=['GET'])
@admin_required
def get_all_invoices(payload):
    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    
    try:
        cur.execute("""
            SELECT 
                si.invoice_id,
                si.invoice_number,
                si.invoice_date,
                si.customer_name,
                si.total_amount,
                si.status,
                u.username as created_by
            FROM sales_invoices si
            JOIN users u ON si.user_id = u.user_id
            ORDER BY si.invoice_date DESC
        """)
        
        invoices = cur.fetchall()
        return jsonify(invoices), 200
    except Exception as e:
        return jsonify({'message': 'Failed to fetch invoices', 'error': str(e)}), 500
    finally:
        cur.close()
        conn.close()