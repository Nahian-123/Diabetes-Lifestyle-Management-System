# =====Updated user_modelpy given by aditya========
from db import get_db_connection
import re
from datetime import datetime, timedelta
from werkzeug.security import generate_password_hash, check_password_hash
import random
import string
# Import email sender from the same package (models)
from models.email_sender import send_email


ADMIN_EMAIL_DOMAIN = "@admin.dms.com"
DOCTOR_EMAIL_DOMAIN = "@doctor.dms.com"


def validate_email(email):
    """Validate email format"""
    email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(email_pattern, email)


def detect_role_from_email(email):
    """Detect user role based on email domain"""
    email_lower = email.lower()
   
    if email_lower.endswith(ADMIN_EMAIL_DOMAIN):
        return 'admin'
    elif email_lower.endswith(DOCTOR_EMAIL_DOMAIN):
        return 'doctor'
    else:
        return 'patient'


def login_user(email, password):
    """Login a user - role is determined by email domain"""
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    user = None
    user_data = None
   
    # Detect role from email domain
    role = detect_role_from_email(email)
   
    try:
        if role == 'admin':
            cursor.execute('SELECT * FROM admin WHERE email = %s', (email,))
            user = cursor.fetchone()
            if user and check_password_hash(user['password'], password):
                user_data = {
                    'user_id': user['id'],
                    'email': user['email'],
                    'role': 'admin',
                    'name': user.get('name', 'Admin')
                }
        elif role == 'doctor':
            cursor.execute('SELECT * FROM doctor WHERE domain_email = %s', (email,))
            user = cursor.fetchone()
            if user:
                # Check verification status FIRST
                if user['verified'] == 0:
                    return {'error': 'Account not verified. Please check your email for the OTP.'}

                if check_password_hash(user['password'], password):
                    user_data = {
                        'user_id': user['d_id'],
                        'email': user['domain_email'],  # Domain email for session
                        'real_email': user['email'],    # Real email for Google integrations
                        'role': 'doctor',
                        'name': user['name']
                    }
        else:  # patient
            cursor.execute('SELECT * FROM patient WHERE email = %s', (email,))
            user = cursor.fetchone()
            if user and check_password_hash(user['password'], password):
                user_data = {
                    'user_id': user['p_id'],
                    'email': user['email'],
                    'role': 'patient',
                    'name': user['name']
                }
    finally:
        cursor.close()
        conn.close()
   
    return user_data if user_data else None


def verify_otp(email, otp_code):
    """Verify OTP for a doctor"""
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    result = {'success': False, 'message': ''}
    
    try:
        # Find doctor with this real email
        cursor.execute("SELECT * FROM doctor WHERE email = %s", (email,))
        user = cursor.fetchone()
        
        if not user:
            result['message'] = "User not found."
            return result
            
        if user['otp_code'] == otp_code:
            # Check expiry
            if user['otp_expiry'] and user['otp_expiry'] > datetime.now():
                # Success! Verify the user
                cursor.execute("UPDATE doctor SET verified = 1, otp_code = NULL WHERE email = %s", (email,))
                conn.commit()
                result['success'] = True
                result['message'] = "Account verified successfully! You can now login with your domain email."
            else:
                 result['message'] = "OTP has expired."
        else:
             result['message'] = "Invalid OTP code."
             
    except Exception as e:
        result['message'] = f"Database error: {str(e)}"
    finally:
        cursor.close()
        conn.close()
        
    return result


def register_user(username, email, password, role, doctor_data=None):
    """Register a new user"""
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    result = {'success': False, 'message': '', 'redirect_otp': False}
    
    # Hash the password
    hashed_password = generate_password_hash(password)
   
    try:
        if role == 'doctor':
            local_part = email.split('@')[0]
            domain_email = local_part + DOCTOR_EMAIL_DOMAIN
           
            # Check if real email already exists
            cursor.execute('SELECT * FROM doctor WHERE email = %s', (email,))
            if cursor.fetchone():
                result['message'] = 'Email already registered as a doctor'
                return result
           
            # Check if domain_email already exists
            cursor.execute('SELECT * FROM doctor WHERE domain_email = %s', (domain_email,))
            if cursor.fetchone():
                result['message'] = 'A doctor with this username already exists'
                return result
            
            # Generate OTP
            otp_code = ''.join(random.choices(string.digits, k=6))
            otp_expiry = datetime.now() + timedelta(minutes=10)
           
            cursor.execute(
                '''INSERT INTO doctor
                (name, email, domain_email, password, designation, verified, otp_code, otp_expiry)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)''',
                (username, email, domain_email, hashed_password, 'General Physician', 0, otp_code, otp_expiry)
            )
            conn.commit()
            
            # Send Email
            email_body = f"Your Verification Code is: {otp_code}\nIt expires in 10 minutes.\nLogin Email: {domain_email}"
            send_email(email, "Doctor Verification Code", email_body)

            result['success'] = True
            result['message'] = f'Registration successful! Please verify your email: {email}'
            result['redirect_otp'] = True # Signal to redirect to OTP page
            result['email'] = email
           
        elif role == 'patient':
            cursor.execute('SELECT * FROM patient WHERE email = %s', (email,))
            if cursor.fetchone():
                result['message'] = 'Email already registered as a patient'
                return result
           
            cursor.execute(
                'INSERT INTO patient (name, email, password) VALUES (%s, %s, %s)',
                (username, email, hashed_password)
            )
            conn.commit()
            result['success'] = True
            result['message'] = 'Registration successful! You can now login.'
    except Exception as e:
        result['message'] = f'Database error: {str(e)}'
    finally:
        cursor.close()
        conn.close()
   
    return result



