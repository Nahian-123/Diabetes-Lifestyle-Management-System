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


#=====================APPOINTMENTS (NAHIAN M2)=============================

def get_pending_appointments(d_id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    query = '''
        SELECT appointment.*, patient.name, patient.phone, patient.email AS patient_email, patient.weight, patient.gender, patient.dob,
               patient.gl_b_breakfast, patient.gl_a_breakfast, patient.gl_b_lunch, patient.gl_b_dinner
        FROM appointment
        JOIN patient ON appointment.p_id = patient.p_id
        WHERE appointment.d_id = %s AND (appointment.confirmation = 0 OR appointment.confirmation = 1) 
              AND appointment.checked = 0
    '''

   

    cursor.execute(query, (d_id,))
    appointments = cursor.fetchall()
    cursor.close()
    conn.close()
    
    return appointments

def update_appointment_status(app_id, d_id, action):
    conn = get_db_connection()
    cursor = conn.cursor()
    #Pending: 0
    action_map = {
        'Confirm': 1,
        'Cancel': 2,
        'Reschedule': 3
    }
    
    if action == 'Checked':
        cursor.execute("UPDATE appointment SET checked = 1 WHERE app_id = %s AND d_id = %s", (app_id, d_id))
    elif action in action_map:
        cursor.execute("UPDATE appointment SET confirmation = %s WHERE app_id = %s AND d_id = %s",
                       (action_map[action], app_id, d_id))

    conn.commit()
    cursor.close()
    conn.close()
#==========NAHIIAN M2 ends===========


#==========LABIBA M1 starts=====================================================================
def insert_prescription(p_id, d_id, date, weekly_smbg):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO prescription (p_id, d_id, date, weekly_smbg)
        VALUES (%s, %s, %s, %s)
    """, (p_id, d_id, date, weekly_smbg))
    conn.commit()
    cursor.close()
    conn.close()



#==========LABIBA M1 ends=====================================================================

#==========LABIBA M2 starts=====================================================================

def get_doctor_by_id(d_id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM doctor WHERE d_id = %s", (d_id,))
    doctor = cursor.fetchone()
    cursor.close()
    conn.close()
    return doctor

#==========LABIBA M2 ends=====================================================================




#==========NAHIAN M3 (appointment mail) starts=====================================================================
def get_appointment_details(app_id):  # For Email System
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    query = """
        SELECT 
            appointment.app_id,
            appointment.date,
            appointment.time,
            appointment.confirmation,
            appointment.appointment_type,   
            patient.name AS patient_name,
            patient.email AS patient_email,
            doctor.name AS doctor_name
        FROM appointment
        JOIN patient ON appointment.p_id = patient.p_id
        JOIN doctor ON appointment.d_id = doctor.d_id
        WHERE appointment.app_id = %s
    """

    print("DEBUG app_id:", app_id)
    cursor.execute(query, (app_id,))
    data = cursor.fetchone()
    print("DEBUG SQL DATA:", data)

    cursor.close()
    conn.close()
    return data

#==========NAHIAN M3 ends=====================================================================

#==========Angshu m3+m4 starts=====================================================================
def update_doctor_profile(d_id, designation, phone, location):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE doctor SET designation = %s, phone = %s, location = %s
        WHERE d_id = %s
    """, (designation, phone, location, d_id))
    conn.commit()
    cursor.close()
    conn.close()
#==========Angshu m3+m4 ends=====================================================================