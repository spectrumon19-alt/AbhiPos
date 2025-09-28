#!/usr/bin/env python3
# verify_setup.py - Comprehensive verification script

import sys
import os
import importlib.util

def check_python_version():
    """Check if Python version is sufficient"""
    version = sys.version_info
    if version.major >= 3 and version.minor >= 7:
        print("✓ Python version OK ({})".format(sys.version.split()[0]))
        return True
    else:
        print("✗ Python version too old: {}".format(sys.version.split()[0]))
        return False

def check_file_exists(filename):
    """Check if a file exists"""
    if os.path.exists(filename):
        print("✓ {} exists".format(filename))
        return True
    else:
        print("✗ {} not found".format(filename))
        return False

def check_module_import(module_name):
    """Check if a module can be imported"""
    try:
        importlib.import_module(module_name)
        print("✓ {} module imports correctly".format(module_name))
        return True
    except ImportError as e:
        print("✗ {} module import failed: {}".format(module_name, e))
        return False

def check_required_files():
    """Check if all required files exist"""
    required_files = [
        "app.py",
        "db.py",
        "auth.py",
        "schema.sql",
        "requirements.txt",
        "routes/__init__.py",
        "routes/auth.py",
        "routes/products.py",
        "routes/sales.py",
        "routes/inventory.py",
        "routes/reports.py",
        "routes/admin.py",
        "index.html",
        "login.html",
        "dashboard.html",
        "purchase.html",
        "inventory.html",
        "reports.html",
        "admin.html",
        "receipt.html",
        "styles.css",
        "sales.js"
    ]
    
    all_good = True
    for file in required_files:
        if not check_file_exists(file):
            all_good = False
    
    return all_good

def check_required_modules():
    """Check if all required modules can be imported"""
    required_modules = [
        "flask",
        "flask_cors",
        "psycopg2",
        "passlib",
        "jwt",
        "dotenv"
    ]
    
    all_good = True
    for module in required_modules:
        if not check_module_import(module):
            all_good = False
    
    return all_good

def main():
    print("POS System Verification")
    print("=" * 30)
    
    # Check Python version
    python_ok = check_python_version()
    print()
    
    # Check required files
    print("Checking required files...")
    files_ok = check_required_files()
    print()
    
    # Check required modules
    print("Checking required modules...")
    modules_ok = check_required_modules()
    print()
    
    # Summary
    if python_ok and files_ok and modules_ok:
        print("🎉 All checks passed! Your POS system is ready.")
        print("\nNext steps:")
        print("1. Configure your database in the .env file")
        print("2. Run: python init_db.py")
        print("3. Run: python app.py")
        print("4. Access at http://localhost:5000")
        return 0
    else:
        print("❌ Some checks failed. Please review the errors above.")
        return 1

if __name__ == "__main__":
    sys.exit(main())