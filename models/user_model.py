from db import get_db_connection
import re
from datetime import datetime

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
            cursor.execute('SELECT * FROM admin WHERE email = %s AND password = %s', (email, password))
            user = cursor.fetchone()
            if user:
                user_data = {
                    'user_id': user['id'],
                    'email': user['email'],
                    'role': 'admin',
                    'name': user.get('name', 'Admin')
                }
        elif role == 'doctor':
            cursor.execute('SELECT * FROM doctor WHERE email = %s AND password = %s', (email, password))
            user = cursor.fetchone()
            if user:
                user_data = {
                    'user_id': user['d_id'],
                    'email': user['email'],
                    'role': 'doctor',
                    'name': user['name']
                }
        else:  # patient
            cursor.execute('SELECT * FROM patient WHERE email = %s AND password = %s', (email, password))
            user = cursor.fetchone()
            if user:
                user_data = {
                    'user_id': user['p_id'],
                    'email': user['email'],
                    'role': 'patient',
                    'name': user['name']
                }
    finally:
        cursor.close()
        conn.close()
    
    return user_data if user else None
    

def register_user(username, email, password, role, doctor_data=None):
    """Register a new user"""
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    result = {'success': False, 'message': ''}
    
    try:
        # Check if email already exists in the appropriate table
        if role == 'doctor':
            cursor.execute('SELECT * FROM doctor WHERE email = %s', (email,))
            if cursor.fetchone():
                result['message'] = 'Email already registered as a doctor'
                return result
            
            if role == "doctor":
                
                cursor.execute(
                    '''INSERT INTO doctor 
                    (name, email, password, designation, verified) 
                    VALUES (%s, %s, %s, %s, %s)''',
                    (username, email, password, 'General Physician', 0)
                )
                conn.commit()
                result['success'] = True
                result['message'] = 'Registration successful! You are a BMDC verified doctor. Please wait for admin approval before logging in.'
            
        elif role == 'Patient':
            cursor.execute('SELECT * FROM patient WHERE email = %s', (email,))
            if cursor.fetchone():
                result['message'] = 'Email already registered as a patient'
                return result
            
            # Insert new patient
            cursor.execute(
                'INSERT INTO patient (name, email, password) VALUES (%s, %s, %s)',
                (username, email, password)
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
