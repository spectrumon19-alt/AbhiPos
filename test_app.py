#!/usr/bin/env python3
# Simple test to verify the application structure

import sys
import os

# Add the current directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_imports():
    """Test that all modules can be imported without errors"""
    try:
        from app import create_app
        print("✓ app module imported successfully")
        
        from auth import hash_password, verify_password, generate_token, verify_token
        print("✓ auth module imported successfully")
        
        from db import get_db_connection, init_db
        print("✓ db module imported successfully")
        
        from routes.auth import auth_bp
        print("✓ auth routes imported successfully")
        
        from routes.products import products_bp
        print("✓ products routes imported successfully")
        
        from routes.sales import sales_bp
        print("✓ sales routes imported successfully")
        
        from routes.inventory import inventory_bp
        print("✓ inventory routes imported successfully")
        
        from routes.reports import reports_bp
        print("✓ reports routes imported successfully")
        
        from routes.admin import admin_bp
        print("✓ admin routes imported successfully")
        
        print("\n🎉 All imports successful! The application structure is correct.")
        return True
        
    except Exception as e:
        print(f"❌ Import error: {e}")
        return False

if __name__ == "__main__":
    print("Testing POS System Application Structure")
    print("=" * 50)
    success = test_imports()
    sys.exit(0 if success else 1)