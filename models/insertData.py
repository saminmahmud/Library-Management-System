from models.database import Database
from datetime import datetime, timedelta
import bcrypt

def insert_dummy_data():
    db = Database()

    def hash_password(pw):
        return bcrypt.hashpw(pw.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

    # Insert users
    users = [
        ('rakib', hash_password('rakibpass'), False),
        ('karim', hash_password('karimpass'), False),
    ]
    for username, pwd, is_admin in users:
        db.execute("""
            INSERT IGNORE INTO users (username, password, is_admin) VALUES (%s, %s, %s)
        """, (username, pwd, is_admin))

    db.execute("SELECT id, username FROM users")
    users_db = {username: uid for uid, username in db.fetchall()}

    # Insert books
    books = [
        ('The Great Gatsby', 'F. Scott Fitzgerald', 'Classic', 5),
        ('1984', 'George Orwell', 'Dystopian', 3),
        ('To Kill a Mockingbird', 'Harper Lee', 'Classic', 4),
        ('Python Programming', 'John Zelle', 'Programming', 2),
        ('Clean Code', 'Robert C. Martin', 'Programming', 1)
    ]
    for title, author, category, quantity in books:
        db.execute("""
            INSERT IGNORE INTO books (title, author, category, quantity) VALUES (%s, %s, %s, %s)
        """, (title, author, category, quantity))

    db.execute("SELECT id, title FROM books")
    books_db = {title: bid for bid, title in db.fetchall()}

    # Insert borrow_records
    borrow_records = [
        (users_db.get('rakib'), books_db.get('1984'), datetime.now() - timedelta(days=10), datetime.now() + timedelta(days=4), None, 0),
        (users_db.get('karim'), books_db.get('Python Programming'), datetime.now() - timedelta(days=20), datetime.now() - timedelta(days=6), datetime.now() - timedelta(days=5), 10),
    ]
    for user_id, book_id, borrow_date, due_date, return_date, fine in borrow_records:
        if user_id is None or book_id is None:
            continue
        db.execute("""
            INSERT IGNORE INTO borrow_records (user_id, book_id, borrow_date, due_date, return_date, fine)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (user_id, book_id, borrow_date, due_date, return_date, fine))

    # Insert reviews
    reviews = [
        (books_db.get('1984'), users_db.get('rakib'), "A chilling vision of the future.", 5),
        (books_db.get('The Great Gatsby'), users_db.get('karim'), "Beautifully written but tragic.", 4),
        (books_db.get('Clean Code'), users_db.get('karim'), "Must-read for programmers.", 5)
    ]
    for book_id, user_id, review_text, rating in reviews:
        if user_id is None or book_id is None:
            continue
        db.execute("""
            INSERT IGNORE INTO reviews (book_id, user_id, review, rating) VALUES (%s, %s, %s, %s)
        """, (book_id, user_id, review_text, rating))

    # Insert reservations
    reservations = [
        (users_db.get('rakib'), books_db.get('To Kill a Mockingbird'), datetime.now()),
        (users_db.get('karim'), books_db.get('Clean Code'), datetime.now())
    ]
    for user_id, book_id, reservation_date in reservations:
        if user_id is None or book_id is None:
            continue
        db.execute("""
            INSERT IGNORE INTO reservations (user_id, book_id, reservation_date) VALUES (%s, %s, %s)
        """, (user_id, book_id, reservation_date))

    db.close()
    # print("Dummy data inserted successfully.")

if __name__ == "__main__":
    insert_dummy_data()
