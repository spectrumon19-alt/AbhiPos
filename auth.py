import jwt
import datetime
from functools import wraps
from flask import request, jsonify
import os
from passlib.hash import pbkdf2_sha256
from db import get_db_connection

SECRET_KEY = os.environ.get('SECRET_KEY', 'dev-secret-key')

def hash_password(password):
    return pbkdf2_sha256.hash(password)

def verify_password(password, hash):
    try:
        return pbkdf2_sha256.verify(password, hash)
    except Exception as e:
        print(f"Password verification error: {e}")
        return False

def generate_token(user_id, role):
    payload = {
        'user_id': user_id,
        'role': role,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=24)
    }
    return jwt.encode(payload, SECRET_KEY, algorithm='HS256')

def verify_token(token):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
        return payload
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if 'Authorization' in request.headers:
            auth_header = request.headers['Authorization']
            try:
                token = auth_header.split(" ")[1]  # Bearer <token>
            except IndexError:
                return jsonify({'message': 'Token is missing!'}), 401

        if not token:
            return jsonify({'message': 'Token is missing!'}), 401

        payload = verify_token(token)
        if not payload:
            return jsonify({'message': 'Token is invalid!'}), 401

        return f(payload, *args, **kwargs)

    return decorated

def admin_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if 'Authorization' in request.headers:
            auth_header = request.headers['Authorization']
            try:
                token = auth_header.split(" ")[1]  # Bearer <token>
            except IndexError:
                return jsonify({'message': 'Token is missing!'}), 401

        if not token:
            return jsonify({'message': 'Token is missing!'}), 401

        payload = verify_token(token)
        if not payload:
            return jsonify({'message': 'Token is invalid!'}), 401

        if payload.get('role') != 'Admin':
            return jsonify({'message': 'Admin access required!'}), 403

        return f(payload, *args, **kwargs)

    return decorated