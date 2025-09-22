import os
from dotenv import load_dotenv

load_dotenv()

def get_port():
    return int(os.getenv('PORT', 5000))

def get_db():

    database = {
        'host': os.getenv('DB_HOST', 'localhost'),
        'port': int(os.getenv('DB_PORT', 3306)),
        'user': os.getenv('DB_USER', 'user'),
        'password': os.getenv('DB_PASSWORD', 'password'),
        'dbname': os.getenv('DB_NAME', 'database')
    }    

    return database

def get_secret_key():
    return os.getenv('SECRET_KEY')