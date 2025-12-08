# models/doctor_model.py
from db import get_db_connection


def get_doctor_name(d_id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT name FROM doctor WHERE d_id = %s", (d_id,))
    result = cursor.fetchone()
    cursor.close()
    conn.close()
    return result['name'] if result else None

def get_doctor_notices(d_id):
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)

    query = """
        SELECT * FROM notices
        WHERE 
            recipient_type = 'doctor'
            OR recipient_type = 'both'
            OR (recipient_type = 'specific_doctor' AND recipient_id = %s)
        ORDER BY date DESC
    """
    cursor.execute(query, (d_id,))
    results = cursor.fetchall()

    cursor.close()
    connection.close()
    return results
