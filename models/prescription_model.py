from db import get_db_connection
#===================NAHIAN M3===========================
def get_all_doctor_previous_prescriptions(d_id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    query = """
        SELECT *
        FROM prescription
        WHERE d_id = %s
        ORDER BY date DESC
    """
    
    cursor.execute(query, (d_id,))
    result = cursor.fetchall()
    cursor.close()
    conn.close()
    return result


def search_patient_for_prescription(p_id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    query = """
        SELECT *
        FROM patient
        WHERE p_id = %s
    """

    cursor.execute(query, (p_id,))
    result = cursor.fetchone()
    
    conn.close()
    return result


def get_patient_info_for_prescription(p_id, d_id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    query = """
        SELECT 
            p.p_id, p.name, p.weight, p.gender, 
            p.gl_b_breakfast, p.gl_b_lunch, p.gl_b_dinner,
            a.app_id, a.appointment_type, a.confirmation, a.checked,
            TIMESTAMPDIFF(YEAR, p.dob, CURDATE()) AS age
        FROM patient p
        JOIN appointment a ON p.p_id = a.p_id
        WHERE p.p_id = %s AND a.d_id = %s
    """

    cursor.execute(query, (p_id, d_id))
    result = cursor.fetchone()
    
    conn.close()
    return result


def get_doctor_info_for_prescription(d_id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    query = """
        SELECT *
        FROM doctor
        WHERE d_id = %s
    """

    cursor.execute(query, (d_id,))
    result = cursor.fetchone()
    
    conn.close()
    return result


def insert_prescription(p_id, d_id, detail, date, morning, afternoon, night, weekly_smbg):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO prescription (p_id, d_id, detail, date, morning, afternoon, night, weekly_smbg)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
    """, (p_id, d_id, detail, date, morning, afternoon, night, weekly_smbg))
    conn.commit()
    cursor.close()
    conn.close()


def get_prescriptions_by_patient(p_id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    query = """
        SELECT *
        FROM prescription
        WHERE p_id = %s
        ORDER BY date DESC
    """
    
    cursor.execute(query, (p_id,))
    result = cursor.fetchall()
    cursor.close()
    conn.close()
    return result


def get_patient_prescription(p_id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    sql= "SELECT * FROM prescription WHERE p_id = %s"
    cursor.execute(sql, (p_id,))
    prescriptions = cursor.fetchall()
    return prescriptions

def get_doctor_name_for_each_prescription(prescription):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    sql= "SELECT name FROM doctor WHERE d_id = %s"

    cursor.execute(sql, (prescription['d_id'],))
    doctor = cursor.fetchone()

    cursor.close()
    conn.close()
    return doctor


def get_prescription_by_id(pres_id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT *
        FROM prescription
        WHERE pres_id = %s
    """, (pres_id,))

    prescription = cursor.fetchone()
    cursor.close()
    conn.close()

    return prescription

#============NAHIAN M3 ENDS HERE==================  