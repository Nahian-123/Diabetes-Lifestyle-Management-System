import sys
import os

# Add parent directory to path to import db
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import mysql.connector
from db import get_db_connection
from werkzeug.security import generate_password_hash

def migrate_table(cursor, table_name, id_column, password_column='password'):
    print(f"Checking table: {table_name}...")
    try:
        cursor.execute(f"SELECT {id_column}, {password_column} FROM {table_name}")
        users = cursor.fetchall()
        
        updated_count = 0
        for user in users:
            user_id = user[0]
            password = user[1]
            
            if not password:
                continue
                
            if not password.startswith('scrypt:'):
                # Needs hashing
                new_hash = generate_password_hash(password)
                cursor.execute(f"UPDATE {table_name} SET {password_column} = %s WHERE {id_column} = %s", (new_hash, user_id))
                updated_count += 1
                
        print(f"  - Updated {updated_count} passwords in {table_name}.")
    except mysql.connector.Error as err:
        print(f"  - Error processing {table_name}: {err}")

def migrate():
    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        # Doctor table (PK: d_id)
        migrate_table(cursor, 'doctor', 'd_id')
        
        # Admin table (PK: id) - note: standard naming often uses 'id' for admin
        # I'll check if it fails, but plan said 'id'
        migrate_table(cursor, 'admin', 'id')
        
        # Patient table (PK: p_id)
        migrate_table(cursor, 'patient', 'p_id')

        conn.commit()
        print("Password migration completed successfully.")

    except mysql.connector.Error as err:
        print(f"Error: {err}")
    finally:
        cursor.close()
        conn.close()

if __name__ == "__main__":
    migrate()
