import psycopg2
import os
from psycopg2.extras import RealDictCursor

def get_db_connection():
    conn = psycopg2.connect(
        host=os.environ.get('DB_HOST', 'localhost'),
        database=os.environ.get('DB_NAME', 'pos_db'),
        user=os.environ.get('DB_USER', 'postgres'),
        password=os.environ.get('DB_PASSWORD', 'password')
    )
    return conn

def init_db():
    conn = None
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        
        # Check if tables exist by querying the products table
        cur.execute("""
            SELECT EXISTS (
                SELECT FROM information_schema.tables 
                WHERE table_name = 'products'
            );
        """)
        
        result = cur.fetchone()
        exists = result[0] if result else False
        
        # If tables don't exist, create them
        if not exists:
            with open('schema.sql', 'r') as f:
                schema = f.read()
                # Split by semicolon to execute each statement separately
                statements = schema.split(';')
                for statement in statements:
                    if statement.strip():
                        cur.execute(statement)
            
            conn.commit()
        
        cur.close()
    except Exception as e:
        print(f"Database initialization error: {e}")
    finally:
        if conn:
            conn.close()