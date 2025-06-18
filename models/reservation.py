from models.database import Database
from datetime import datetime

db = Database()

class Reservation:
    def __init__(self, user_id, book_id):
        self.user_id = user_id
        self.book_id = book_id
        self.reservation_date = datetime.now()

    def save(self):
        sql = "INSERT INTO reservations (user_id, book_id, reservation_date) VALUES (%s, %s, %s)"
        db.execute(sql, (self.user_id, self.book_id, self.reservation_date))

    @staticmethod
    def add_reservation(user_id, book_id):
        sql = "INSERT INTO reservations (user_id, book_id, reservation_date) VALUES (%s, %s, %s)"
        db.execute(sql, (user_id, book_id, datetime.now()))

    @staticmethod
    def has_reservation(book_id):
        sql = "SELECT COUNT(*) FROM reservations WHERE book_id=%s"
        db.execute(sql, (book_id,))
        count = db.fetchone()[0]
        return count > 0

    @staticmethod
    def get_first_reservation(book_id):
        sql = "SELECT id, user_id FROM reservations WHERE book_id=%s ORDER BY reservation_date LIMIT 1"
        db.execute(sql, (book_id,))
        res = db.fetchone()
        if res:
            class Res:
                def __init__(self, id, user_id):
                    self.id = id
                    self.user_id = user_id
            return Res(res[0], res[1])
        return None

    @staticmethod
    def delete_reservation(reservation_id):
        sql = "DELETE FROM reservations WHERE id=%s"
        db.execute(sql, (reservation_id,))

    @staticmethod
    def user_has_reservation(user_id, book_id):
        sql = "SELECT COUNT(*) FROM reservations WHERE user_id=%s AND book_id=%s"
        db.execute(sql, (user_id, book_id))
        count = db.fetchone()[0]
        return count > 0

    @staticmethod
    def delete_user_reservation(user_id, book_id):
        sql = "DELETE FROM reservations WHERE user_id=%s AND book_id=%s"
        db.execute(sql, (user_id, book_id))
        return True

    @staticmethod
    def get_all_reservations():
        sql = """
            SELECT r.id, u.username, b.title, r.reservation_date
            FROM reservations r
            JOIN users u ON r.user_id = u.id
            JOIN books b ON r.book_id = b.id
            ORDER BY r.reservation_date
        """
        db.execute(sql)
        return db.fetchall()
