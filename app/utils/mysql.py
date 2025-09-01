import os
from dotenv import load_dotenv
from mysql.connector import connect, Error

load_dotenv()
config = {
    'user': os.getenv("DB_USER"),
    'password': os.getenv("DB_PASSWORD"),
    'host': os.getenv("DB_HOST"),
    'database': os.getenv("DB_DATABASE")
}

def executar(query):
    try:
        db = connect(**config)
        if db.is_connected():
            db_info = db.server_info
            print('Connected to MySQL server version -', db_info)
            with db.cursor() as cursor:
                cursor.execute(query)
                resultado = cursor.fetchall()

            db.commit()
            cursor.close()
            db.close()
            return resultado
    
    except Error as e:
        print('Error to connect with MySQL -', e)    