import mysql.connector

#MySQL Database Configuration (XAMPP)
db_config= {
    'host':'127.0.0.1',
    'user' : 'root',
    'password': '',
    'database': 'dms'
}


#Establising db connection
def get_db_connection():
    return mysql.connector.connect(**db_config)