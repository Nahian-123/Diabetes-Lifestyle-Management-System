
from db import get_db_connection
from datetime import datetime


def get_dashboard_stats():      ###########  ADITYA #########
    """Get statistics for admin dashboard"""
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    stats = {}
    
    try:
        # Get pending doctor verifications (email verified but pending admin approval)
        cursor.execute("SELECT COUNT(*) AS pending_count FROM doctor WHERE verified = 1")
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

def get_all_doctors():    ###########  ADITYA #########
    """Get all doctors"""
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute("SELECT * FROM doctor")
        doctors = cursor.fetchall()
        return doctors
    finally:
        cursor.close()
        conn.close()

def get_all_doctors_for_verification():  ###########  ADITYA #########
    """Get all doctors for verification, ordered by verification status"""
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    result = {'doctors': [], 'pending_count': 0}
    
    try:
        # Get all doctors, ordered by verification status (pending first)
        cursor.execute("SELECT * FROM doctor ORDER BY verified ASC, d_id ASC")
        result['doctors'] = cursor.fetchall()
        
        # Get count of pending verifications
        cursor.execute("SELECT COUNT(*) AS pending_count FROM doctor WHERE verified = 0")
        result['pending_count'] = cursor.fetchone()['pending_count']
    finally:
        cursor.close()
        conn.close()
    
    return result

def update_doctor_verification(d_id, action):  ###########  ADITYA #########
    """Update doctor verification status and return doctor info for email notification"""
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    result = {'success': False, 'message': '', 'doctor_email': None, 'doctor_name': None, 'domain_email': None}
    
    try:
        # First, get doctor information for email notification
        cursor.execute("SELECT name, email, domain_email FROM doctor WHERE d_id = %s", (d_id,))
        doctor = cursor.fetchone()
        
        if not doctor:
            result['message'] = f'Doctor ID {d_id} not found.'
            return result
        
        result['doctor_email'] = doctor['email']
        result['doctor_name'] = doctor['name']
        result['domain_email'] = doctor['domain_email']
        
        if action == 'Confirm':
            # Set verified = 2 (admin approved)
            cursor.execute("UPDATE doctor SET verified = 2 WHERE d_id = %s", (d_id,))
            result['message'] = f'Doctor {doctor["name"]} has been approved successfully!'
            result['approved'] = True
        elif action == 'Cancel':
            # Set verified = -1 (admin rejected)
            cursor.execute("UPDATE doctor SET verified = -1 WHERE d_id = %s", (d_id,))
            result['message'] = f'Doctor {doctor["name"]} has been rejected.'
            result['approved'] = False
            
        conn.commit()
        result['success'] = True
    except Exception as e:
        result['message'] = f'Error: {str(e)}'
    finally:
        cursor.close()
        conn.close()
    
    return result

def get_all_orders():  ###########  ADITYA #########
    """Get all orders with their items"""
    print("Starting get_all_orders function")
    try:
        conn = get_db_connection()
        if not conn:
            print("Failed to connect to database")
            return []
            
        cursor = conn.cursor(dictionary=True)
        
        # Get all orders with patient information
        query = """
            SELECT o.*, p.name as patient_name 
            FROM orders o
            JOIN patient p ON o.p_id = p.p_id
            ORDER BY o.order_date DESC
        """
        print(f"Executing query: {query}")
        cursor.execute(query)
        
        orders = cursor.fetchall()
        print(f"Found {len(orders) if orders else 0} orders")
        
        # Convert orders to list if it's not already
        if not isinstance(orders, list):
            print(f"Orders is not a list, it's a {type(orders)}")
            orders = list(orders) if orders else []
        
        # For each order, get its items and calculate total
        for order in orders:
            item_query = """
                SELECT * FROM order_items
                WHERE order_id = %s
            """
            print(f"Executing item query for order {order['order_id']}")
            cursor.execute(item_query, (order['order_id'],))
            
            items = cursor.fetchall()
            print(f"Found {len(items) if items else 0} items for order {order['order_id']}")
            
            # Convert items to list if it's not already
            if not isinstance(items, list):
                print(f"Items is not a list, it's a {type(items)}")
                items = list(items) if items else []
            
            # Process each item to ensure all values are of the right type
            processed_items = []
            for item in items:
                processed_item = dict(item)  # Create a copy to avoid modifying the original
                
                # Ensure price is a float
                if 'price' in processed_item:
                    try:
                        processed_item['price'] = float(processed_item['price'])
                    except (TypeError, ValueError):
                        processed_item['price'] = 0.0
                else:
                    processed_item['price'] = 0.0
                
                # Ensure quantity is an int
                if 'quantity' in processed_item:
                    try:
                        processed_item['quantity'] = int(processed_item['quantity'])
                    except (TypeError, ValueError):
                        processed_item['quantity'] = 0
                else:
                    processed_item['quantity'] = 0
                
                processed_items.append(processed_item)
            
            order['items'] = processed_items
            
            # Calculate total amount
            total_amount = 0
            for item in processed_items:
                item_total = item['price'] * item['quantity']
                total_amount += item_total
            
            order['total_amount'] = float(total_amount)
            
            # Set default payment method if not present
            if 'payment_method' not in order:
                order['payment_method'] = 'cash'
        
        cursor.close()
        conn.close()
        
        print(f"Returning {len(orders)} orders")
        return orders
    except Exception as e:
        import traceback
        print(f"Error getting orders: {str(e)}")
        print(traceback.format_exc())
        return []

def update_order_status(order_id, status):     ###########  ADITYA #########
    """Update order status"""
    try:
        conn = get_db_connection()
        if not conn:
            return {"success": False, "message": "Database connection failed"}
            
        cursor = conn.cursor()
        
        cursor.execute("""
            UPDATE orders 
            SET status = %s
            WHERE order_id = %s
        """, (status, order_id))
        
        conn.commit()
        cursor.close()
        conn.close()
        
        status_text = "responded" if status == "responded" else "pending"
        return {"success": True, "message": f"Order marked as {status_text}"}
    except Exception as e:
        print(f"Error updating order status: {str(e)}")
        return {"success": False, "message": f"Error: {str(e)}"}
    

################# NAHIAN  m4 ###########################
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
