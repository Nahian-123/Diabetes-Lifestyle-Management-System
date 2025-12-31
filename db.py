# import mysql.connector

# #MySQL Database Configuration (XAMPP)
# db_config= {
#     'host':'127.0.0.1',
#     'user' : 'root',
#     'password': '',
#     'database': 'dms'
# }


# #Establising db connection
# def get_db_connection():
#     return mysql.connector.connect(**db_config)

import mysql.connector

# MySQL Database Configuration (Railway)
db_config = {
    'host': 'switchback.proxy.rlwy.net',
    'user': 'root',
    'password': 'ADgeeNSrZYmubwUSIyjHWVsMsnvkolAT',  
    'database': 'railway',  # Your database is now named 'railway', not 'dms'
    'port': 52990           
}

# Establishing db connection
def get_db_connection():
    try:
        connection = mysql.connector.connect(**db_config)
        print("✅ Connected to Railway successfully!")
        return connection
    except mysql.connector.Error as err:
        print(f"❌ Error: {err}")
        return None
