import mysql.connector

from models.table import CreateTables

class Database:
    def __init__(self):
        self.conn = mysql.connector.connect(
            host="localhost",
            port=3307,
            user="root",
            password="password" 
        )
        self.cursor = self.conn.cursor()

        self.cursor.execute("CREATE DATABASE IF NOT EXISTS library_db")
        self.cursor.execute("USE library_db")

        CreateTables(self.cursor)
    

    def commit(self):
        self.conn.commit()


    def close(self):
        self.cursor.close()
        self.conn.close()


