import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from db import get_db_connection

def migrate_patient_contacts():
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        print("Adding emergency_contact_name column...")
        cursor.execute("ALTER TABLE patient ADD COLUMN emergency_contact_name VARCHAR(100)")
        print("Adding emergency_contact_number column...")
        cursor.execute("ALTER TABLE patient ADD COLUMN emergency_contact_number VARCHAR(20)")
        
        # Seed dummy data for existing patients
        cursor.execute("UPDATE patient SET emergency_contact_name = 'Mom', emergency_contact_number = '01711000000' WHERE emergency_contact_name IS NULL")
        
        conn.commit()
        print("Patient contacts migration successful.")
    except Exception as e:
        print(f"Migration error (cols might exist): {e}")
    finally:
        cursor.close()
        conn.close()

if __name__ == "__main__":
    migrate_patient_contacts()
