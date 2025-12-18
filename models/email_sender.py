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
