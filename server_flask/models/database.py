import mysql.connector
from config import Config


class Database:
    @staticmethod
    def get_connection():
        return mysql.connector.connect(
            user=Config.MYSQL_USER,
            password=Config.MYSQL_PASSWORD,
            host=Config.MYSQL_HOST,
            database=Config.MYSQL_DB,
        )

    @staticmethod
    def execute_query(query):
        connection = Database.get_connection()
        cursor = connection.cursor(dictionary=True)
        cursor.execute(query)
        result = cursor.fetchall()
        cursor.close()
        connection.close()
        return result

    @staticmethod
    def execute_non_query(query):
        connection = Database.get_connection()
        cursor = connection.cursor()
        cursor.execute(query)
        connection.commit()
        cursor.close()
        connection.close()
