import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os

def send_email(to_address, subject, body):
    sender_email = "your-email@gmail.com" # Replace with env var in production
    sender_password = "your-app-password" # Replace with env var in production
    
    # Check if we have credentials (setup for demo: mocked if not present)
    if sender_email == "your-email@gmail.com":
        print(f"\n[Mock Email] To: {to_address}\nSubject: {subject}\nBody: {body}\n")
        return True

    try:
        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['To'] = to_address
        msg['Subject'] = subject

        msg.attach(MIMEText(body, 'plain'))

        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(sender_email, sender_password)
        text = msg.as_string()
        server.sendmail(sender_email, to_address, text)
        server.quit()
        return True
    except Exception as e:
        print(f"Failed to send email: {e}")
        return False
def send_doctor_approval_email(to_address, doctor_name, domain_email):
    subject = "Doctor Account Approved - DLMS"
    body = f"""Dear Dr. {doctor_name},

Congratulations! Your account on the Diabetes Lifestyle Management System (DLMS) has been approved by the admin.

You can now log in using your domain email:
Login Email: {domain_email}

Thank you for joining our medical professional network.

Best regards,
DLMS Admin Team"""
    return send_email(to_address, subject, body)

def send_doctor_rejection_email(to_address, doctor_name):
    subject = "Doctor Account Application - DLMS"
    body = f"""Dear {doctor_name},

Thank you for your interest in joining the Diabetes Lifestyle Management System (DLMS).

After reviewing your application, we regret to inform you that we cannot approve your account at this time.

If you believe this is an error or have further information to provide, please contact our support team.

Best regards,
DLMS Admin Team"""
    return send_email(to_address, subject, body)
