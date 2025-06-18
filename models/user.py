from models.database import Database
import hashlib

db = Database()

class User:
    def __init__(self, username, password, is_admin=False):
        self.username = username
        self.password = self.hash_password(password)
        self.is_admin = is_admin

    @staticmethod
    def hash_password(password):
        return hashlib.sha256(password.encode()).hexdigest()

    def save(self):
        sql = "INSERT INTO users (username, password, is_admin) VALUES (%s, %s, %s)"
        db.execute(sql, (self.username, self.password, self.is_admin))

    @staticmethod
    def login(username, password):
        hashed = User.hash_password(password)
        sql = "SELECT id, username, is_admin FROM users WHERE username=%s AND password=%s"
        db.execute(sql, (username, hashed))
        return db.fetchone()

    @staticmethod
    def update_password(user_id, new_password):
        hashed = User.hash_password(new_password)
        sql = "UPDATE users SET password=%s WHERE id=%s"
        db.execute(sql, (hashed, user_id))

    @staticmethod
    def get_all_users():
        sql = "SELECT id, username, is_admin FROM users"
        db.execute(sql)
        return db.fetchall()

    @staticmethod
    def get_user_by_id(user_id):
        sql = "SELECT id, username, is_admin FROM users WHERE id=%s"
        db.execute(sql, (user_id,))
        return db.fetchone()

    @staticmethod
    def delete_user(user_id):
        sql = "DELETE FROM users WHERE id=%s"
        db.execute(sql, (user_id,))
