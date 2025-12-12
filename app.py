from flask import Flask, request, jsonify, render_template, redirect, url_for, session, flash
import mysql.connector
from datetime import datetime
from functools import wraps
import os
import base64

# # DeepFace for verification
# from deepface import DeepFace

# Import models
from models.user_model import login_user, register_user, validate_email

from models.patient_model import get_patient_notifications, get_time_based_medication_reminder,get_patient_notifications, get_patient_name_glucose_info_update,get_patient_notices,get_confirmed_app_id, get_unpaid_telemed,populate_telemed_payment #last 3 imports by angshu
from models.user_model import login_user, register_user, validate_email
from models.doctor_model import get_doctor_name, get_doctor_notices 
from models.admin_model import insert_notice,get_dashboard_stats
from models.payment_model import verify_card_details, finalize_telemedicine_transaction  # Angshu M2 payment model imports
from models.appointment_model import get_latest_appointment  # Angshu M2 appointment model import


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



from models.user_model import login_user, register_user, validate_email
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
            flash(result['message'], 'success')
            return redirect(url_for('login'))
        else:
            flash(result['message'], 'error')
            return redirect(url_for('register'))
   
    return render_template('register.html')





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


# ############################################################
# # >>> NEW: FACE VERIFICATION PAGE <<<
# ############################################################
# @app.route('/verify')
# @login_required
# def verify_face_page():
#     if session.get('role') != 'doctor':
#         return redirect(url_for('login'))
#     return render_template("verify.html")


# def get_doctor_image_path(doctor_id):
#     UPLOAD_FOLDER = "uploads/doctors/"
#     valid_ext = ["jpeg", "jpg", "png"]

#     for ext in valid_ext:
#         path = os.path.join(UPLOAD_FOLDER, f"{doctor_id}.{ext}")
#         if os.path.exists(path):
#             return path
    
#     return None


# @app.post("/verify-face")
# def verify_face_api():

#     doctor_id = session.get("user_id")

#     if not doctor_id:
#         return jsonify({"match": False, "message": "Not logged in"})

#     UPLOAD_FOLDER = "uploads/doctors/"
#     os.makedirs(UPLOAD_FOLDER, exist_ok=True)

#     data = request.json
#     live_image = data["live_image"]

#     stored_image_path = os.path.join(UPLOAD_FOLDER, f"{doctor_id}.jpg")

#     if not os.path.exists(stored_image_path):
#         print(f"[v0] ERROR: Doctor image not found at {stored_image_path}")
#         return jsonify({"match": False, "message": f"Doctor photo not found. Expected at: {stored_image_path}"})

#     # Convert base64 → actual file
#     live_image = live_image.replace("data:image/jpg;base64,", "")
#     live_bytes = base64.b64decode(live_image)

#     live_path = "live_temp.jpg"
#     with open(live_path, "wb") as f:
#         f.write(live_bytes)

#     # Perform face verification
#     try:
#         print(f"[v0] Comparing {stored_image_path} with {live_path}")
#         result = DeepFace.verify(
#         img1_path=stored_image_path,
#         img2_path=live_path,
#         model_name="VGG-Face",
#         distance_metric="cosine",
#         threshold=0.6,   # ← LOWER = strict, HIGHER = lenient
#         enforce_detection=False
#         )

#         if result["verified"]:
#             print(f"[v0] Face verified! Distance: {result['distance']}")
#             os.remove(live_path)  # Clean up temp file
#             flash("Face Verified Successfully!", "success")
#             return jsonify({"match": True, "redirect": url_for("doctor_dashboard")})
#         else:
#             print(f"[v0] Face not matched. Distance: {result['distance']}")
#             os.remove(live_path)  # Clean up temp file
#             return jsonify({"match": False, "message": "Face does not match."})

#     except Exception as e:
#         print(f"[v0] Face detection error: {str(e)}")
#         if os.path.exists(live_path):
#             os.remove(live_path)
#         return jsonify({"match": False, "message": f"Face not detected. Error: {str(e)}"})



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
from datetime import datetime, timedelta

def generate_slot_times(start_time_str, count=8, duration=30):
    start = datetime.strptime(start_time_str, "%H:%M")
    times = []

    for i in range(count):
        st = start + timedelta(minutes=i * duration)
        et = st + timedelta(minutes=duration)
        times.append(f"{st.strftime('%H:%M')} - {et.strftime('%H:%M')}")
    
    return times


from datetime import datetime, timezone, timedelta

@app.route("/update_schedule", methods=["GET", "POST"])
def update_schedule():
    if 'user_id' not in session:
        flash("Session timed out. Please login again.")
        return redirect(url_for('login'))

    d_id = session['user_id']

    #LOAD SCHEDULE + SLOT DATA FIRST ----
    schedule = get_schedule(d_id)
    slots = get_slots(d_id)

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

    day1_times = generate_slot_times(schedule['day1_starttime'], len(slots['day1_slots']))
    day2_times = generate_slot_times(schedule['day2_starttime'], len(slots['day2_slots']))
    teleday_times = generate_slot_times(schedule['teleday_starttime'], len(slots['teleday_slots']))

    # ========== POST REQUEST ==========
    if request.method == "POST":

        # ---- CHECK DAY ----
        bd_time = datetime.now(timezone(timedelta(hours=6)))
        today = bd_time.strftime("%A")

        if today != "Saturday":
            flash("You can update your schedule only on Saturdays.", "error")
            return render_template(
                "doctor_schedule.html",
                schedule=schedule,
                slots=slots,
                day1_times=day1_times,
                day2_times=day2_times,
                teleday_times=teleday_times
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
        d_id = d_id,
        schedule=schedule,
        slots=slots,
        day1_times=day1_times,
        day2_times=day2_times,
        teleday_times=teleday_times
    )

#==========NAHIIAN M1 ends===========

#==========NAHIAN M2===========

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
        return redirect(url_for('login'))  # Add your login route
    
    if request.method == 'POST':
        app_id = request.form.get('app_id')
        action = request.form.get('action')

        update_appointment_status(app_id, d_id, action)

        # --
        # ========= LABIBA M2 GOOGLE CALENDER API =================
        # if confirmed → add event to patient Google Calendar
        if action == "Confirm":
            create_google_calendar_event(app_id)
        #==========================================================

        flash('Updated appointment successfully!', 'success')
        return redirect(url_for('doctor_appointments'))
 # --------------------------------------------------------------------------------

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

@app.route('/doctor_prescriptions', methods=['GET', 'POST'])
def doctor_prescriptions():
    d_id= session['user_id']
    if 'user_id' not in session:  #######Finally activate this
        flash("Session timed out. Please login again.")
        return redirect(url_for('login'))  # Add your login route


    if request.method == 'POST':
        p_id = request.form['p_id']
        weekly_smbg = request.form['weekly_smbg']
        date = datetime.today().strftime('%Y-%m-%d')


        # if not check_patient_appointment(p_id, d_id):
        #     flash("This patient doesn't have a confirmed appointment with you.", "warning")
        #     return redirect(url_for('doctor_prescriptions'))
       
        insert_prescription(p_id, d_id, date, weekly_smbg)
        flash('Prescription added successfully!', 'success')
        return redirect(url_for('doctor_prescriptions'))


    return render_template('doctor_prescriptions.html',d_id=d_id)




@app.route('/patient_dashboard', endpoint='patient_dashboard')
def patient_dashboard():
    if 'user_id' not in session:
        flash("Session timed out. Please login again.")
        return redirect(url_for('login'))


    p_id = session['user_id']
    patient = get_patient_name_glucose_info_update(p_id)
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


 


    return render_template(
        'patient_dashboard.html',
        name=patient['name'],
        p_id=p_id,
        updated_on=patient['updated_on'],
        glucose_data=glucose_data,
       
        smbg_status=smbg_routine_details["status"],
        weekly_smbg=smbg_routine_details.get("weekly_smbg"),
        doctor_name=smbg_routine_details.get("doctor_name"),
        smbg_date=smbg_routine_details.get("date")
        )  

#==========LABIBA M1 ends=====================================================================


#==========LABIBA M2 starts===================================================================
from models.patient_model import filter_doctor_by_area, get_verified_doctor_details, get_verified_doctor_details, get_distinct_area
from models.patient_model import get_patient_details, update_patient_details

from models.patient_model import get_doctor_weekly_schedule, get_doctor_slots, get_patient_required_fields, check_appointment_next_week, update_doctor_slot, insert_appointment
from models.appointment_model import get_appointment_by_id

from models.doctor_model import get_doctor_by_id
from datetime import time, timedelta
import json


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
    weekly_data = get_doctor_weekly_schedule(d_id)
    slot_data = get_doctor_slots(d_id)

    # Determine day_num (“day1”, “day2”, “teleday”)
    if appointment_day == weekly_data["day1"]:
        day_num = "day1"
    elif appointment_day == weekly_data["day2"]:
        day_num = "day2"
    elif appointment_day == weekly_data["teleday"]:
        day_num = "teleday"
    else:
        flash("Error: Invalid schedule day selected.")
        return redirect(url_for('request_appointment', d_id=d_id))

    slot_column = f"{day_num}slot{slot_number}"

    # Generate slot_time again (same logic as request_appointment)
    # Fetch starting time
    start_time = normalize_time(weekly_data[f"{day_num}_starttime"])
    slot_date = datetime.strptime(appointment_date, "%Y-%m-%d")
    start_dt = datetime.combine(slot_date, start_time)
    slot_dt = start_dt + timedelta(minutes=(int(slot_number) - 1) * 30)
    slot_time = slot_dt.strftime("%I:%M %p")

    # --------- VALIDATION CHECKS ---------

    # 1. Profile check
    patient_fields = get_patient_required_fields(p_id)
    required_fields = [
        'name', 'dob', 'weight', 'gender',
        'gl_b_breakfast', 'gl_a_breakfast',
        'gl_b_lunch', 'gl_b_dinner'
    ]

    if not all(patient_fields.get(f) not in (None, '', 0) for f in required_fields):
        flash("Error: Please complete your profile first.")
        return redirect(url_for('request_appointment', d_id=d_id))

    # 2. Followup date check
    today = datetime.now().date()
    patient = get_patient_details(p_id)
    followup = patient["followup_date"]

    if followup and today < followup:
        flash(f"Error: Your follow-up date ({followup}) has not arrived yet.")
        return redirect(url_for('request_appointment', d_id=d_id))

    # 3. Next 7 days rule
    next_7 = today + timedelta(days=7)
    if check_appointment_next_week(p_id, today, next_7):
        flash("Error: You already have an appointment within the next 7 days.")
        return redirect(url_for('request_appointment', d_id=d_id))

    # 4. Slot availability
    if slot_data.get(slot_column) == 1:
        flash("Error: Slot already booked. Please select another slot.")
        return redirect(url_for('request_appointment', d_id=d_id))

    # Mark slot booked
    update_doctor_slot(d_id, slot_column)

    # Insert new appointment
    insert_appointment(d_id, p_id, appointment_date, slot_time, appointment_type)
    appointment= get_latest_appointment()
    if appointment["appointment_type"]=="telemedicine":
        populate_telemed_payment(appointment["app_id"],p_id,d_id)

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
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import Flow
from datetime import datetime, timedelta
import os

os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'  # Allow http:// for local dev

CLIENT_SECRETS_FILE = "client_secret.json"
SCOPES = ["https://www.googleapis.com/auth/calendar"]

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
    appointment = get_appointment_by_id(app_id)
    patient = get_patient_details(appointment["p_id"])
    doctor = get_doctor_by_id(appointment["d_id"])
    
    # 3. Build start/end datetime
    # Combine date + time → datetime
    date = str(appointment["date"])       # YYYY-MM-DD
    time = str(appointment["time"])       # HH:MM AM/PM

    # Build ISO datetime
    # Convert "YYYY-MM-DD" + "HH:MM AM/PM" → datetime object
    start_dt = datetime.strptime(f"{date} {time}", "%Y-%m-%d %I:%M %p")
    end_dt = start_dt + timedelta(minutes=30)

    # Create Google Calendar–ready ISO strings
    start_iso = start_dt.isoformat()
    end_iso = end_dt.isoformat()

    print("start_iso:",start_iso)
    print("end_iso:",end_iso)

    # Build event
    event = {
        "summary": f"DLMS Appointment Day",
        "description": (
            f"Appointment ID: {appointment['app_id']}\n"
            f"Appointment Type: {appointment['appointment_type']}\n"
            f"Doctor: {doctor['name']}"
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
    created_event = service.events().insert(
        calendarId="primary",
        body=event,
        sendUpdates="all"   # sends email + calendar invite to patient
    ).execute()


    print("Event created:", created_event.get("htmlLink"))
    return True

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









#############################################
# LOGOUT
#############################################
@app.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out', 'info')
    return redirect(url_for('login'))


#############################################
# RUN APP
#############################################
if __name__ == '__main__':
    app.run(debug=True)
