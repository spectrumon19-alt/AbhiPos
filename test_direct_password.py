from passlib.hash import pbkdf2_sha256
from db import get_db_connection

def test_direct_verification():
    """Test password verification directly"""
    # Get the hash from the database
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT password_hash FROM users WHERE username = 'admin'")
    result = cur.fetchone()
    
    if result:
        db_hash = result[0]
        print(f"Database hash: {db_hash}")
        print(f"Hash length: {len(db_hash)}")
        
        # Test verification
        try:
            is_valid = pbkdf2_sha256.verify("admin123", db_hash)
            print(f"Password verification result: {is_valid}")
        except Exception as e:
            print(f"Verification error: {e}")
            print(f"Error type: {type(e)}")
    else:
        print("User not found")
    
    cur.close()
    conn.close()

if __name__ == "__main__":
    test_direct_verification()