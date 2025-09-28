#!/usr/bin/env python3
# test_setup.py - Test script to verify POS system setup

import os
import sys
import psycopg2
from dotenv import load_dotenv

def test_database_connection():
    """Test database connection"""
    try:
        load_dotenv()
        
        conn = psycopg2.connect(
            host=os.environ.get('DB_HOST', 'localhost'),
            database=os.environ.get('DB_NAME', 'pos_db'),
            user=os.environ.get('DB_USER', 'postgres'),
            password=os.environ.get('DB_PASSWORD', 'password')
        )
        
        cur = conn.cursor()
        cur.execute("SELECT version();")
        version = cur.fetchone()
        
        print("✓ Database connection successful")
        if version:
            print(f"  Database version: {version[0]}")
        
        cur.close()
        conn.close()
        return True
    except Exception as e:
        print("✗ Database connection failed")
        print(f"  Error: {e}")
        return False

def test_python_packages():
    """Test if required Python packages are installed"""
    required_packages = [
        'flask',
        'flask_cors',
        'psycopg2',
        'passlib',
        'PyJWT',
        'dotenv'
    ]
    
    missing_packages = []
    
    for package in required_packages:
        try:
            if package == 'flask':
                __import__('flask')
            elif package == 'flask_cors':
                __import__('flask_cors')
            elif package == 'psycopg2':
                __import__('psycopg2')
            elif package == 'passlib':
                __import__('passlib')
            elif package == 'PyJWT':
                __import__('jwt')
            elif package == 'dotenv':
                __import__('dotenv')
        except ImportError as e:
            missing_packages.append(f"{package} ({str(e)})")
    
    if missing_packages:
        print("✗ Missing Python packages:")
        for package in missing_packages:
            print(f"  - {package}")
        return False
    else:
        print("✓ All required Python packages are installed")
        return True

def test_env_file():
    """Test if .env file exists and has required variables"""
    if not os.path.exists('.env'):
        print("✗ .env file not found")
        return False
    
    load_dotenv()
    
    required_vars = ['DB_HOST', 'DB_NAME', 'DB_USER', 'DB_PASSWORD', 'SECRET_KEY']
    missing_vars = []
    
    for var in required_vars:
        if not os.environ.get(var):
            missing_vars.append(var)
    
    if missing_vars:
        print("✗ Missing environment variables in .env file:")
        for var in missing_vars:
            print(f"  - {var}")
        return False
    else:
        print("✓ .env file has all required variables")
        return True

def main():
    print("POS System Setup Test")
    print("=" * 30)
    
    tests = [
        test_env_file,
        test_python_packages,
        test_database_connection
    ]
    
    results = []
    for test in tests:
        results.append(test())
        print()
    
    passed = sum(results)
    total = len(results)
    
    print(f"Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! Your POS system is ready to run.")
        return 0
    else:
        print("❌ Some tests failed. Please check the errors above.")
        return 1

if __name__ == "__main__":
    sys.exit(main())