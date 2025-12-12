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