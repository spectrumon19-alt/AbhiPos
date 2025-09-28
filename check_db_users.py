import psycopg2
import os
from dotenv import load_dotenv

def check_users():
    """Check users in the database"""
    load_dotenv()
    
    try:
        # Connect to PostgreSQL
        conn = psycopg2.connect(
            host=os.environ.get('DB_HOST', 'localhost'),
            database=os.environ.get('DB_NAME', 'pos_db'),
            user=os.environ.get('DB_USER', 'postgres'),
            password=os.environ.get('DB_PASSWORD', 'password')
        )
        
        cur = conn.cursor()
        
        # Get all users
        cur.execute("SELECT user_id, username, role, created_at FROM users ORDER BY user_id")
        users = cur.fetchall()
        
        print("Users in database:")
        print("-" * 50)
        for user in users:
            print(f"ID: {user[0]}, Username: {user[1]}, Role: {user[2]}, Created: {user[3]}")
        
        cur.close()
        conn.close()
        
    except Exception as e:
        print(f"Error checking users: {e}")

if __name__ == "__main__":
    check_users()