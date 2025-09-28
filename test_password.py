from passlib.hash import pbkdf2_sha256
from db import get_db_connection

def test_password_verification():
    """Test password verification"""
    # Test with a known password and hash
    password = "admin123"
    hash = "$pbkdf2-sha256$29000$d875X8vZu3dOCcG4N8Y4Bw$XXjGT1jpZKChZ80biGTQNRId.tZ.QsfRGWuEFnRLQuyI"
    
    print(f"Testing password: {password}")
    print(f"Testing hash: {hash}")
    
    try:
        result = pbkdf2_sha256.verify(password, hash)
        print(f"Verification result: {result}")
    except Exception as e:
        print(f"Verification error: {e}")
    
    # Now check what's in the database
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT username, password_hash FROM users WHERE username = 'admin'")
    user = cur.fetchone()
    
    if user:
        username, db_hash = user
        print(f"\nDatabase user: {username}")
        print(f"Database hash: {db_hash}")
        
        try:
            result = pbkdf2_sha256.verify("admin123", db_hash)
            print(f"Database verification result: {result}")
        except Exception as e:
            print(f"Database verification error: {e}")
    else:
        print("User not found in database")
    
    cur.close()
    conn.close()

if __name__ == "__main__":
    test_password_verification()