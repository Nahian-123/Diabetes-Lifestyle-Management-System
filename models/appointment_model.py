from db import get_db_connection

#================ LABIBA M2 GOOGLE CALENDER API================
def get_appointment_by_id(app_id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    query = "SELECT * FROM appointment WHERE app_id = %s"
    cursor.execute(query, (app_id,))
    
    appointment = cursor.fetchone()
    
    cursor.close()
    conn.close()
    
    return appointment

#======LABIBA M2 ends==============================================
<<<<<<< HEAD


def get_patient_appointments_with_zoom(p_id):
    """
    Get all appointments for a patient including zoom meeting links
    """
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    query = """
        SELECT a.*, d.name as doctor_name
        FROM appointment a
        JOIN doctor d ON a.d_id = d.d_id
        WHERE a.p_id = %s
        ORDER BY a.date DESC, a.time DESC
    """
    cursor.execute(query, (p_id,))
    
    appointments = cursor.fetchall()
    
    cursor.close()
    conn.close()
    
    return appointments




=======
#======Angshu M2 strats==============================================
def get_latest_appointment():
    """
    Fetches the single row for the appointment with the highest app_id.
    """
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        query = "SELECT * FROM appointment ORDER BY app_id DESC LIMIT 1"
        cursor.execute(query)
        return cursor.fetchone()
        
    finally:
        cursor.close()
        conn.close()
#======Angshu M2 ends==============================================
>>>>>>> 0076bea61cea1d974306a23f63511e0b476af2e1
