from db import get_db_connection

#model made  by angshu
from datetime import datetime

def verify_card_details(p_id, card_number, input_cvv, input_expiry):
    """
    Checks validity of the single card registered to this p_id.
    """
    # --- 1. Expiry Check (Date Logic) ---
    try:
        exp_month, exp_year_short = map(int, input_expiry.split('/'))
        exp_year = 2000 + exp_year_short
        now = datetime.now()
        
        # Check if date is in the past
        if exp_year < now.year or (exp_year == now.year and exp_month < now.month):
            return "EXPIRED"
        if exp_month < 1 or exp_month > 12:
            return "INVALID"
    except ValueError:
        return "INVALID"

    # --- 2. Database Check (Strict 1 Card per Patient) ---
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        # Get the ONE card registered to this patient
        query = """
            SELECT cvv, expiration_date, card_number
            FROM card_registry 
            WHERE p_id = %s 
            LIMIT 1
        """
        cursor.execute(query, (p_id,))
        record = cursor.fetchone()
        print(record)

        # If no record exists for this patient, it's a NEW card
        if not record:
            print(f"from model.py new branch")
            return "NEW"
              
       
        if (record['card_number'] == card_number and 
            record['cvv'] == input_cvv and 
            record['expiration_date'] == input_expiry):
            print(f"from model.py valid branch")
            return "VALID"
        else:
            print(f"from model.py invalid branch")
            return "INVALID"
            
    finally:
        cursor.close()
        conn.close()

def finalize_telemedicine_transaction(p_id, app_id, card_number, cvv, expiry, amount, is_new_card):
    """
    Updates the payment status. 
    Only inserts the card into registry if it is marked as 'is_new_card'.
    """
    conn =get_db_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        # 1. OPTIONAL: Save Card (Only if it's new)
        if is_new_card:
            insert_card = """
                INSERT INTO card_registry (p_id, card_number, cvv, expiration_date)
                VALUES (%s, %s, %s, %s)
            """
            cursor.execute(insert_card, (p_id, card_number, cvv, expiry))

        # 2. ALWAYS: Update Payment Status
        update_payment = """
            UPDATE telemedicine_payment 
            SET paid = 1, 
                amount = %s, 
                timestamp = NOW() 
            WHERE app_id = %s
        """
        cursor.execute(update_payment, (amount, app_id))

        conn.commit()
        return True

    except Exception as e:
        print(f"Transaction Error: {e}")
        conn.rollback()
        return False
    finally:
        cursor.close()
        conn.close()
