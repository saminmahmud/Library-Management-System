from models.database import Database
from datetime import datetime, timedelta

db = Database()

class Book:
    def __init__(self, title, author, category, quantity):
        self.title = title
        self.author = author
        self.category = category
        self.quantity = quantity

    def save(self):
        sql = "INSERT INTO books (title, author, category, quantity) VALUES (%s, %s, %s, %s)"
        db.execute(sql, (self.title, self.author, self.category, self.quantity))

    @staticmethod
    def get_all_books():
        sql = "SELECT * FROM books"
        db.execute(sql)
        return db.fetchall()

    @staticmethod
    def get_book_by_id(book_id):
        sql = "SELECT * FROM books WHERE id=%s"
        db.execute(sql, (book_id,))
        return db.fetchone()

    @staticmethod
    def search_books_by_title(title):
        sql = "SELECT * FROM books WHERE title LIKE %s"
        db.execute(sql, (f"%{title}%",))
        return db.fetchall()

    @staticmethod
    def search_books_by_author(author):
        sql = "SELECT * FROM books WHERE author LIKE %s"
        db.execute(sql, (f"%{author}%",))
        return db.fetchall()

    @staticmethod
    def search_books_by_category(category):
        sql = "SELECT * FROM books WHERE category LIKE %s"
        db.execute(sql, (f"%{category}%",))
        return db.fetchall()

    @staticmethod
    def update_book(book_id, title, author, category, quantity):
        sql = "UPDATE books SET title=%s, author=%s, category=%s, quantity=%s WHERE id=%s"
        db.execute(sql, (title, author, category, quantity, book_id))

    @staticmethod
    def update_book_quantity(book_id, quantity):
        sql = "UPDATE books SET quantity=%s WHERE id=%s"
        db.execute(sql, (quantity, book_id))

    @staticmethod
    def delete_book(book_id):
        sql = "DELETE FROM books WHERE id=%s"
        db.execute(sql, (book_id,))

    @staticmethod
    def get_available_copies(book_id):
        sql = """
            SELECT b.quantity - COUNT(br.id)
            FROM books b
            LEFT JOIN borrow_records br ON b.id = br.book_id AND br.return_date IS NULL
            WHERE b.id = %s
            GROUP BY b.id
        """
        db.execute(sql, (book_id,))
        result = db.fetchone()
        if result is None:
            return 0
        return max(result[0], 0)

    @staticmethod
    def borrow_book(user_id, book_id, borrow_days=14):
        available = Book.get_available_copies(book_id)
        if available <= 0:
            return False, "No copies available to borrow."

        borrow_date = datetime.now()
        due_date = borrow_date + timedelta(days=borrow_days)

        sql = "INSERT INTO borrow_records (user_id, book_id, borrow_date, due_date) VALUES (%s, %s, %s, %s)"
        try:
            db.execute(sql, (user_id, book_id, borrow_date, due_date))
            return True, "Book borrowed successfully."
        except Exception as e:
            return False, f"Error borrowing book: {e}"

    @staticmethod
    def return_book(user_id, book_id, fine_per_day=10):
        # Find active borrow record
        sql = """
            SELECT id, due_date FROM borrow_records
            WHERE user_id=%s AND book_id=%s AND return_date IS NULL
            ORDER BY borrow_date LIMIT 1
        """
        db.execute(sql, (user_id, book_id))
        borrow = db.fetchone()
        if not borrow:
            return False, "No active borrow record found for this book.", 0

        borrow_id, due_date = borrow
        return_date = datetime.now()
        fine = 0
        if return_date > due_date:
            delta = return_date - due_date
            fine = delta.days * fine_per_day

        sql = "UPDATE borrow_records SET return_date=%s, fine=%s WHERE id=%s"
        db.execute(sql, (return_date, fine, borrow_id))

        return True, "Book returned successfully.", fine

    @staticmethod
    def get_borrow_history_with_fines(user_id, fine_per_day=10):
        sql = """
            SELECT br.id, b.title, br.borrow_date, br.due_date, br.return_date, br.fine
            FROM borrow_records br
            JOIN books b ON br.book_id = b.id
            WHERE br.user_id = %s
            ORDER BY br.borrow_date DESC
        """
        db.execute(sql, (user_id,))
        records = db.fetchall()
        history = []
        for r in records:
            br_id, title, borrow_date, due_date, return_date, fine = r
            if return_date is None:
                now = datetime.now()
                if now > due_date:
                    delta = now - due_date
                    fine = delta.days * fine_per_day
                else:
                    fine = 0
            history.append({
                "borrow_id": br_id,
                "title": title,
                "borrow_date": borrow_date.strftime("%Y-%m-%d"),
                "due_date": due_date.strftime("%Y-%m-%d"),
                "return_date": return_date.strftime("%Y-%m-%d") if return_date else "Not returned",
                "fine": fine
            })
        return history
