import mysql.connector

DB_CONFIG = {
    "host": "localhost",
    "user": "root",       
    "password": "Kingsley20!!",       
    "database": "music_reviews"
}

def get_connection():
    connection = mysql.connector.connect(**DB_CONFIG)
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SET SESSION TRANSACTION ISOLATION LEVEL READ COMMITTED")
    return connection
