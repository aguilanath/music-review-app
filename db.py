import mysql.connector

DB_CONFIG = {
    "host": "localhost",
    "user": "root",       
    "password": "Kingsley20!!",       
    "database": "music_reviews"
}

def get_connection():
    return mysql.connector.connect(**DB_CONFIG)
