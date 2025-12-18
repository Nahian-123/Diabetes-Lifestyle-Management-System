from db import get_db_connection
import math
from datetime import datetime

def haversine_distance(lat1, lon1, lat2, lon2):
    """
    Calculate the great circle distance between two points 
    on the earth (specified in decimal degrees)
    """
    # Convert decimal degrees to radians 
    lon1, lat1, lon2, lat2 = map(math.radians, [float(lat1), float(lon1), float(lat2), float(lon2)])

    # Haversine formula 
    dlon = lon2 - lon1 
    dlat = lat2 - lat1 
    a = math.sin(dlat/2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon/2)**2
    c = 2 * math.asin(math.sqrt(a)) 
    r = 6371 # Radius of earth in kilometers. Use 3956 for miles
    return c * r

def send_emergency_sms(contact, message):
    """Mock SMS API"""
    print(f"\n[URGENT CARE API] Sending Message to {contact}: {message}\n")
    return True

def request_ambulance(p_id, lat, lon):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    result = {'success': False, 'message': ''}
    
    try:
        # Check if already has pending request
        cursor.execute("SELECT * FROM emergency_requests WHERE patient_id = %s AND status != 'Resolved' AND ride_completed = 0", (p_id,))
        if cursor.fetchone():
            result['message'] = 'You already have an active emergency request.'
            return result

        # Find nearest available ambulance
        cursor.execute("SELECT * FROM ambulance WHERE is_available = 1")
        ambulances = cursor.fetchall()
        
        if not ambulances:
            result['message'] = 'No ambulances valid at the moment. Please call 999.'
            return result
        
        nearest_amb = None
        min_dist = float('inf')
        
        for amb in ambulances:
            dist = haversine_distance(lat, lon, amb['latitude'], amb['longitude'])
            if dist < min_dist:
                min_dist = dist
                nearest_amb = amb
        
        if nearest_amb:
            # Create Request
            cursor.execute("""
                INSERT INTO emergency_requests (patient_id, location_lat, location_lon, assigned_ambulance_id, status)
                VALUES (%s, %s, %s, %s, 'Dispatched')
            """, (p_id, lat, lon, nearest_amb['amb_id']))
            req_id = cursor.lastrowid
            
            # Simulated Driver Notification
            msg = f"EMERGENCY! Go to Lat: {lat}, Lon: {lon}. Contact Patient ID: {p_id}"
            send_emergency_sms(nearest_amb['contact_number'], msg)
            
            conn.commit()
            
            result['success'] = True
            result['message'] = 'Ambulance dispatched!'
            result['ambulance'] = nearest_amb
            result['eta'] = round((min_dist / 40) * 60) # Assume 40km/h avg speed, return minutes
        
    except Exception as e:
        result['message'] = f"Error: {str(e)}"
    finally:
        cursor.close()
        conn.close()
        
    return result

def get_active_request(p_id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        query = """
            SELECT r.*, a.driver_name, a.contact_number, a.latitude as amb_lat, a.longitude as amb_lon 
            FROM emergency_requests r
            JOIN ambulance a ON r.assigned_ambulance_id = a.amb_id
            WHERE r.patient_id = %s AND r.status != 'Resolved' AND r.ride_completed = 0
            ORDER BY r.timestamp DESC LIMIT 1
        """
        cursor.execute(query, (p_id,))
        return cursor.fetchone()
    finally:
        cursor.close()
        conn.close()

def mark_ride_completed(p_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        # We find the active request for this patient and mark it completed
        cursor.execute("""
            UPDATE emergency_requests 
            SET ride_completed = 1, status = 'Resolved'
            WHERE patient_id = %s AND ride_completed = 0
        """, (p_id,))
        conn.commit()
        return {'success': True, 'message': 'Ride marked as completed.'}
    except Exception as e:
        return {'success': False, 'message': str(e)}
    finally:
        cursor.close()
        conn.close()

def add_emergency_contact(p_id, name, phone, relation):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "INSERT INTO emergency_contacts (p_id, name, contact_number, relation) VALUES (%s, %s, %s, %s)",
            (p_id, name, phone, relation)
        )
        conn.commit()
        return {'success': True, 'message': 'Contact added successfully.'}
    except Exception as e:
        return {'success': False, 'message': str(e)}
    finally:
        cursor.close()
        conn.close()

def get_emergency_contacts(p_id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute("SELECT * FROM emergency_contacts WHERE p_id = %s", (p_id,))
        return cursor.fetchall()
    finally:
        cursor.close()
        conn.close()

def notify_family(p_id, lat, lon, recipients):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    result = {'success': False, 'message': ''}
    
    try:
        contact_numbers = []
        
        # If 'all' is passed, fetch all contacts
        if recipients == 'all':
            contacts = get_emergency_contacts(p_id)
            for c in contacts:
                contact_numbers.append({'name': c['name'], 'number': c['contact_number']})
        else:
            # Recipients should be a list of numbers, verify they belong to user? 
            # For simplicity, assuming the frontend passes valid numbers for now.
             contacts = get_emergency_contacts(p_id) # Verify ownership
             valid_map = {c['contact_number']: c['name'] for c in contacts}
             
             for r in recipients:
                 if r in valid_map:
                     contact_numbers.append({'name': valid_map[r], 'number': r})
        
        if not contact_numbers:
             result['message'] = "No valid contacts to notify."
             return result

        # Send SMS
        msg = f"URGENT: Your family member needs help at current location: Lat {lat}, Lon {lon}."
        sent_names = []
        for contact in contact_numbers:
            send_emergency_sms(contact['number'], msg)
            sent_names.append(contact['name'])
        
        result['success'] = True
        result['message'] = f"Emergency alert sent to: {', '.join(sent_names)}"
        
    except Exception as e:
        result['message'] = f"Error: {str(e)}"
    finally:
        cursor.close()
        conn.close()
        
    return result
