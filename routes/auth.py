from flask import Blueprint, request, jsonify
from db import get_db_connection
from auth import hash_password, verify_password, generate_token
from psycopg2.extras import RealDictCursor

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    
    if not username or not password:
        return jsonify({'message': 'Username and password are required'}), 400
    
    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    
    try:
        cur.execute(
            'SELECT user_id, username, password_hash, role FROM users WHERE username = %s',
            (username,)
        )
        user = cur.fetchone()
        
        if user and verify_password(password, user['password_hash']):
            token = generate_token(user['user_id'], user['role'])
            return jsonify({
                'token': token,
                'user': {
                    'user_id': user['user_id'],
                    'username': user['username'],
                    'role': user['role']
                }
            }), 200
        else:
            return jsonify({'message': 'Invalid credentials'}), 401
    except Exception as e:
        print(f"Login error: {e}")  # Debug print
        return jsonify({'message': 'Login failed', 'error': str(e)}), 500
    finally:
        cur.close()
        conn.close()

@auth_bp.route('/users/me', methods=['GET'])
def get_current_user():
    token = None
    if 'Authorization' in request.headers:
        auth_header = request.headers['Authorization']
        try:
            token = auth_header.split(" ")[1]  # Bearer <token>
        except IndexError:
            return jsonify({'message': 'Token is missing!'}), 401

    if not token:
        return jsonify({'message': 'Token is missing!'}), 401

    from auth import verify_token  # Import here to avoid circular import
    payload = verify_token(token)
    if not payload:
        return jsonify({'message': 'Token is invalid!'}), 401

    return jsonify({
        'user_id': payload.get('user_id'),
        'username': payload.get('username'),
        'role': payload.get('role')
    }), 200