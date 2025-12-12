from db import get_db_connection


def get_patient_name_glucose_info_update(p_id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    sql= """
        SELECT name, gl_b_breakfast, gl_a_breakfast, gl_b_lunch, gl_b_dinner, updated_on
        FROM patient
        WHERE p_id = %s
    """
    cursor.execute(sql, (p_id,))
    patient = cursor.fetchone()
    conn.close()
    return patient



def get_patient_details(p_id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    sql= """
        SELECT name, dob, phone, weight, gender,
        gl_b_breakfast, gl_a_breakfast, gl_b_lunch, gl_b_dinner
        FROM patient WHERE p_id = %s
    """
    cursor.execute(sql, (p_id,))
    patient = cursor.fetchone()
    return patient



def update_patient_details(dob, phone, weight, gender, gl_b_breakfast, gl_a_breakfast, gl_b_lunch, gl_b_dinner, updated_on, p_id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    sql= """
            UPDATE patient SET
                dob = %s,
                phone = %s,
                weight = %s,
                gender = %s,
                gl_b_breakfast = %s,
                gl_a_breakfast = %s,
                gl_b_lunch = %s,
                gl_b_dinner = %s,
                updated_on = %s
            WHERE p_id = %s
        """
    cursor.execute(sql, (dob, phone, weight, gender, gl_b_breakfast, gl_a_breakfast, gl_b_lunch, gl_b_dinner, updated_on, p_id))

    conn.commit() #changes in DB will be saved
    cursor.close()
    conn.close()
    

def get_verified_doctor_details():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    sql= """
        SELECT d_id, name, designation, location, email, phone 
        FROM doctor 
        WHERE verified = 1 AND designation IS NOT NULL 
        AND location IS NOT NULL AND phone IS NOT NULL
    """
    cursor.execute(sql)
    doctor = cursor.fetchall()
    cursor.close()
    conn.close()

    return doctor

def filter_doctor_by_area(area):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    sql="SELECT * FROM doctor WHERE area = %s"
    
    cursor.execute(sql, (area,))
    doctor = cursor.fetchall()
    cursor.close()
    conn.close()

    return doctor

def get_distinct_area():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    sql="SELECT DISTINCT area FROM doctor WHERE area IS NOT NULL"
    
    cursor.execute(sql)
    distinct_area_dictionary= cursor.fetchall()
    distinct_area_lst = [row['area'] for row in distinct_area_dictionary]
    cursor.close()
    conn.close()

    return distinct_area_lst






def get_patient_prescription(p_id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    sql= "SELECT pres_id, d_id, detail, date, morning, afternoon, night FROM prescription WHERE p_id = %s"
    cursor.execute(sql, (p_id,))
    prescriptions = cursor.fetchall()
    return prescriptions


# Fetch doctor names for each prescription
def get_doctor_name_for_each_prescription(prescription):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    sql= "SELECT name FROM doctor WHERE d_id = %s"

    cursor.execute(sql, (prescription['d_id'],))
    doctor = cursor.fetchone()

    cursor.close()
    conn.close()
    return doctor

    


def get_appointment_details(p_id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    sql=  "SELECT app_id, d_id, appointment_type, date, time, confirmation, checked FROM appointment WHERE p_id = %s"

    #Fetching appointments
    cursor.execute(sql, (p_id,))
    appointments = cursor.fetchall()

    cursor.close()
    conn.close()
    return appointments


# Fetching doctor name for each appointment
def get_doctor_name_for_each_appointment(appointment):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    sql= "SELECT name FROM doctor WHERE d_id = %s"
    cursor.execute(sql, (appointment['d_id'],))
    doc = cursor.fetchone()
    
    cursor.close()
    conn.close()
    return doc

def get_patient_required_fields(p_id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    sql= """
        SELECT name, dob, weight, gender,
               gl_b_breakfast, gl_a_breakfast,
               gl_b_lunch, gl_b_dinner 
        FROM patient 
        WHERE p_id = %s
        """
    cursor.execute(sql, (p_id,))
    required_fields= cursor.fetchone()
    
    cursor.close()
    conn.close()
    return required_fields

def get_doctor_schedule(d_id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    sql = """
        SELECT monday, tuesday, wednesday, thursday, friday, saturday, sunday, telemedicine_days 
        FROM doctor_schedule 
        WHERE d_id = %s
    """
    cursor.execute(sql, (d_id,))
    schedule = cursor.fetchone()
    
    cursor.close()
    conn.close()
    return schedule

'''def check_existing_appointment(p_id, date):
    conn = get_db_connection()
    cursor = conn.cursor()
    sql = "SELECT * FROM appointment WHERE p_id = %s AND date = %s" #need some change here 
    cursor.execute(sql, (p_id, date))
    appointment_exist = cursor.fetchone()
    cursor.close()
    conn.close()
    return appointment_exist is not None'''
#new code angshu
def check_existing_appointment(p_id, date):
    conn = get_db_connection()
    cursor = conn.cursor()
    sql = "SELECT * FROM appointment WHERE p_id = %s AND date = %s"
    cursor.execute(sql, (p_id, date))
    appointment_exist = cursor.fetchone()
    cursor.fetchall()  # ✅ consume remaining results if any
    cursor.close()     # ✅ explicitly close cursor
    conn.close()
    return appointment_exist is not None


def get_column_value(d_id, day):
    conn = get_db_connection()
    cursor = conn.cursor()
    sql = f"SELECT `{day}` FROM doctor_schedule WHERE d_id = %s"
    cursor.execute(sql, (d_id,))
    
    column_value = cursor.fetchone()
    cursor.close()
    conn.close()
    return column_value[0] if column_value else None
    


def insert_appointment(d_id, p_id, date, time, appointment_type):
    conn = get_db_connection()
    cursor = conn.cursor()
    sql = "INSERT INTO appointment (d_id, p_id, date, time, appointment_type) VALUES (%s, %s, %s, %s, %s)"
    cursor.execute(sql, (d_id, p_id, date, time, appointment_type))
    conn.commit()
    cursor.close()
    conn.close()
    return True
    

def insert_sos_alert(p_id, name, latitude, longitude):
    location = f"{latitude},{longitude}"
    
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    # Check if the p_id already exists
    cursor.execute("SELECT p_id FROM sos_alerts WHERE p_id = %s", (p_id,))
    result = cursor.fetchone()

    if result:
        # p_id exists → update the existing row
        cursor.execute("""
        REPLACE INTO sos_alerts (p_id, name, location)
        VALUES (%s, %s, %s)
    """, (p_id, name, location))
    else:
        # p_id does not exist → insert new row
        cursor.execute("""
            INSERT INTO sos_alerts (p_id, name, location)
            VALUES (%s, %s, %s)
        """, (p_id, name, location))

    conn.commit()
    cursor.close()
    conn.close()


#new code angshu
def is_duplicate_telemedicine(p_id, date, time):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    sql = "SELECT * FROM appointment WHERE p_id = %s AND date = %s AND time = %s AND appointment_type = %s"
    cursor.execute(sql, (p_id, date, time, 'telemedicine'))
    existing = cursor.fetchone()
    cursor.close()
    conn.close()
    return existing is not None


# new for patient notification by angshu

# Fetch active notifications for a patient
# Fetch active notifications for a patient
def get_patient_notifications(p_id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT id, message, status, timestamp 
        FROM patient_notifications 
        WHERE p_id = %s 
          AND status IN ('unread', 'read') 
        ORDER BY timestamp DESC
    """, (p_id,))
    notifications = cursor.fetchall()
    cursor.close()
    conn.close()
    return notifications

# Dismiss a notification
def dismiss_patient_notification(notif_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE patient_notifications
        SET status = 'dismissed'
        WHERE id = %s
    """, (notif_id,))
    conn.commit()
    cursor.close()
    conn.close()
def create_notification_for_appointment_action(app_id, action):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    # Fetch p_id, date, time for the appointment
    cursor.execute("SELECT p_id, date, time FROM appointment WHERE app_id = %s", (app_id,))
    appointment = cursor.fetchone()

    if appointment:
        p_id = appointment['p_id']
        date = appointment['date']
        time = appointment['time']

        # Build the notification message based on action
        if action == 'Confirm':
            message = f"Your appointment on {date} at {time} has been Confirmed ✅"
        elif action == 'Cancel':
            message = f"Your appointment on {date} at {time} has been Cancelled ❌"
        elif action == 'Reschedule':
            message = f"Doctor requested to reschedule your appointment on {date} at {time} 🔁"
        else:
            message = f"Update on your appointment for {date} at {time}"

        # Insert the notification
        cursor2 = conn.cursor()
        cursor2.execute("""
            INSERT INTO patient_notifications (p_id, message, app_id)
            VALUES (%s, %s, %s)
        """, (p_id, message, app_id))
        conn.commit()
        cursor2.close()

    cursor.close()
    conn.close()
#new code angshu
from datetime import datetime

def get_time_based_medication_reminder(p_id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    # Get latest prescription for the patient
    cursor.execute("""
        SELECT date, morning, afternoon, night
        FROM prescription
        WHERE p_id = %s
        ORDER BY date DESC
        LIMIT 1
    """, (p_id,))
    prescription = cursor.fetchone()
    cursor.close()
    conn.close()

    if not prescription:
        return None  # No prescriptions found

    # Determine current time slot
    now = datetime.now().time()
    hour = now.hour

    if 6 <= hour < 12:
        slot = 'morning'
    elif 12 <= hour < 18:
        slot = 'afternoon'
    else:
        slot = 'night'

    message = prescription.get(slot)
    date = prescription.get('date')

    if message:
        display = f"💊 {slot.capitalize()} Medication prescribed on ({date}): {message}"
    else:
        display = f"💊 {slot.capitalize()} Medication ({date}): You have no medication for this time."

    return display

def get_food_sugar_level(food_item):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT Sugar_level FROM sugar_lvl WHERE Food = %s", (food_item,))
    result = cursor.fetchone()
    cursor.close()
    conn.close()
    return result['Sugar_level'] if result else None


def get_diet_plan_by_age_and_gender(age, gender):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    # Determine which age range this falls under
    if age < 18:
        age_range = '10 to 17'
    elif 18 <= age <= 20:
        age_range = '18 to 20'
    elif 21 <= age <= 25:
        age_range = '21 to 25'
    elif 26 <= age <= 30:
        age_range = '25 to 30'
    elif 31 <= age <= 40:
        age_range = '31 to 40'
    elif 41 <= age <= 50:
        age_range = '40 to 50'
    elif 51 <= age <= 60:
        age_range = '50 to 60'
    elif 61 <= age <= 70:
        age_range = '60 to 70'
    else:
        age_range = '70+'

    
    cursor.execute("SELECT male_plan, female_plan FROM diet WHERE age_range = %s", (age_range,))
    diet_plan_row = cursor.fetchone()
    cursor.close()
    conn.close()

    if gender.lower() == 'male':
        return diet_plan_row['male_plan']
    else:
        return diet_plan_row['female_plan']


#nahian m4
def get_patient_notices(p_id):
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)

    query = """
        SELECT * FROM notices
        WHERE 
          recipient_type = 'patient'
            OR recipient_type = 'both'
            OR (recipient_type = 'specific_patient' AND recipient_id = %s)
        ORDER BY date DESC
    """
    cursor.execute(query, (p_id,))
    notices = cursor.fetchall()

    cursor.close()
    connection.close()
    return notices


#============ LABIBA M1 Starts =====================
def get_patient_name_glucose_info_update(p_id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    sql= """
        SELECT name, gl_b_breakfast, gl_a_breakfast, gl_b_lunch, gl_b_dinner, updated_on
        FROM patient
        WHERE p_id = %s
    """
    cursor.execute(sql, (p_id,))
    patient = cursor.fetchone()
    conn.close()
    return patient

def get_latest_SMBG_routine(p_id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)


    sql = """
        SELECT prescription.weekly_smbg,
               prescription.date,
               doctor.name AS doctor_name
        FROM prescription
        JOIN doctor ON prescription.d_id = doctor.d_id
        WHERE prescription.p_id = %s
        ORDER BY prescription.date DESC
    """
    cursor.execute(sql, (p_id,))
    prescriptions = cursor.fetchall()


    cursor.close()
    conn.close()


    return prescriptions


def get_patient_name_glucose_info_update(p_id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    sql= """
        SELECT name, gl_b_breakfast, gl_a_breakfast, gl_b_lunch, gl_b_dinner, updated_on
        FROM patient
        WHERE p_id = %s
    """
    cursor.execute(sql, (p_id,))
    patient = cursor.fetchone()
    conn.close()
    return patient



def get_patient_details(p_id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    sql= """
        SELECT name, email, dob, phone, weight, gender,
        gl_b_breakfast, gl_a_breakfast, gl_b_lunch, gl_b_dinner, followup_date
        FROM patient WHERE p_id = %s
    """
    cursor.execute(sql, (p_id,))
    patient = cursor.fetchone()
    return patient
#============ LABIBA M1 ends =====================



#============ LABIBA M2 starts =====================


def filter_doctor_by_area(area):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    sql="SELECT * FROM doctor WHERE area = %s"
    
    cursor.execute(sql, (area,))
    doctor = cursor.fetchall()
    cursor.close()
    conn.close()

    return doctor

def get_verified_doctor_details():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    sql= """
        SELECT d_id, name, designation, location, email, phone 
        FROM doctor 
        WHERE verified = 1 AND designation IS NOT NULL 
        AND location IS NOT NULL AND phone IS NOT NULL
    """
    cursor.execute(sql)
    doctor = cursor.fetchall()
    cursor.close()
    conn.close()

    return doctor

def get_distinct_area():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    sql="SELECT DISTINCT area FROM doctor WHERE area IS NOT NULL"
    
    cursor.execute(sql)
    distinct_area_dictionary= cursor.fetchall()
    distinct_area_lst = [row['area'] for row in distinct_area_dictionary]
    cursor.close()
    conn.close()

    return distinct_area_lst


def get_patient_details(p_id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    sql= """
        SELECT name, email, dob, phone, weight, gender,
        gl_b_breakfast, gl_a_breakfast, gl_b_lunch, gl_b_dinner, followup_date
        FROM patient WHERE p_id = %s
    """
    cursor.execute(sql, (p_id,))
    patient = cursor.fetchone()
    return patient

def update_patient_details(dob, phone, weight, gender, gl_b_breakfast, gl_a_breakfast, gl_b_lunch, gl_b_dinner, updated_on, p_id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    sql= """
            UPDATE patient SET
                dob = %s,
                phone = %s,
                weight = %s,
                gender = %s,
                gl_b_breakfast = %s,
                gl_a_breakfast = %s,
                gl_b_lunch = %s,
                gl_b_dinner = %s,
                updated_on = %s
            WHERE p_id = %s
        """
    cursor.execute(sql, (dob, phone, weight, gender, gl_b_breakfast, gl_a_breakfast, gl_b_lunch, gl_b_dinner, updated_on, p_id))

    conn.commit() #changes in DB will be saved
    cursor.close()
    conn.close()


def get_doctor_weekly_schedule(d_id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    sql = """
        SELECT * 
        FROM doctor_schedule 
        WHERE d_id = %s
    """
    cursor.execute(sql, (d_id,))
    schedule = cursor.fetchone()
    
    cursor.close()
    conn.close()
    return schedule



def get_doctor_slots(d_id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT * FROM doctor_slot WHERE d_id = %s
    """, (d_id,))
    slots = cursor.fetchone()

    cursor.close()
    conn.close()
    return slots

def get_patient_required_fields(p_id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    sql= """
        SELECT name, dob, weight, gender,
               gl_b_breakfast, gl_a_breakfast,
               gl_b_lunch, gl_b_dinner
        FROM patient 
        WHERE p_id = %s
        """
    cursor.execute(sql, (p_id,))
    required_fields= cursor.fetchone()
    
    cursor.close()
    conn.close()
    return required_fields

def check_appointment_next_week(p_id, today, next_7_days):
    """
    Returns appointment details if the patient has
    a pending or confirmed appointment within next 7 days,
    otherwise returns None.
    """

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    sql = """
        SELECT app_id, d_id, p_id, date, time, confirmation, appointment_type
        FROM appointment
        WHERE p_id = %s 
          AND date BETWEEN %s AND %s
          AND confirmation IN (0, 1) 
        LIMIT 1
    """

    cursor.execute(sql, (p_id, today, next_7_days))
    row = cursor.fetchone()

    cursor.close()
    conn.close()

    # Automatically returns a dictionary (or None if no result)
    return row


def update_doctor_slot(d_id, slot_col):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute(f"UPDATE doctor_slot SET {slot_col} = 1 WHERE d_id = %s", (d_id,))
    conn.commit()

    cursor.close()
    conn.close()

def insert_appointment(d_id, p_id, date, time, appointment_type):
    conn = get_db_connection()
    cursor = conn.cursor()
    if appointment_type== "inperson":
        appointment_type= "in-person"
    sql = "INSERT INTO appointment (d_id, p_id, date, time, appointment_type) VALUES (%s, %s, %s, %s, %s)"
    cursor.execute(sql, (d_id, p_id, date, time, appointment_type))
    conn.commit()
    cursor.close()
    conn.close()
    return True
#============ LABIBA M2 ends =====================

