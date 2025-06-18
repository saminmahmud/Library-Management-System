import mysql.connector
from models.table import CreateTables

class Database:
    def __init__(self):
        self.connection = mysql.connector.connect(
            host="localhost",
            port=3307,
            user="root",  
            password="password", 
        )
        self.cursor = self.connection.cursor(buffered=True)
        
        CreateTables(self.cursor)


    def execute(self, query, params=None):
        self.cursor.execute(query, params or ())
        self.connection.commit()

    def fetchall(self):
        return self.cursor.fetchall()

    def fetchone(self):
        return self.cursor.fetchone()

    def close(self):
        self.cursor.close()
        self.connection.close()
