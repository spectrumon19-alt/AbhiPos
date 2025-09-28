from db import get_db_connection

def check_users():
    """Check users in the database"""
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute('SELECT user_id, username, password_hash, role FROM users')
        users = cur.fetchall()
        print('Users in database:')
        for user in users:
            print(f"ID: {user[0]}, Username: {user[1]}, Role: {user[3]}")
            print(f"  Password hash: {user[2][:20]}...")  # Show first 20 chars
        cur.close()
        conn.close()
    except Exception as e:
        print(f"Error checking users: {e}")

if __name__ == "__main__":
    check_users()