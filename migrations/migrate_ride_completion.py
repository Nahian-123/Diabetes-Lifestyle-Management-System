import sys
import os

# Add parent directory to path to import db
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import mysql.connector
from db import get_db_connection

def migrate():
    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        # Check if column exists
        cursor.execute("SHOW COLUMNS FROM emergency_requests LIKE 'ride_completed'")
        result = cursor.fetchone()
        
        if not result:
            cursor.execute("""
                ALTER TABLE emergency_requests
                ADD COLUMN ride_completed TINYINT(1) DEFAULT 0
            """)
            print("Column 'ride_completed' added successfully.")
        else:
            print("Column 'ride_completed' already exists.")

        conn.commit()
    except mysql.connector.Error as err:
        print(f"Error: {err}")
    finally:
        cursor.close()
        conn.close()

if __name__ == "__main__":
    migrate()
