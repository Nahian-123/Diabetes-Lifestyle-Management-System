#from utils.db import get_connection
from db import get_db_connection
from datetime import datetime


def get_dashboard_stats():
    """Get statistics for admin dashboard"""
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    stats = {}
    
    try:
        # Get pending doctor verifications
        cursor.execute("SELECT COUNT(*) AS pending_count FROM doctor WHERE verified = 0 OR verified IS NULL")
        stats['pending_count'] = cursor.fetchone()['pending_count']
        
        # Get today's appointments
        cursor.execute("SELECT COUNT(*) AS pending_app FROM appointment WHERE DATE(date) = CURDATE()")
        stats['pending_app'] = cursor.fetchone()['pending_app']
        
        # Get total doctors count
        cursor.execute("SELECT COUNT(*) AS total_doctors FROM doctor")
        stats['total_doctors'] = cursor.fetchone()['total_doctors']
        
        # Get total patients count
        cursor.execute("SELECT COUNT(*) AS total_patients FROM patient")
        stats['total_patients'] = cursor.fetchone()['total_patients']
        
        # Get current timestamp
        stats['timestamp'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    finally:
        cursor.close()
        conn.close()
    
    return stats



def insert_notice(sender_id, recipient_type, recipient_id, message, date):
    connection = get_db_connection()
    cursor = connection.cursor()

    query = """
        INSERT INTO notices (sender_id, recipient_type, recipient_id, message, date)
        VALUES (%s, %s, %s, %s, %s)
    """
    cursor.execute(query, (sender_id, recipient_type, recipient_id, message, date))
    connection.commit()
    cursor.close()
    connection.close()

