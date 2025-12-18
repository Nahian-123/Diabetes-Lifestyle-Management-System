import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from db import get_db_connection

def migrate_urgent_care():
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        # Create Ambulance Table
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS ambulance (
            amb_id INT AUTO_INCREMENT PRIMARY KEY,
            driver_name VARCHAR(100),
            contact_number VARCHAR(20),
            latitude DECIMAL(10, 8),
            longitude DECIMAL(10, 8),
            is_available BOOLEAN DEFAULT TRUE
        )
        """)
        
        # Create Emergency Requests Table
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS emergency_requests (
            req_id INT AUTO_INCREMENT PRIMARY KEY,
            patient_id INT,
            location_lat DECIMAL(10, 8),
            location_lon DECIMAL(10, 8),
            assigned_ambulance_id INT,
            status VARCHAR(20) DEFAULT 'Pending',
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (assigned_ambulance_id) REFERENCES ambulance(amb_id)
        )
        """)
        
        # Seed Ambulances (Around Dhaka for demo)
        cursor.execute("SELECT COUNT(*) FROM ambulance")
        if cursor.fetchone()[0] == 0:
            print("Seeding ambulances...")
            ambulances = [
                ('Rahim Khan', '01711000001', 23.8103, 90.4125), # Gulshan
                ('Karim Ullah', '01711000002', 23.7940, 90.4043), # Banani
                ('Sokina Begum', '01711000003', 23.7330, 90.3950), # Uniliver/Shahbagh area
            ]
            cursor.executemany(
                "INSERT INTO ambulance (driver_name, contact_number, latitude, longitude, is_available) VALUES (%s, %s, %s, %s, TRUE)",
                ambulances
            )
            conn.commit()
            
        print("Urgent Care migration successful.")
    except Exception as e:
        print(f"Migration error: {e}")
    finally:
        cursor.close()
        conn.close()

if __name__ == "__main__":
    migrate_urgent_care()
