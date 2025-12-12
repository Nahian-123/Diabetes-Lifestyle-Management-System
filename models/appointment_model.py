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