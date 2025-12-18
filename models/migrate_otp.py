from db import get_db_connection

def migrate():
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        print("Adding otp_code column...")
        cursor.execute("ALTER TABLE doctor ADD COLUMN otp_code VARCHAR(6)")
        print("Adding otp_expiry column...")
        cursor.execute("ALTER TABLE doctor ADD COLUMN otp_expiry DATETIME")
        conn.commit()
        print("Migration successful.")
    except Exception as e:
        print(f"Migration error (might already exist): {e}")
    finally:
        cursor.close()
        conn.close()

if __name__ == "__main__":
    migrate()
