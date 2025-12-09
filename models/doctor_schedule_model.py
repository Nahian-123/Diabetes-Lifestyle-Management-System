from db import get_db_connection
#=========NAHIAN M1===========

#==================SCHEDULE======================
def save_schedule(d_id, day1, day2, teleday, day1_start, day2_start, teleday_start):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO doctor_schedule
        (d_id, day1, day2, teleday, day1_starttime, day2_starttime, teleday_starttime)
        VALUES (%s,%s,%s,%s,%s,%s,%s)
        ON DUPLICATE KEY UPDATE
            day1=VALUES(day1),
            day2=VALUES(day2),
            teleday=VALUES(teleday),
            day1_starttime=VALUES(day1_starttime),
            day2_starttime=VALUES(day2_starttime),
            teleday_starttime=VALUES(teleday_starttime)
    """, (d_id, day1, day2, teleday, day1_start, day2_start, teleday_start))

    conn.commit()
    cursor.close()
    conn.close()


def get_schedule(d_id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT 
            d_id,
            day1, day2, teleday,
            TIME_FORMAT(day1_starttime, '%H:%i') AS day1_starttime,
            TIME_FORMAT(day2_starttime, '%H:%i') AS day2_starttime,
            TIME_FORMAT(teleday_starttime, '%H:%i') AS teleday_starttime
        FROM doctor_schedule
        WHERE d_id = %s
    """, (d_id,))

    result = cursor.fetchone()

    cursor.close()
    conn.close()
    return result


#=====================SLOTS=============================

def create_or_reset_slots(d_id):
    conn = get_db_connection()
    cursor = conn.cursor()

    # Reset all slots to 0 for the existing row
    cursor.execute("""
        UPDATE doctor_slot
        SET
            day1slot1 = 0, day1slot2 = 0, day1slot3 = 0, day1slot4 = 0,
            day1slot5 = 0, day1slot6 = 0, day1slot7 = 0, day1slot8 = 0,
            day2slot1 = 0, day2slot2 = 0, day2slot3 = 0, day2slot4 = 0,
            day2slot5 = 0, day2slot6 = 0, day2slot7 = 0, day2slot8 = 0,
            teledayslot1 = 0, teledayslot2 = 0, teledayslot3 = 0, teledayslot4 = 0,
            teledayslot5 = 0, teledayslot6 = 0, teledayslot7 = 0, teledayslot8 = 0
        WHERE d_id = %s
    """, (d_id,))

    # If row doesn't exist, insert it (first time)
    if cursor.rowcount == 0:
        slot_values = [0] * 24
        cursor.execute("""
            INSERT INTO doctor_slot (
                d_id,
                day1slot1, day1slot2, day1slot3, day1slot4, day1slot5, day1slot6, day1slot7, day1slot8,
                day2slot1, day2slot2, day2slot3, day2slot4, day2slot5, day2slot6, day2slot7, day2slot8,
                teledayslot1, teledayslot2, teledayslot3, teledayslot4, teledayslot5, teledayslot6, teledayslot7, teledayslot8
            ) VALUES (%s, %s,%s,%s,%s,%s,%s,%s,%s,
                      %s,%s,%s,%s,%s,%s,%s,%s,
                      %s,%s,%s,%s,%s,%s,%s,%s)
        """, (d_id, *slot_values))

    conn.commit()
    cursor.close()
    conn.close()




def get_slots(d_id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM doctor_slot WHERE d_id = %s", (d_id,))
    data = cursor.fetchone()
    cursor.fetchall()

    cursor.close()
    conn.close()

    if not data:
        return None

    return {
        "day1_slots": [data[f"day1slot{i}"] for i in range(1, 9)],
        "day2_slots": [data[f"day2slot{i}"] for i in range(1, 9)],
        "teleday_slots": [data[f"teledayslot{i}"] for i in range(1, 9)]
    }
