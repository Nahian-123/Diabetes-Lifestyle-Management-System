from flask import Flask, request, jsonify, render_template, redirect, url_for, session, flash
import mysql.connector
from datetime import datetime
from functools import wraps
import os
import base64

# DeepFace for verification
from deepface import DeepFace

# Import models
from models.user_model import login_user, register_user, validate_email

from models.patient_model import get_patient_notifications, get_time_based_medication_reminder,get_patient_notifications, get_patient_name_glucose_info_update,get_patient_notices
from models.user_model import login_user, register_user, validate_email
from models.doctor_model import get_doctor_name, get_doctor_notices 
from models.admin_model import insert_notice,get_dashboard_stats



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


#############################################
# REGISTER ROUTE  (UNCHANGED)
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
    
    return render_template('register.html')   ### Made a change


#############################################
# LOGIN ROUTE — >>> UPDATED <<<
#############################################
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':

        email = request.form['email']
        password = request.form['password']
        
        
        user_data = login_user(email, password)
        
        if user_data:
            session['user_id'] = user_data['user_id']
            session['email'] = user_data['email']
            session['role'] = user_data['role']
            session['name'] = user_data['name']

            flash('Login successful!', 'success')

            # >>> NEW LOGIC: If doctor logs in → Send to face verification
            if session['role'] == 'doctor':
                return redirect(url_for('doctor_dashboard'))   ## I changed

            # Normal login flow for others
            if session['role'] == 'admin':
                return redirect(url_for('admin_dashboard'))
            elif session['role'] == 'patient':
                return redirect(url_for('patient_dashboard'))
        
        flash('Invalid email, password, or role selection', 'error')

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
    
    notices = get_patient_notices(p_id)  #rakha lagbe
    notifications = get_patient_notifications(p_id)  # 🆕 fetch notifications angshu for doctor appointment confirm/cancel/reschedule #rakha lagbe 
    medication_message = get_time_based_medication_reminder(p_id) #rakha lagbe


    return render_template('patient_dashboard.html', name=patient['name'], p_id=p_id, updated_on=patient['updated_on'], glucose_data=glucose_data, notifications=notifications, medication_message=medication_message, notices=notices)




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
