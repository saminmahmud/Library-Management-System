from models.database import Database

db = Database()

class ReviewAndRating:
    def __init__(self, book_id, user_id, review, rating):
        self.book_id = book_id
        self.user_id = user_id
        self.review = review
        self.rating = rating

    def save(self):
        sql = "INSERT INTO reviews (book_id, user_id, review, rating) VALUES (%s, %s, %s, %s)"
        db.execute(sql, (self.book_id, self.user_id, self.review, self.rating))

    @staticmethod
    def get_reviews_by_book(book_id):
        sql = "SELECT * FROM reviews WHERE book_id=%s"
        db.execute(sql, (book_id,))
        return db.fetchall()

    @staticmethod
    def get_average_rating(book_id):
        sql = "SELECT AVG(rating) FROM reviews WHERE book_id=%s"
        db.execute(sql, (book_id,))
        avg = db.fetchone()[0]
        if avg is None:
            return None
        return round(avg, 2)
