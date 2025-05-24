from models.database import Database


class User:
    def __init__(self, username, password, is_admin=False):
        self.username = username
        self.password = password
        self.is_admin = is_admin

    
    def save(self):
        try:
            db = Database()
            db.cursor.execute(
                "INSERT INTO user (username, password, is_admin) VALUES (%s, %s, %s)",
                (self.username, self.password, self.is_admin)
            )
            db.commit()
            db.close()
            print("User created successfully.")
        except Exception as e:
            print(f"Error saving user: {e}. Please Try Again.")
            db.close()

    
    @staticmethod
    def user_is_admin(user_id):
        try:
            db = Database()
            db.cursor.execute("SELECT is_admin FROM user WHERE user_id = %s", (user_id,))
            is_admin = db.cursor.fetchone()
            return is_admin[0] if is_admin else False
        except Exception as e:
            print(f"An error occurred while checking admin status: {e}")
            return False
        finally:
            db.close()
    

    @staticmethod
    def get_all_users():
        try:
            db = Database()
            db.cursor.execute("SELECT * FROM user")
            users = db.cursor.fetchall()
            return users
        except Exception as e:
            print(f"An error occurred while fetching users: {e}")
            return None
        finally:
            db.close()
    

    @staticmethod
    def get_user_by_id(user_id):
        try:
            db = Database()
            db.cursor.execute("SELECT * FROM user WHERE user_id = %s", (user_id,))
            user = db.cursor.fetchone()
            return user
        except Exception as e:
            print(f"An error occurred while fetching the user: {e}")
            return None
        finally:
            db.close()


    @staticmethod
    def update_password(user_id, new_password):
        try:
            db = Database()
            db.cursor.execute(
                "UPDATE user SET password = %s WHERE user_id = %s",
                (new_password, user_id)
            )
            db.commit()
            print("Password updated successfully.")
        except Exception as e:
            print(f"An error occurred while updating the password: {e}")
        finally:
            db.close()


    @staticmethod
    def delete_user(user_id):
        try:
            db = Database()
            db.cursor.execute("DELETE FROM user WHERE user_id = %s", (user_id,))
            db.commit()
            print("User deleted successfully.")
        except Exception as e:
            print(f"An error occurred while deleting the user: {e}")
        finally:
            db.close()

    
    @staticmethod
    def login(username, password):
        try:
            db = Database()
            db.cursor.execute(
                "SELECT user_id, username, is_admin FROM user WHERE username = %s AND password = %s",
                (username, password)
            )
            user = db.cursor.fetchone()
            return user
        except Exception as e:
            print(f"An error occurred during login: {e}")
            return None
        finally:
            db.close()
     
    