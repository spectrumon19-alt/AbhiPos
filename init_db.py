#!/usr/bin/env python3
# init_db.py - Script to initialize the database

import psycopg2
import os
from dotenv import load_dotenv

def init_database():
    """Initialize the database with schema and sample data"""
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
        
        print("Connected to database successfully")
        
        # Read and execute schema.sql
        with open('schema.sql', 'r') as f:
            schema = f.read()
            
        # Split by semicolon and execute each statement
        statements = schema.split(';')
        for statement in statements:
            if statement.strip():
                try:
                    cur.execute(statement)
                    print(f"Executed: {statement[:50]}...")
                except Exception as e:
                    print(f"Warning: {e}")
        
        conn.commit()
        print("Database initialized successfully!")
        
        # Verify tables were created
        cur.execute("""
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_schema = 'public'
        """)
        
        tables = cur.fetchall()
        print(f"Tables in database: {[table[0] for table in tables]}")
        
        cur.close()
        conn.close()
        
    except Exception as e:
        print(f"Error initializing database: {e}")

if __name__ == "__main__":
    init_database()