from db import get_db_connection
from datetime import datetime

def add_review(p_id, d_id, rating, comment):       #######  ADITYA ########
    """Add a new review from a patient to a doctor"""
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        # Check if patient has had an appointment with this doctor
        cursor.execute("""
            SELECT 1 FROM appointment 
            WHERE p_id = %s AND d_id = %s AND confirmation = 1 AND checked = 1
            LIMIT 1
        """, (p_id, d_id))
        
        has_appointment = cursor.fetchone() is not None
        
        if not has_appointment:
            return {
                "success": False,
                "message": "You can only review doctors you've had appointments with"
            }
        
        # Check if patient has already reviewed this doctor
        cursor.execute("""
            SELECT 1 FROM doctor_reviews 
            WHERE p_id = %s AND d_id = %s
            LIMIT 1
        """, (p_id, d_id))
        
        already_reviewed = cursor.fetchone() is not None
        
        if already_reviewed:
            # Update existing review
            cursor.execute("""
                UPDATE doctor_reviews 
                SET rating = %s, comment = %s, review_date = %s
                WHERE p_id = %s AND d_id = %s
            """, (rating, comment, datetime.now(), p_id, d_id))
            
            conn.commit()
            return {
                "success": True,
                "message": "Your review has been updated"
            }
        else:
            # Insert new review
            cursor.execute("""
                INSERT INTO doctor_reviews (p_id, d_id, rating, comment, review_date)
                VALUES (%s, %s, %s, %s, %s)
            """, (p_id, d_id, rating, comment, datetime.now()))
            
            conn.commit()
            return {
                "success": True,
                "message": "Your review has been submitted"
            }
    except Exception as e:
        conn.rollback()
        return {
            "success": False,
            "message": f"Error submitting review: {str(e)}"
        }
    finally:
        cursor.close()
        conn.close()

def get_doctor_reviews(d_id):          #######  ADITYA ########
    """Get all reviews for a specific doctor"""
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute("""
            SELECT dr.*, p.name as patient_name
            FROM doctor_reviews dr
            JOIN patient p ON dr.p_id = p.p_id
            WHERE dr.d_id = %s
            ORDER BY dr.review_date DESC
        """, (d_id,))
        
        reviews = cursor.fetchall()
        
        # Calculate average rating
        if reviews:
            total_rating = sum(review['rating'] for review in reviews)
            avg_rating = total_rating / len(reviews)
        else:
            avg_rating = 0
            
        return {
            "reviews": reviews,
            "avg_rating": avg_rating,
            "total_reviews": len(reviews)
        }
    except Exception as e:
        print(f"Error getting doctor reviews: {str(e)}")
        return {
            "reviews": [],
            "avg_rating": 0,
            "total_reviews": 0
        }
    finally:
        cursor.close()
        conn.close()

def get_patient_reviews(p_id):          #######  ADITYA ########
    """Get all reviews submitted by a specific patient"""
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute("""
            SELECT dr.*, d.name as doctor_name
            FROM doctor_reviews dr
            JOIN doctor d ON dr.d_id = d.d_id
            WHERE dr.p_id = %s
            ORDER BY dr.review_date DESC
        """, (p_id,))
        
        reviews = cursor.fetchall()
        return reviews
    except Exception as e:
        print(f"Error getting patient reviews: {str(e)}")
        return []
    finally:
        cursor.close()
        conn.close()

def delete_review(review_id, p_id):        #######  ADITYA ########
    """Delete a review (only if it belongs to the patient)"""
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("""
            DELETE FROM doctor_reviews
            WHERE review_id = %s AND p_id = %s
        """, (review_id, p_id))
        
        if cursor.rowcount > 0:
            conn.commit()
            return {
                "success": True,
                "message": "Review deleted successfully"
            }
        else:
            return {
                "success": False,
                "message": "Review not found or you don't have permission to delete it"
            }
    except Exception as e:
        conn.rollback()
        return {
            "success": False,
            "message": f"Error deleting review: {str(e)}"
        }
    finally:
        cursor.close()
        conn.close()

def get_reviewable_doctors(p_id):          #######  ADITYA ########
    """Get list of doctors the patient has had appointments with"""
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute("""
            SELECT DISTINCT d.d_id, d.name, d.designation,
                   (SELECT MAX(a.date) FROM appointment a 
                    WHERE a.p_id = %s AND a.d_id = d.d_id AND a.confirmation = 1 AND a.checked = 1) as last_appointment,
                   (SELECT dr.rating FROM doctor_reviews dr 
                    WHERE dr.p_id = %s AND dr.d_id = d.d_id) as current_rating
            FROM doctor d
            JOIN appointment a ON d.d_id = a.d_id
            WHERE a.p_id = %s AND a.confirmation = 1 AND a.checked = 1
            ORDER BY last_appointment DESC
        """, (p_id, p_id, p_id))
        
        doctors = cursor.fetchall()
        return doctors
    except Exception as e:
        print(f"Error getting reviewable doctors: {str(e)}")
        return []
    finally:
        cursor.close()
        conn.close()
