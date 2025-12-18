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
        # Create emergency_contacts table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS emergency_contacts (
                contact_id INT AUTO_INCREMENT PRIMARY KEY,
                p_id INT NOT NULL,
                name VARCHAR(100) NOT NULL,
                contact_number VARCHAR(20) NOT NULL,
                relation VARCHAR(50),
                FOREIGN KEY (p_id) REFERENCES patient(p_id) ON DELETE CASCADE
            )
        """)
        print("Table 'emergency_contacts' created successfully.")

        # Optional: Migrate existing contacts from patient table if needed
        # For now, we will just leave the old columns as legacy or for fallback

        conn.commit()
    except mysql.connector.Error as err:
        print(f"Error: {err}")
    finally:
        cursor.close()
        conn.close()

if __name__ == "__main__":
    migrate()
