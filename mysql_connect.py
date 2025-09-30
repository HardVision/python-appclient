from mysql.connector import connect, Error
import dotenv as d
from os import getenv

d.load_dotenv()

def conectar_server():
    config = {
        'user': getenv("USER_DB"),
        'password': getenv("PASSWORD_DB"),
        'host': getenv("HOST_DB"),
        'database': getenv("DATABASE_DB"),
    }

    try:
        db = connect(**config)
        if db.is_connected():
            db_info = db.get_server_info()
            print('Connected to MySQL server version -', db_info)
        return db
    
    except Error as e:
        print('Error to connect with MySQL -', e)
        return None