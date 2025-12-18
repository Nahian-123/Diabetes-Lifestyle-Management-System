from flask import Flask, request, jsonify, render_template, redirect, url_for, session, flash
import mysql.connector
from datetime import datetime, date, time, timedelta
from functools import wraps
import os
import base64
import requests  # Added for Zoom API calls
#import jwt  # Added for JWT token generation
#import time
import json
import markdown, bleach #new line by angshy
# # DeepFace for verification
# from deepface import DeepFace

# Import models
from models.user_model import login_user, register_user, validate_email

from models.patient_model import get_patient_notifications, get_time_based_medication_reminder,get_patient_notifications, get_patient_name_glucose_info_update,get_patient_notices,get_confirmed_app_id, get_unpaid_telemed,populate_telemed_payment #last 3 imports by angshu
from models.user_model import login_user, register_user, validate_email
from models.doctor_model import get_doctor_name, get_doctor_notices, update_doctor_profile #new line by angshu
from models.admin_model import insert_notice,get_dashboard_stats
from models.payment_model import verify_card_details, finalize_telemedicine_transaction  # Angshu M2 payment model imports
from models.appointment_model import get_latest_appointment  # Angshu M2 appointment model import
# For Google Calendar API
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import Flow
import os
from models.ai_assistant_model import get_llama_response #new line by angshu
# Google Calendar API Setup
os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'  # Allow http:// for local dev
CLIENT_SECRETS_FILE = "client_secret.json"
SCOPES = ["https://www.googleapis.com/auth/calendar"]

app = Flask(__name__, template_folder="templates")
app.secret_key = 'your_secret_key_here'

# MySQL Database Configuration
db_config = {
    'host': '127.0.0.1',
    'user': 'root',
    'password': '',
    'database': 'dms'
}

# Establish DB connection
def get_db_connection():
    return mysql.connector.connect(**db_config)


#############################################
# LOGIN REQUIRED DECORATOR
#############################################
def login_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if 'user_id' not in session:
            flash('Please login to access this page', 'error')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated


#############################################
@app.route('/')
def index():
    return redirect(url_for('login'))



from models.user_model import login_user, register_user, validate_email, verify_otp
#############################################
# REGISTER ROUTE  - SIMPLIFIED (no extra field needed)
#############################################
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':


        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        role = request.form['user'].lower()


        if not username or not email or not password or not role:
            flash('All fields are required', 'error')
            return redirect(url_for('register'))
       
        if not validate_email(email):
            flash('Please enter a valid email address', 'error')
            return redirect(url_for('register'))
       
        if len(password) < 3:
            flash('Password must be at least 3 characters long', 'error')
            return redirect(url_for('register'))
       
        result = register_user(username, email, password, role)
       
        if result['success']:
            if result.get('redirect_otp'):
                 flash(result['message'], 'info')
                 return render_template('verify_account.html', email=result.get('email'))
            
            flash(result['message'], 'success')
            return redirect(url_for('login'))
        else:
            flash(result['message'], 'error')
            return redirect(url_for('register'))
   
    return render_template('register.html')

@app.route('/verify_account', methods=['POST'])
def verify_account():
    email = request.form.get('email')
    otp = request.form.get('otp')
    
    result = verify_otp(email, otp)
    
    if result['success']:
        flash(result['message'], 'success')
        return redirect(url_for('login'))
    else:
        flash(result['message'], 'error')
        return render_template('verify_account.html', email=email)



#############################################
# LOGIN ROUTE - STORES real_email FOR GOOGLE
#############################################
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':


        email = request.form['email']
        password = request.form['password']

       
#=======

        user_data = login_user(email, password)
       
        if user_data:
            session['user_id'] = user_data['user_id']
            session['email'] = user_data['email']
            session['role'] = user_data['role']
            session['name'] = user_data['name']
           
            if user_data.get('real_email'):
                session['real_email'] = user_data['real_email']


            flash('Login successful!', 'success')  


            if session['role'] == 'doctor':
                return redirect(url_for('doctor_dashboard'))


            if session['role'] == 'admin':
                return redirect(url_for('admin_dashboard'))
            elif session['role'] == 'patient':
                return redirect(url_for('patient_dashboard'))
       
        flash('Invalid email or password', 'error')  


    return render_template('login.html')







# @app.route('/patient_dashboard', endpoint='patient_dashboard')
# def patient_dashboard():
#     if 'user_id' not in session:
#         flash("Session timed out. Please login again.")
#         return redirect(url_for('login'))

#     p_id = session['user_id']

#     patient = get_patient_name_glucose_info_update(p_id)
#     if not patient:
#         return "Patient not found", 404

#     glucose_data = [
#         patient.get('gl_b_breakfast', 0),
#         patient.get('gl_a_breakfast', 0),
#         patient.get('gl_b_lunch', 0),
#         patient.get('gl_b_dinner', 0)
#     ]
    
#     notices = get_patient_notices(p_id)  #rakha lagbe
#     notifications = get_patient_notifications(p_id)  # 🆕 fetch notifications angshu for doctor appointment confirm/cancel/reschedule #rakha lagbe 
#     medication_message = get_time_based_medication_reminder(p_id) #rakha lagbe


#     return render_template('patient_dashboard.html', name=patient['name'], p_id=p_id, updated_on=patient['updated_on'], glucose_data=glucose_data, notifications=notifications, medication_message=medication_message, notices=notices)

#############################################
# ZOOM INTEGRATION CONFIGURATION
#############################################
ZOOM_ACCOUNT_ID = os.getenv('ZOOM_ACCOUNT_ID', 'your_zoom_account_id')
ZOOM_CLIENT_ID = os.getenv('ZOOM_CLIENT_ID', 'your_zoom_client_id')
ZOOM_CLIENT_SECRET = os.getenv('ZOOM_CLIENT_SECRET', 'your_zoom_client_secret')

def get_zoom_access_token():
    """Generate Zoom OAuth access token using Server-to-Server OAuth"""
    token_url = f"https://zoom.us/oauth/token?grant_type=account_credentials&account_id={ZOOM_ACCOUNT_ID}"
    
    auth_header = base64.b64encode(f"{ZOOM_CLIENT_ID}:{ZOOM_CLIENT_SECRET}".encode()).decode()
    headers = {
        'Authorization': f'Basic {auth_header}',
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    
    try:
        response = requests.post(token_url, headers=headers)
        response.raise_for_status()
        return response.json().get('access_token')
    except Exception as e:
        print(f"[v0] Error getting Zoom access token: {str(e)}")
        return None

def create_zoom_meeting(topic, start_time, duration=30):
    """
    Create a Zoom meeting
    
    Args:
        topic: Meeting topic/title
        start_time: Meeting start time (datetime object)
        duration: Meeting duration in minutes (default 30)
    
    Returns:
        dict with meeting details (join_url, meeting_id, password) or None if failed
    """
    access_token = get_zoom_access_token()
    
    if not access_token:
        print("[v0] Failed to get Zoom access token")
        return None
    
    # Zoom API endpoint to create a meeting (using 'me' as user_id for the account owner)
    create_meeting_url = "https://api.zoom.us/v2/users/me/meetings"
    
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json'
    }
    
    meeting_data = {
        "topic": topic,
        "type": 2,  # Scheduled meeting
        "start_time": start_time.strftime("%Y-%m-%dT%H:%M:%S"),
        "duration": duration,
        "timezone": "Asia/Dhaka",
        "settings": {
            "host_video": True,
            "participant_video": True,
            "join_before_host": False,
            "mute_upon_entry": True,
            "waiting_room": True,
            "audio": "both",
            "auto_recording": "none"
        }
    }
    
    try:
        response = requests.post(create_meeting_url, json=meeting_data, headers=headers)
        response.raise_for_status()
        meeting_info = response.json()
        
        return {
            'join_url': meeting_info.get('join_url'),
            'meeting_id': meeting_info.get('id'),
            'password': meeting_info.get('password', '')
        }
    except Exception as e:
        print(f"[v0] Error creating Zoom meeting: {str(e)}")
        return None

#############################################

@app.route('/admin')
@login_required
def admin_dashboard():
    stats = get_dashboard_stats()
    return render_template('admin.html', 
                          id=session.get('user_id'),
                          email=session.get('email'),
                          pending_count=stats['pending_count'],
                          pending_app=stats['pending_app'],
                          total_doctors=stats['total_doctors'],
                          total_patients=stats['total_patients'],
                          timestamp=stats['timestamp'])

@app.route('/doctor_dashboard', endpoint='doctor_dashboard')
def doctor_dashboard():
    d_id= session['user_id']
    if 'user_id' not in session:  #######Finally activate this
        flash("Session timed out. Please login again.")
        return redirect(url_for('login'))  # Add your login route
    name = get_doctor_name(d_id)
    notices = get_doctor_notices(d_id)
    return render_template('doctor_dashboard.html', name=name, d_id=d_id, notices=notices)

@app.route('/admin_send_notice', methods=['GET', 'POST'])
def admin_send_notice():
    if 'user_id' not in session:
        flash("Session timed out. Please login again.")
        return redirect(url_for('login'))

    admin_id = session['user_id']

    if request.method == 'POST':
        recipient_type = request.form['recipient_type']
        recipient_id = request.form.get('recipient_id')  # Optional
        message = request.form['message']
        date = datetime.today().strftime('%Y-%m-%d')

        if not message:
            flash("Notice message cannot be empty.", "danger")
            return redirect(url_for('admin_send_notice'))

        if recipient_id == '':
            recipient_id = None  # Only needed for specific targets

        insert_notice(admin_id, recipient_type, recipient_id, message, date)
        flash("Notice sent successfully!", "success")
        return redirect(url_for('admin_send_notice'))

    return render_template('admin_send_notice.html')

#=========NAHIAN M1===========

from models.doctor_schedule_model import save_schedule, get_schedule, create_or_reset_slots, get_slots
from datetime import datetime, timezone, timedelta 

def generate_slot_times(start_time_str, count=8, duration=30):
    start = datetime.strptime(start_time_str, "%H:%M")
    times = []

    for i in range(count):
        st = start + timedelta(minutes=i * duration)
        et = st + timedelta(minutes=duration)
        times.append(f"{st.strftime('%H:%M')} - {et.strftime('%H:%M')}")
    
    return times

@app.route("/update_schedule", methods=["GET", "POST"])
def update_schedule():
    if 'user_id' not in session:
        flash("Session timed out. Please login again.")
        return redirect(url_for('login'))

    d_id = session['user_id']

    #LOAD SCHEDULE + SLOT DATA FIRST ----
    schedule = get_schedule(d_id)
    slots = get_slots(d_id)

    #HANDLE NEW DOCTOR (no schedule yet)
    if schedule["day1"] is None: #then all others are None bc required fields
            return render_template(
                "doctor_schedule.html",
                schedule=schedule,
                slots=slots,
                day1_times="",
                day2_times="",
                teleday_times=""
            )
    
    def clean_time(t):
        if not t:
            return ""
        if isinstance(t, str):
            return t[:5]
        try:
            total_seconds = int(t.total_seconds())
            hours = total_seconds // 3600
            minutes = (total_seconds % 3600) // 60
            return f"{hours:02d}:{minutes:02d}"
        except:
            return ""

    schedule['day1_starttime'] = clean_time(schedule['day1_starttime'])
    schedule['day2_starttime'] = clean_time(schedule['day2_starttime'])
    schedule['teleday_starttime'] = clean_time(schedule['teleday_starttime'])

    day1_times = generate_slot_times(schedule['day1_starttime'])
    day2_times = generate_slot_times(schedule['day2_starttime'])
    teleday_times = generate_slot_times(schedule['teleday_starttime'])

    # ========== POST REQUEST ==========

    if request.method == "POST":

        # ---- CHECK DAY ----
        bd_time = datetime.now(timezone(timedelta(hours=6)))
        today = bd_time.strftime("%A")

        if today != "Friday":
            flash("You can update your schedule only on Fridays.", "error")
            return render_template(
                "doctor_schedule.html",
                schedule=schedule,
                slots=slots,
                day1_times=day1_times,
                day2_times=day2_times,
                teleday_times=teleday_times, d_id=d_id
            )

        # ---- Updating schedule ----
        day1 = request.form.get("day1")
        day1_start = request.form.get("day1_start")
        day2 = request.form.get("day2")
        day2_start = request.form.get("day2_start")
        teleday = request.form.get("teleday")
        teleday_start = request.form.get("teleday_start")

        # Check duplicate days
        days = [day1, day2, teleday]
        if len(days) != len(set(days)):
            flash("Error: You cannot pick the same day more than once.", "error")
            return redirect(url_for("update_schedule"))

        # Save schedule
        save_schedule(d_id, day1, day2, teleday, day1_start, day2_start, teleday_start)
        create_or_reset_slots(d_id)

        flash("Schedule updated successfully!", "success")
        return redirect(url_for("update_schedule"))

    # ===== GET REQUEST =====
    return render_template(
        "doctor_schedule.html",
        schedule=schedule,
        slots=slots,
        day1_times=day1_times,
        day2_times=day2_times,
        teleday_times=teleday_times, d_id=d_id
    )

#==========NAHIIAN M1 ends===========

#==========NAHIIAN M2 starts===========

from models.doctor_model import get_pending_appointments, update_appointment_status 
from datetime import date

def calculate_age(dob):
    today = date.today()
    return today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))

@app.route('/doctor_appointments', methods=['GET', 'POST']) 
def doctor_appointments():
    d_id= session['user_id']
    if 'user_id' not in session:  
        flash("Session timed out. Please login again.")
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        app_id = request.form.get('app_id')
        action = request.form.get('action')

        update_appointment_status(app_id, d_id, action)

        #==========NAHIIAN M3 starts===========       
        # Fetch appointment details
        appointment = get_appointment_details(app_id)
        print("DEBUG APPOINTMENT:", appointment)

        patient_email = appointment['patient_email']
        patient_name = appointment['patient_name']
        doctor_name = appointment['doctor_name']
        appointment_type = appointment.get("appointment_type")  # telemedicine 
        appointment_date = appointment.get("date")

        # ------------------------------------------
        # EMAIL SENDING FOR ALL ACTIONS
        # ------------------------------------------
        if action == "Reschedule":
            send_appointment_email(app_id, appointment_date, patient_email, patient_name, doctor_name, "requested for reschedule")

        elif action == "Confirm":
            send_appointment_email(app_id,appointment_date, patient_email, patient_name, doctor_name, "Confirmed", appointment_type)

        elif action == "Cancel":
            send_appointment_email(app_id, appointment_date, patient_email, patient_name, doctor_name, "Cancelled")
        #==========NAHIIAN M3 ends===========

        if action == "Confirm":
            # Get appointment details
            from models.appointment_model import get_appointment_by_id
            appointment = get_appointment_by_id(app_id)
            
            if appointment and appointment.get('appointment_type') == 'telemedicine':
                # Create Zoom meeting
                appointment_datetime = datetime.combine(
                    appointment['date'],
                    datetime.strptime(appointment['time'], "%I:%M %p").time()
                )
                
                meeting_topic = f"Telemedicine Appointment - Dr. {get_doctor_name(d_id)}"
                zoom_meeting = create_zoom_meeting(meeting_topic, appointment_datetime, duration=30)
                
                if zoom_meeting:
                    # Store Zoom meeting link in database with correct table name
                    conn = get_db_connection()
                    cursor = conn.cursor()
                    cursor.execute("""
                        UPDATE appointment 
                        SET zoom_meeting_link = %s, zoom_meeting_id = %s, zoom_password = %s
                        WHERE app_id = %s
                    """, (zoom_meeting['join_url'], zoom_meeting['meeting_id'], zoom_meeting['password'], app_id))
                    conn.commit()
                    cursor.close()
                    conn.close()
                    
                    flash('Appointment confirmed and Zoom meeting created!', 'success')
                else:
                    flash('Appointment confirmed but Zoom meeting creation failed. Please create manually.', 'warning')
            else:
                flash('Appointment confirmed!', 'success')
            
            # Google Calendar integration (if exists)
            try:
                create_google_calendar_event(app_id)
            except Exception as e:
                print(f"Google Calendar integration failed: {e}")
                pass

        else:
            flash('Updated appointment successfully!', 'success')
            
        return redirect(url_for('doctor_appointments'))

    # GET - Fetch pending or confirmed + unchecked appointments
    appointments = get_pending_appointments(d_id)
    
    # Calculate age for each appointment
    for appointment in appointments:
        appointment['age'] = calculate_age(appointment['dob'])

    return render_template('doctor_appointments.html', appointments=appointments, d_id=d_id)

#==========NAHIIAN M2 ends===========

#==========LABIBA M1 starts=====================================================================

from models.doctor_model import insert_prescription
from models.patient_model import get_patient_name_glucose_info_update, get_latest_SMBG_routine

#This is updated by Nahian in Nahian M3 prescriptions part
# @app.route('/doctor_prescriptions', methods=['GET', 'POST'])
# def doctor_prescriptions():
#     d_id= session['user_id']
#     if 'user_id' not in session:  #######Finally activate this
#         flash("Session timed out. Please login again.")
#         return redirect(url_for('login'))  # Add your login route


#     if request.method == 'POST':
#         p_id = request.form['p_id']
#         weekly_smbg = request.form['weekly_smbg']
#         date = datetime.today().strftime('%Y-%m-%d')


#         # if not check_patient_appointment(p_id, d_id):
#         #     flash("This patient doesn't have a confirmed appointment with you.", "warning")
#         #     return redirect(url_for('doctor_prescriptions'))
       
#         insert_prescription(p_id, d_id, date, weekly_smbg)
#         flash('Prescription added successfully!', 'success')
#         return redirect(url_for('doctor_prescriptions'))


#     return render_template('doctor_prescriptions.html',d_id=d_id)

@app.route('/patient_dashboard', endpoint='patient_dashboard')
def patient_dashboard():
    if 'user_id' not in session:
        flash("Session timed out. Please login again.")
        return redirect(url_for('login'))

    p_id = session['user_id']
    patient = get_patient_name_glucose_info_update(p_id)
    medication_messages = get_time_based_medication_reminder(p_id) #new line by angshu
    if not patient:
        return "Patient not found", 404

    glucose_data = [
        patient.get('gl_b_breakfast', 0),
        patient.get('gl_a_breakfast', 0),
        patient.get('gl_b_lunch', 0),
        patient.get('gl_b_dinner', 0)
    ]
   
    # SMBG Routine
    prescriptions= get_latest_SMBG_routine(p_id)
    smbg_routine_details = {}
    notices= get_patient_notices(p_id) #new line by angshu
    # Find first non-null weekly_smbg
    for entry in prescriptions:
        if entry["weekly_smbg"] is not None:
            smbg_routine_details = {
                "status": "prescribed",
                "weekly_smbg": entry["weekly_smbg"],
                "doctor_name": entry["doctor_name"],
                "date": entry["date"]
            }
            break


    # If ALL entries had weekly_smbg == NULL
    if not smbg_routine_details:
        smbg_routine_details = {"status": "not_prescribed"}


  # Added Zoom meeting link display on patient dashboard
    zoom_meeting_link = patient.get('zoom_meeting_link')
    zoom_meeting_id = patient.get('zoom_meeting_id')
    zoom_password = patient.get('zoom_password')

    return render_template(
        'patient_dashboard.html',
        name=patient['name'],
        p_id=p_id,
        updated_on=patient['updated_on'],
        glucose_data=glucose_data,
        medication_message=medication_messages, #new line by angshu
        smbg_status=smbg_routine_details["status"],
        weekly_smbg=smbg_routine_details.get("weekly_smbg"),
        doctor_name=smbg_routine_details.get("doctor_name"),
        smbg_date=smbg_routine_details.get("date"),
        zoom_meeting_link=zoom_meeting_link,
        zoom_meeting_id=zoom_meeting_id,
        zoom_password=zoom_password,
        notices=notices) #new line by angshu  

#==========LABIBA M1 ends=====================================================================

#==========LABIBA M2 starts===================================================================

from models.patient_model import filter_doctor_by_area, get_verified_doctor_details, get_distinct_area
from models.patient_model import get_patient_details, update_patient_details

from models.patient_model import get_doctor_weekly_schedule, get_doctor_slots, get_patient_required_fields, check_appointment_next_week, update_doctor_slot, insert_appointment
from models.appointment_model import get_appointment_by_id

from models.patient_model import get_upcoming_patient_appointments,get_patient_appointments_with_details
from models.doctor_model import get_doctor_by_id


@app.route('/update_patient_profile', methods=['GET', 'POST'])
def update_patient_profile():
    p_id= session['user_id']
   
    if 'user_id' not in session:
        flash("Session timed out. Please login again.")
        return redirect(url_for('login')) 
    
 

    #fetching patient details
    patient = get_patient_details(p_id)
    if not patient:
        flash("No data found for this patient.")
        return redirect('/update_patient_profile')

    if request.method == 'POST':
        # Form values
        dob = request.form['dob']
        phone = request.form['phone']
        weight = request.form['weight']
        gender = request.form['gender']
        gl_b_breakfast = request.form['gl_b_breakfast']
        gl_a_breakfast = request.form['gl_a_breakfast']
        gl_b_lunch = request.form['gl_b_lunch']
        gl_b_dinner = request.form['gl_b_dinner']
        
        #Checking if glucose values changed
        values_changed = (
            float(gl_b_breakfast) != float(patient['gl_b_breakfast']) or
            float(gl_a_breakfast) != float(patient['gl_a_breakfast']) or
            float(gl_b_lunch) != float(patient['gl_b_lunch']) or
            float(gl_b_dinner) != float(patient['gl_b_dinner'])
        )
        updated_on = datetime.now() if values_changed else patient.get('updated_on')
        
        update_patient_details(dob, phone, weight, gender, gl_b_breakfast, gl_a_breakfast, gl_b_lunch, gl_b_dinner, updated_on, p_id)
        
        if not patient:
            flash("No data found for this patient.")
            return redirect('/update_patient_profile')
        else:
            flash("Patient profile updated successfully")
            return redirect('/patient_dashboard')
    
    return render_template('update_patient_profile.html', patient=patient) 


@app.route('/verified_doctor_list')
def verified_doctor_list():
    p_id = session['user_id']
    if 'user_id' not in session:
        flash("Session timed out. Please login again.")
        return redirect(url_for('login'))

    area = request.args.get('area')
    if area:
        doctor = filter_doctor_by_area(area)
    else:
        doctor = get_verified_doctor_details()   
    
    distinct_area_lst = get_distinct_area()
    return render_template('verified_doctor_list.html', doctor=doctor, areas=distinct_area_lst)

@app.route('/request_appointment', methods=['GET', 'POST'])
def request_appointment():
    # d_id comes from the doctor's info box request button click e.g. /request_appointment?d_id=5
    d_id = request.args.get('d_id')
    if 'user_id' not in session:
        flash("Session timed out. Please login again.")
        return redirect(url_for('login'))
    if not d_id:
        return redirect('/verified_doctor_list')

    p_id = session['user_id']

    # appointment_type and appointment_day are user inputs from the form (POST).
    # For a GET, they will be None.
    appointment_type = request.form.get('appointment_type')  # "telemedicine" or "inperson"
    appointment_day = request.form.get('appointment_day')  # will be the option value (we'll use index or key)

    # Get doctor schedule and slots from DB
    schedule = get_doctor_weekly_schedule(d_id)
    slot_data = get_doctor_slots(d_id)

    weekly_data = []

    # Build the list of day tuples based on chosen or available types
    # We always create weekly_data for any available schedule fields
    days_to_consider = []
    # Only include a day if the schedule row has the weekday and starttime filled
    if schedule:
        # day1, day2 and teleday keys must match DB column names
        days_to_consider.append(("day1", schedule.get("day1"), schedule.get("day1_starttime")))
        days_to_consider.append(("day2", schedule.get("day2"), schedule.get("day2_starttime")))
        days_to_consider.append(("teleday", schedule.get("teleday"), schedule.get("teleday_starttime")))

    # Helper to map weekday name -> next date for that weekday
    weekday_map = {
        "Sunday": 6, "Monday": 0, "Tuesday": 1,
        "Wednesday": 2, "Thursday": 3, "Friday": 4, "Saturday": 5
    }
    today = datetime.now().date()

    for (key, weekday, starttime) in days_to_consider:
        if not weekday or not starttime:
            continue

        # figure out the upcoming date for that weekday
        diff = (weekday_map[weekday] - today.weekday() + 7) % 7
        slot_date = today + timedelta(days=diff)

        # normalize_time may return a time object or expects timedelta; ensure we have a time
        starttime = normalize_time(starttime)
        if isinstance(starttime, time):
            start_dt = datetime.combine(slot_date, starttime)
        else:
            # fallback: assume it's already a datetime or convertible
            start_dt = datetime.combine(slot_date, time(8, 0))

        # Generate 8 slot start times (30-min intervals)
        slot_times = []
        for i in range(8):
            st = (start_dt + timedelta(minutes=i * 30)).strftime("%I:%M %p")
            slot_times.append(st)

        # Read status bits from slot_data, DB column names expected like "day1slot1" or "teledayslot1"
        # Build keys accordingly (key + "slot" + index)
        status_list = []
        for i in range(8):
            colname = f"{key}slot{i+1}"
            s = 1  # default assume booked if missing
            if slot_data and colname in slot_data:
                s = slot_data[colname]
            status_list.append("available" if int(s) == 0 else "booked")

        weekly_data.append({
            "key": key,             # "day1", "day2" or "teleday" — useful for client filtering
            "day": weekday,         # weekday string, e.g. "Monday"
            "date": slot_date.strftime("%Y-%m-%d"),
            "display_date": slot_date.strftime("%d-%m-%Y"),  # for dropdown display (dd-mm-yyyy)
            "slots": [
                {
                    "slot": i + 1,
                    "time": slot_times[i],
                    "status": status_list[i]
                } for i in range(8)
            ]
        })

    # Render the template; weekly_data is passed to client as JSON for JS to use
    return render_template(
        "request_appointment.html",
        d_id=d_id,
        p_id=p_id,
        appointment_type=appointment_type,
        appointment_day=appointment_day,
        weekly_data=weekly_data
    )

@app.route('/request_appointment_progress', methods=['POST'])
def request_appointment_progress():
    if 'user_id' not in session:
        flash("Session timed out. Please login again.")
        return redirect(url_for('login'))

    p_id = session['user_id']
    d_id = request.form.get('d_id')

    # Values from request_appointment form
    appointment_type = request.form.get('appointment_type')
    day_obj = request.form.get('appointment_day')    # JSON string: {"key": "day1", "date":"2025-01-13"}

    slot_number = request.form.get('selected_slot')

    if not appointment_type or not day_obj or not slot_number:
        flash("Error: Invalid appointment request. Please try again.")
        return redirect(url_for('request_appointment', d_id=d_id))

    # Decode appointment day
    day_data = json.loads(day_obj)
    # day_obj = request.form.get("appointment_day")  # e.g. "day1|2025-02-10"

    # day_key, appointment_date = day_obj.split("|")
    appointment_date = day_data["date"]
    day_key = day_data["key"]

    # Convert date → weekday name to compare with doctor_schedule
    appointment_day = convert_date_to_weekday(appointment_date)

    # Retrieve slot time
    # Note: This should ideally fetch the same schedule data as in request_appointment to ensure consistency.
    # For simplicity, we'll re-fetch; in a production system, consider passing this data or using a shared service.
    schedule = get_doctor_weekly_schedule(d_id)
    slot_data = get_doctor_slots(d_id)


    # Determine day_num (“day1”, “day2”, “teleday”)
    if appointment_day == schedule["day1"]:
        day_num = "day1"
    elif appointment_day == schedule["day2"]:
        day_num = "day2"
    elif appointment_day == schedule["teleday"]:
        day_num = "teleday"
    else:
        flash("Error: Invalid schedule day selected. Please try again.")
        return redirect(url_for('request_appointment', d_id=d_id))

    slot_column = f"{day_num}slot{slot_number}"

    # Generate slot_time again (same logic as request_appointment)
    # Fetch starting time
    start_time = normalize_time(schedule[f"{day_num}_starttime"])
    slot_date_obj = datetime.strptime(appointment_date, "%Y-%m-%d")
    start_dt = datetime.combine(slot_date_obj, start_time)
    slot_dt = start_dt + timedelta(minutes=(int(slot_number) - 1) * 30)
    slot_time = slot_dt.strftime("%I:%M %p")

    # --------- VALIDATION CHECKS ---------

    # 1. Profile check
    patient_fields = get_patient_required_fields(p_id)
    required_fields = [
        'name', 'dob', 'phone', 'weight', 'gender',
        'gl_b_breakfast', 'gl_a_breakfast',
        'gl_b_lunch', 'gl_b_dinner'
    ]
    # Check if all required fields are not None or empty string
    if  all(patient_fields.get(f)  in (None, '', 'None') for f in required_fields):
        flash("Error: Please complete your profile details (dob, phone, weight, gender, glucose levels) before booking an appointment.")
        return redirect(url_for('update_patient_profile')) # Redirect to profile update

    # 2. Followup date check
    today = datetime.now().date()
    patient_details = get_patient_details(p_id) # Fetch again to get fresh followup_date
    followup = patient_details.get("followup_date")

    if followup and today < followup:
        flash(f"Error: Your next follow-up is scheduled for {followup}. You cannot book a new appointment before this date.")
        return redirect(url_for('request_appointment', d_id=d_id))

    # 3. Next 7 days rule
    next_7 = today + timedelta(days=7)
    if check_appointment_next_week(p_id, today, next_7):
        flash("Error: You already have an appointment booked within the next 7 days. Please check your existing appointments.")
        return redirect(url_for('request_appointment', d_id=d_id))

    # 4. Slot availability
    if slot_data.get(slot_column) == 1:
        flash("Error: This slot is already booked. Please select another available slot.")
        return redirect(url_for('request_appointment', d_id=d_id))

    # Mark slot booked
    update_doctor_slot(d_id, slot_column)

    # Insert new appointment
    insert_appointment(d_id, p_id, appointment_date, slot_time, appointment_type)
    appointment= get_latest_appointment()
    if appointment["appointment_type"]=="telemedicine":
        populate_telemed_payment(appointment["app_id"]) #change here by Anghsu

    success = "Your appointment request has been successfully placed!"

    return render_template("request_appointment_progress.html",
                           success=success,
                           redirect_url=url_for('patient_dashboard'))

# Helper func for M2 LABIBA
def normalize_time(value):
    if isinstance(value, timedelta):
        total_seconds = int(value.total_seconds())
        return time(total_seconds // 3600, (total_seconds % 3600) // 60)
    return value

def convert_date_to_weekday(date_str):
    # Convert string to date object
    date_obj = datetime.strptime(date_str, "%Y-%m-%d")
    # Return weekday name
    return date_obj.strftime("%A")  

def convert_date_to_day_key(date_str):
    import datetime
    weekday = datetime.datetime.strptime(date_str, "%Y-%m-%d").weekday()
    return f"day{weekday+1}"  # Monday=1 ... Sunday=7

# GOOGLE CALENDER API =================================

@app.route("/authorize")
def authorize():
    print("DEBUG REDIRECT URI:", url_for("oauth2callback", _external=True))

    flow = Flow.from_client_secrets_file(
        CLIENT_SECRETS_FILE,
        scopes=SCOPES,
        redirect_uri=url_for("oauth2callback", _external=True)
    )
    authorization_url, state = flow.authorization_url(
        access_type="offline",
        include_granted_scopes="true",
        prompt="consent"
    )
    session["state"] = state
    return redirect(authorization_url)


@app.route("/oauth2callback")
def oauth2callback():
    state = session["state"]

    flow = Flow.from_client_secrets_file(
        CLIENT_SECRETS_FILE,
        scopes=SCOPES,
        state=state,
        redirect_uri=url_for("oauth2callback", _external=True)
    )

    flow.fetch_token(authorization_response=request.url)
    credentials = flow.credentials

    # Store credentials in session (or DB)
    session["google_credentials"] = {
        "token": credentials.token,
        "refresh_token": credentials.refresh_token,
        "token_uri": credentials.token_uri,
        "client_id": credentials.client_id,
        "client_secret": credentials.client_secret,
        "scopes": credentials.scopes,
    }
    print("Google Calendar linked successfully!", "success")
    
    flash("Google Calendar linked successfully!", "success")
    return redirect(url_for("doctor_appointments"))


def create_google_calendar_event(app_id):
    # Load tokens from session  # 1. Load saved Google credentials
    creds_data = session.get("google_credentials")
    if not creds_data:
        print("Please connect your Google Calendar first. warning")
        flash("Please connect your Google Calendar first.", "warning")
        return redirect(url_for("authorize"))

    creds = Credentials(
        token=creds_data["token"],
        refresh_token=creds_data["refresh_token"],
        token_uri=creds_data["token_uri"],
        client_id=creds_data["client_id"],
        client_secret=creds_data["client_secret"],
        scopes=creds_data["scopes"],
    )

    service = build("calendar", "v3", credentials=creds)
    
    # 2. Fetch appointment details
    # Fetch appointment + patient + doctor details from DB
    from models.appointment_model import get_appointment_by_id
    appointment = get_appointment_by_id(app_id)
    patient = get_patient_details(appointment["p_id"])
    doctor = get_doctor_by_id(appointment["d_id"])
    
    # 3. Build start/end datetime
    # Combine date + time → datetime
    date_str = str(appointment["date"])       # YYYY-MM-DD
    time_str = str(appointment["time"])       # HH:MM AM/PM

    # Build ISO datetime
    # Convert "YYYY-MM-DD" + "HH:MM AM/PM" → datetime object
    start_dt = datetime.strptime(f"{date_str} {time_str}", "%Y-%m-%d %I:%M %p")
    end_dt = start_dt + timedelta(minutes=30) # Assuming 30 min appointment duration

    # Create Google Calendar–ready ISO strings
    start_iso = start_dt.isoformat()
    end_iso = end_dt.isoformat()

    print("start_iso:",start_iso)
    print("end_iso:",end_iso)

    # Build event
    event = {
        "summary": f"DLMS Appointment with Dr. {doctor['name']}",
        "description": (
            f"Appointment ID: {appointment['app_id']}\n"
            f"Appointment Type: {appointment['appointment_type']}\n"
            f"Patient: {patient['name']}"
            f"\nBooked via DLMS"
        ),
        "start": {
            "dateTime": start_iso,
            "timeZone": "Asia/Dhaka"
        },
        "end": {
            "dateTime": end_iso,
            "timeZone": "Asia/Dhaka"
        },
         "attendees": [
            {"email": patient["email"]},  # PATIENT becomes invited guest
        ],
        "reminders": {"useDefault": True}
    }
    
    # 5. Create event in doctor's Google Calendar
    try:
        created_event = service.events().insert(
            calendarId="primary",
            body=event,
            sendUpdates="all"   # sends email + calendar invite to patient
        ).execute()
        print("Event created:", created_event.get("htmlLink"))
        return True
    except Exception as e:
        print(f"Error creating Google Calendar event: {e}")
        return False

#==========LABIBA M2 ends=====================================================================


#==========Angshu M2 starts===========
@app.route('/telemedicine_payment', methods=['GET'])
def telemedicine_payment():
    # 1. Check if user is logged in
    if 'user_id' not in session:
        return redirect(url_for('login')) # Redirect if not logged in
    
    p_id = session['user_id']
    
    # 2. Get confirmed app_ids from appointment table
    confirmed_apps_ids = get_confirmed_app_id(p_id)
    
    # 3. Get unpaid details from telemedicine_payment table
    # Note: This assumes rows exist in telemedicine_payment for these appointments.
    # If rows are created only upon payment attempt, logic might need adjustment.
    unpaid_appointments = get_unpaid_telemed(confirmed_apps_ids)
    
    # 4. Render the template
    return render_template(
        'telemedicine_payment.html', 
        name=session.get('name', 'Patient'), # Passing name for header
        p_id=p_id,
        unpaid_list=unpaid_appointments
    )




@app.route('/save_card_details', methods=['POST'])
def save_card_details():
    if 'user_id' not in session:
        return redirect(url_for('login'))
        
    p_id = request.form['p_id']
    app_id = request.form['app_id']
    card_number = request.form['card_number'].replace(" ", "")
    cvv = request.form['cvv']
    expiration_date = request.form['expiration_date']
    
    payment_amount = 1000.00 

    # --- UPDATED VERIFICATION CALL ---
    # Now passing p_id as the first argument
    card_status = verify_card_details(p_id, card_number, cvv, expiration_date)
    print(f"from app.py {card_status}")
    # --- Handle Results ---
    if card_status == "EXPIRED":
        return render_template('payment_gateway.html', 
                               app_id=app_id, 
                               p_id=p_id, 
                               error="Payment Failed: This card has expired.")
                               
    elif card_status == "INVALID":
        
        return render_template('payment_gateway.html', 
                               app_id=app_id, 
                               p_id=p_id, 
                               error="Verification Failed: The Card Number or CVV or Expiry Date does not match our records for this card.")

    # --- Processing ---
    is_new = (card_status == "NEW")
    
    success = finalize_telemedicine_transaction(p_id, app_id, card_number, cvv, expiration_date, payment_amount, is_new)

    if success:
        return redirect(url_for('telemedicine_payment'))
    else:
        return render_template('payment_gateway.html', 
                               app_id=app_id, 
                               p_id=p_id, 
                               error="System error processing payment. Please try again.")

@app.route('/payment_gateway/<int:app_id>')
def payment_gateway(app_id):
    # Check if user is logged in
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    # Render the credit card page, passing the specific app_id
    # This allows the page to know WHICH appointment is being paid for
    return render_template('payment_gateway.html', app_id=app_id, p_id=session['user_id'])
#==========Angshu M2 End===========

@app.route('/join_zoom/<int:app_id>')
@login_required
def join_zoom(app_id):
    """Join a Zoom meeting for a specific appointment"""
    user_id = session.get('user_id')
    user_role = session.get('role')
    
    # Fetch appointment details
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT a.*, p.name as patient_name, d.name as doctor_name,
               a.zoom_meeting_link, a.zoom_meeting_id, a.zoom_password
        FROM appointment a
        JOIN patient p ON a.p_id = p.p_id
        JOIN doctor d ON a.d_id = d.d_id
        WHERE a.app_id = %s
    """, (app_id,))
    appointment = cursor.fetchone()
    cursor.close()
    conn.close()
    
    if not appointment:
        flash('Appointment not found', 'error')
        return redirect(url_for('patient_dashboard' if user_role == 'patient' else 'doctor_dashboard'))
    
    # Check if user has access to this appointment
    if user_role == 'patient' and appointment['p_id'] != user_id:
        flash('You do not have access to this appointment', 'error')
        return redirect(url_for('patient_dashboard'))
    elif user_role == 'doctor' and appointment['d_id'] != user_id:
        flash('You do not have access to this appointment', 'error')
        return redirect(url_for('doctor_dashboard'))
    
    if not appointment.get('zoom_meeting_link'):
        flash('No Zoom meeting has been created for this appointment yet', 'warning')
        return redirect(url_for('patient_dashboard' if user_role == 'patient' else 'doctor_dashboard'))
    
    return render_template('zoom_meeting.html', appointment=appointment, user_role=user_role)

@app.route('/my_zoom_meetings')
@login_required
def my_zoom_meetings():
    """View all Zoom meetings for the logged-in user"""
    user_id = session.get('user_id')
    user_role = session.get('role')
    
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    if user_role == 'patient':
        cursor.execute("""
            SELECT a.*, d.name as doctor_name, d.designation,
                   a.zoom_meeting_link, a.zoom_meeting_id, a.zoom_password
            FROM appointment a
            JOIN doctor d ON a.d_id = d.d_id
            WHERE a.p_id = %s 
            AND a.appointment_type = 'telemedicine'
            AND a.confirmation = '1'
            AND a.zoom_meeting_link IS NOT NULL
            ORDER BY a.date DESC, a.time DESC
        """, (user_id,))
    else:  # doctor
        cursor.execute("""
            SELECT a.*, p.name as patient_name, p.phone,
                   a.zoom_meeting_link, a.zoom_meeting_id, a.zoom_password
            FROM appointment a
            JOIN patient p ON a.p_id = p.p_id
            WHERE a.d_id = %s 
            AND a.appointment_type = 'telemedicine'
            AND a.confirmation = '1'
            AND a.zoom_meeting_link IS NOT NULL
            ORDER BY a.date DESC, a.time DESC
        """, (user_id,))
    
    meetings = cursor.fetchall()
    cursor.close()
    conn.close()
    
    return render_template('my_zoom_meetings.html', meetings=meetings, user_role=user_role)

@app.route('/patient_appointments')
@login_required
def patient_appointments():
    """View all appointments for the logged-in patient"""
    p_id = session.get('user_id')
    
    if session.get('role') != 'patient':
        flash('Access denied. Patients only.', 'error')
        return redirect(url_for('login'))
    
    # Fetch all appointments with details
    appointments = get_patient_appointments_with_details(p_id)
    
    # Add status labels for display
    for appointment in appointments:
        if appointment['confirmation'] == 0:
            appointment['status_label'] = 'Pending'
            appointment['status_class'] = 'warning'
        elif appointment['confirmation'] == 1:
            appointment['status_label'] = 'Confirmed'
            appointment['status_class'] = 'success'
        elif appointment['confirmation'] == 2:
            appointment['status_label'] = 'Cancelled'
            appointment['status_class'] = 'danger'
        elif appointment['confirmation'] == 3:
            appointment['status_label'] = 'Reschedule Requested'
            appointment['status_class'] = 'info'
        else:
            appointment['status_label'] = 'Unknown'
            appointment['status_class'] = 'secondary'
        
        # Format date for display
        if isinstance(appointment['date'], date):
            appointment['date_display'] = appointment['date'].strftime('%B %d, %Y')
        else:
            appointment['date_display'] = str(appointment['date'])
    
    return render_template('patient_appointments.html', appointments=appointments)

@app.route('/patient_upcoming_appointments')
@login_required
def patient_upcoming_appointments():
    """View only upcoming appointments for the logged-in patient"""
    p_id = session.get('user_id')
    
    if session.get('role') != 'patient':
        flash('Access denied. Patients only.', 'error')
        return redirect(url_for('login'))
    
    # Fetch upcoming appointments
    appointments = get_upcoming_patient_appointments(p_id)
    
    # Add status labels
    for appointment in appointments:
        if appointment['confirmation'] == 0:
            appointment['status_label'] = 'Pending Confirmation'
            appointment['status_class'] = 'warning'
        elif appointment['confirmation'] == 1:
            appointment['status_label'] = 'Confirmed'
            appointment['status_class'] = 'success'
        elif appointment['confirmation'] == 3:
            appointment['status_label'] = 'Reschedule Requested'
            appointment['status_class'] = 'info'
        else:
            appointment['status_label'] = 'Unknown'
            appointment['status_class'] = 'secondary'
        
        # Format date
        if isinstance(appointment['date'], date):
            appointment['date_display'] = appointment['date'].strftime('%B %d, %Y')
        else:
            appointment['date_display'] = str(appointment['date'])
    
    return render_template('patient_upcoming_appointments.html', appointments=appointments)

#============================================


#==NAHIAN m3================= Prescription for Doctor + Patient ==============
#updated prescription with patient search
from datetime import datetime
from models.prescription_model import get_all_doctor_previous_prescriptions,search_patient_for_prescription, get_patient_info_for_prescription, get_doctor_info_for_prescription, insert_prescription, get_prescriptions_by_patient, get_patient_prescription, get_doctor_name_for_each_prescription, get_prescription_by_id

@app.route('/doctor_all_previous_prescriptions')
def doctor_all_previous_prescriptions():
  # Ensure doctor is logged in
    if 'user_id' not in session:
        flash("Session timed out. Please login again.", "error")
        return redirect(url_for('login'))

    d_id = session['user_id']
    prescriptions = get_all_doctor_previous_prescriptions(d_id)
    # if not prescriptions:
    #     flash("No prescriptions found.", "error")
    #     return redirect(url_for('doctor_dashboard'))
    return render_template('doctor_all_previous_prescriptions.html', prescriptions=prescriptions, d_id=d_id)

@app.route('/doctor_prescriptions', methods=['GET', 'POST'])
def doctor_prescriptions():
    # Ensure doctor is logged in
    if 'user_id' not in session:
        flash("Session timed out. Please login again.", "error")
        return redirect(url_for('login'))

    d_id = session['user_id']
    patient = None  # to hold searched patient info

    # -------------------------
    # 1️⃣ PATIENT SEARCH (search_patient button)
    # -------------------------
    if request.method == 'POST' and 'search_patient' in request.form:
        p_id = request.form.get('p_id')
        
        # Validation1: ensure patient exists
        patient = search_patient_for_prescription(p_id)
        if not patient:
            flash("No patient with this ID exists.", "error")
            return redirect(url_for('doctor_prescriptions', d_id=d_id))
        
        
        patient = get_patient_info_for_prescription(d_id, p_id)
        # Validation2: ensure this patient has an appointment with this doctor
        if not patient:
            flash("This patient does not have any appointment with you.", "error")
            return redirect(url_for('doctor_prescriptions', d_id=d_id))
        # Validation3: ensure doctor confirmed this patient's appointment
        if patient['confirmation'] != 1:
            flash("This patient does not have a confirmed appointment with you.", "error")
            return redirect(url_for('doctor_prescriptions', d_id=d_id))
        # Validation4: ensure this appointment is not yet checked
        if patient['checked'] == 1:
            flash("This patient's appointment has already been marked as checked.", "error")
            return redirect(url_for('doctor_prescriptions', d_id=d_id))
        
        # Fetch doctor info for the prescription page
        doctor = get_doctor_info_for_prescription(d_id)
        for i in doctor:
            if doctor[i] is None:
                doctor[i] = "Not Updated Yet"

        current_date = datetime.today().strftime('%Y-%m-%d')

        # Render page WITH patient data
        return render_template('doctor_prescriptions.html', patient=patient, doctor=doctor, current_date=current_date, d_id=d_id)


    # -------------------------
    # 2️⃣ ADD PRESCRIPTION (submit_prescription button)
    # -------------------------
    if request.method == 'POST' and 'submit_prescription' in request.form:

        p_id = request.form.get('p_id')
        detail = request.form.get('detail')
        morning = request.form.get('morning')
        afternoon = request.form.get('afternoon')
        night = request.form.get('night')
        date = datetime.today().strftime('%Y-%m-%d')
        weekly_smbg = request.form.get('weekly_smbg')

        # Insert prescription
        insert_prescription(p_id, d_id, detail, date, morning, afternoon, night, weekly_smbg)

        flash("Prescription added successfully!", "success")
        return redirect(url_for('doctor_prescriptions'))

    # -------------------------
    # 3️⃣ DEFAULT: no search, show empty page
    # -------------------------
    return render_template('doctor_prescriptions.html', patient=patient, d_id=d_id)

@app.route('/previous_prescriptions/<int:p_id>')
def previous_prescriptions(p_id):
    prescriptions = get_prescriptions_by_patient(p_id)
    return render_template('doctor_view_prescription_list.html', prescriptions=prescriptions, p_id=p_id)
#================


@app.route('/my_prescription')
def my_prescription():

    p_id= session['user_id']
 
    if 'user_id' not in session:
        flash("Session timed out. Please login again.")
        return redirect(url_for('login'))  

   
    prescriptions = get_patient_prescription(p_id)
    print(prescriptions)

    # Fetch doctor names for each prescription
    for prescription in prescriptions:
        doctor = get_doctor_name_for_each_prescription(prescription)
        prescription['doctor_name'] = doctor['name'] if doctor else 'Unknown Doctor'
    return render_template('my_prescription.html', prescriptions=prescriptions)



@app.route('/patient_prescription_details/<int:pres_id>')
def patient_prescription_details(pres_id):
    # Fetch the prescription
    prescription = get_prescription_by_id(pres_id)  

    if not prescription:
        return "Prescription not found", 404
    p_id = prescription['p_id']
    d_id = prescription['d_id']
    patient = get_patient_info_for_prescription(p_id, d_id)  
    
    # Fetch doctor info
    doctor = get_doctor_info_for_prescription(d_id)
    for i in doctor:
            if doctor[i] is None:
                doctor[i] = "Not Updated Yet"

    current_date = datetime.today().strftime('%Y-%m-%d')
    return render_template('patient_prescription_details.html', prescription=prescription, doctor=doctor, patient=patient, current_date=current_date)


#======NAHIAN M3 (prescription)ends=============================================================================

#======NAHIAN M3 (MAIL) starts=============================================================================
# -------------------------
# MAIL CONFIG
# -------------------------
from flask_mail import Mail, Message
from models.doctor_model import get_appointment_details #WITH MAIL

app.config["MAIL_SERVER"] = "smtp.gmail.com"
app.config["MAIL_PORT"] = 587
app.config["MAIL_USE_TLS"] = True
app.config["MAIL_USE_SSL"] = False
app.config["MAIL_USERNAME"] = "nahianlamisa12@gmail.com"
app.config["MAIL_PASSWORD"] = "pkcq qvpu eyaz euxr"
app.config["MAIL_DEFAULT_SENDER"] = "DLMS Notification <nahianlamisa12@gmail.com>"

mail = Mail(app)

def send_appointment_email(app_id, appointment_date, patient_email, patient_name, doctor_name, action, appointment_type=None):
    
    if action == "Confirmed" and appointment_type == "telemedicine":
        subject = f"Appintment ID- {app_id}: Payment Needed to Confirm Your Telemedicine Appointment"
        body = (
            f"Hello {patient_name},\n\n"
            f"Your telemedicine appointment request with Dr. {doctor_name} on {appointment_date} has been reviewed.\n"
            f"To complete and confirm your appointment, please make the online payment of 1000 BDT in out website: \n"
            f"http://127.0.0.1:5000/ \n"
            f"Once the payment is completed, your appointment will be fully confirmed and you will receive your online meeting link prior to your appointment.\n"
        )

    else:
       subject = f"Appintment ID- {app_id}: Your Appointment Has Been {action}"

       # Default email body
       body = (
           f"Hello {patient_name},\n\n"
           f"Your appointment with Dr. {doctor_name} on {appointment_date} has been {action.lower()}.\n"
        )


    body += "\nIf you need any help, feel free to contact us.\nThank you."

    msg = Message(subject, recipients=[patient_email])
    msg.body = body

    try:
        mail.send(msg)
        print(f"{action} email sent.")
        return True
    except Exception as e:
        print("Email error:", e)
        return False

#Then update doctor_appointments function to call this send_appointment_email function after updating appointment status.      
#======NAHIAN M3 (MAIL) ends============================================================================



from models.review_model import add_review, get_patient_reviews, delete_review, get_reviewable_doctors,get_doctor_reviews
# Adi integrated - Doctor review system
@app.route('/write_review', methods=['GET', 'POST'])
def write_review():
    if 'user_id' not in session:
        flash("Session timed out. Please login again.")
        return redirect(url_for('login'))
    
    p_id = session['user_id']
    
    if request.method == 'POST':
        d_id = request.form.get('d_id')
        rating = request.form.get('rating')
        comment = request.form.get('comment')
        
        if not d_id or not rating:
            flash("Doctor and rating are required", "error")
            return redirect(url_for('write_review'))
        
        try:
            rating = int(rating)
            if rating < 1 or rating > 5:
                flash("Rating must be between 1 and 5", "error")
                return redirect(url_for('write_review'))
        except ValueError:
            flash("Invalid rating value", "error")
            return redirect(url_for('write_review'))
        
        result = add_review(p_id, d_id, rating, comment)
        
        if result['success']:
            flash(result['message'], "success")
            return redirect(url_for('my_reviews'))
        else:
            flash(result['message'], "error")
            return redirect(url_for('write_review'))
    
    
    reviewable_doctors = get_reviewable_doctors(p_id)
    return render_template('write_review.html', doctors=reviewable_doctors)

# Adi integrated - View patient's own reviews
@app.route('/my_reviews')
def my_reviews():
    if 'user_id' not in session:
        flash("Session timed out. Please login again.")
        return redirect(url_for('login'))
    
    p_id = session['user_id']
    reviews = get_patient_reviews(p_id)
    return render_template('my_reviews.html', reviews=reviews)

# Adi integrated - Delete review
@app.route('/delete_review/<int:review_id>', methods=['POST'])
def delete_review_route(review_id):
    if 'user_id' not in session:
        flash("Session timed out. Please login again.")
        return redirect(url_for('login'))
    
    p_id = session['user_id']
    result = delete_review(review_id, p_id)
    
    if result['success']:
        flash(result['message'], "success")
    else:
        flash(result['message'], "error")
    
    return redirect(url_for('my_reviews'))

# Adi integrated - Doctor view of their reviews
@app.route('/doctor_reviews')
def doctor_reviews():
    if 'user_id' not in session:
        flash("Session timed out. Please login again.")
        return redirect(url_for('login'))
    
    if session['role'] != 'doctor':
        flash("Access denied", "error")
        return redirect(url_for('index'))
    
    d_id = session['user_id']
    review_data = get_doctor_reviews(d_id)
    return render_template('doctor_reviews.html', review_data=review_data)

#================M3+M4 Angshu starts===========================
@app.route('/ai_assistant', methods=['GET', 'POST'])
def ai_assistant():
    # 1. Authentication Check (Common for both)
    if 'user_id' not in session:
        return redirect(url_for('login'))
    # 2. Handle Chat Logic (POST request from JavaScript)
    if request.method == 'POST':
        data = request.get_json()
        
        if not data or 'prompt' not in data:
            return jsonify({"success": False, "message": "Missing 'prompt' in request body"}), 400

        user_prompt = data['prompt']
        
        # Call the model
        result = get_llama_response(user_prompt)
        
        # Handle Model Error
        if result['status'] == 'error':
            return jsonify({
                "success": False, 
                "message": result['payload'] 
            })

        # Handle Model Success
        elif result['status'] == 'success':
            raw_response = result['payload']
            
            # Convert Markdown to HTML & Sanitize
            html_response = markdown.markdown(raw_response)
            allowed_tags = list(bleach.sanitizer.ALLOWED_TAGS) + ['p', 'br', 'h1', 'h2', 'h3', 'strong', 'em', 'pre', 'code', 'ul', 'ol', 'li']
            clean_html_response = bleach.clean(html_response, tags=allowed_tags)
            
            return jsonify({
                "success": True,
                "response": clean_html_response,
                "raw_text": raw_response
            })

    # 3. Handle Page Load (GET request)
    return render_template('ai_assistant.html', p_id=session['user_id'])

@app.route('/update_doctor_profile', methods=['GET', 'POST'], endpoint='update_doctor_profile')
def update_doctor_profile_route():
    d_id= session['user_id']
    if 'user_id' not in session:  
        flash("Session timed out. Please login again.")
        return redirect(url_for('login'))  
    
    if request.method == 'POST':
        designation = request.form['designation']
        phone = request.form['phone']
        location = request.form['location']

        update_doctor_profile(d_id, designation, phone, location)
        flash("Doctor profile updated successfully")
        return redirect(url_for('doctor_dashboard'))

    doctor = get_doctor_by_id(d_id)
    if doctor:
        return render_template('update_doctor_profile.html', doctor=doctor)
    else:
        flash("No data found for this patient.")
        return 'Doctor not found', 404

#---------------Ansghu m3+m4 ends----------------------------


#############################################
# LOGOUT
@app.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out', 'info')
    return redirect(url_for('login'))

# RUN APP
if __name__ == '__main__':
    app.run(debug=True)
