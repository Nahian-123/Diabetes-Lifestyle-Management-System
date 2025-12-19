import json
from datetime import datetime
from db import get_db_connection

ALLOWED_TABLES = {
    'carbs', 'protein', 'vegetable',
    'fruits', 'dairy', 'healthy_fats'
}



def get_patient(p_id):
    db = get_db_connection()
    cur = db.cursor(dictionary=True)
    cur.execute(
        "SELECT gender, dob, weight, height_cm FROM patient WHERE p_id=%s",
        (p_id,)
    )
    data = cur.fetchone()
    db.close()
    return data

# ✅ GENDER MISMATCH FIX (REQUESTED)
# def calculate_daily_cal(age, gender, weight, height, activity):
#     gender = gender.lower()
#     bmr = 10*weight + 6.25*height - 5*age + (5 if gender.startswith('m') else -161)
#     factor = {'sedentary':1.2, 'moderate':1.55, 'active':1.75}
#     return int(bmr * factor.get(activity, 1.2))

def calculate_daily_cal(age, gender, weight, height, activity):
    weight = float(weight)
    height = float(height)
    age = int(age)

    gender = gender.lower()

    bmr = (
        10 * weight
        + 6.25 * height
        - 5 * age
        + (5 if gender.startswith('m') else -161)
    )

    factor = {
        'sedentary': 1.2,
        'moderate': 1.55,
        'active': 1.75
    }

    return int(bmr * factor.get(activity, 1.2))




def get_foods(category):
    if category not in ALLOWED_TABLES:
        return []

    db = get_db_connection()
    cur = db.cursor(dictionary=True)
    cur.execute(f"SELECT item, calory FROM `{category}`")
    data = cur.fetchall()
    db.close()
    return data

def save_diet(d_id, diet):
    db = get_db_connection()
    cur = db.cursor()

    cur.execute("""
        INSERT INTO diet_suggestion (
            d_id, p_id, activity_lvl, diabetes_condition,
            breakfast, breakfast_cal,
            lunch, lunch_cal,
            dinner, dinner_cal,
            daily_cal_allowance, suggested_on
        ) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
    """, (
        d_id,
        diet['p_id'],
        diet['activity_lvl'],
        diet['diabetes_condition'],
        json.dumps(diet['breakfast']),
        diet['breakfast_cal'],
        json.dumps(diet['lunch']),
        diet['lunch_cal'],
        json.dumps(diet['dinner']),
        diet['dinner_cal'],
        diet['daily_cal'],
        datetime.now()
    ))

    db.commit()
    db.close()


def get_latest_diet_suggestion(p_id):
    """
    Returns latest diet suggestion for a given patient
    """
    conn = get_db_connection()
    cur = conn.cursor(dictionary=True)
    cur.execute("""
        SELECT *
        FROM diet_suggestion
        WHERE p_id = %s
        ORDER BY suggested_on DESC
        LIMIT 1
    """, (p_id,))
    diet = cur.fetchone()
    conn.close()

    if diet:
        # Convert JSON strings to Python objects
        for meal in ['breakfast', 'lunch', 'dinner']:
            diet[meal] = json.loads(diet[meal]) if diet[meal] else []
        return diet
    return None

def get_doctor_name(d_id):
    """
    Returns doctor's full name by d_id
    """
    conn = get_db_connection()
    cur = conn.cursor(dictionary=True)
    cur.execute("SELECT name FROM doctor WHERE d_id = %s", (d_id,))
    row = cur.fetchone()
    conn.close()
    return row['name'] if row else "Unknown"
