from models.database import Database


class ReviewAndRating:
    def __init__(self, book_id, user_id, review, rating):
        self.book_id = book_id
        self.user_id = user_id
        self.review = review
        self.rating = rating


    def save(self):
        try:
            db = Database()
            db.cursor.execute(
                "INSERT INTO review_and_rating (book_id, user_id, review, rating) VALUES (%s, %s, %s, %s)",
                (self.book_id, self.user_id, self.review, self.rating)
            )
            db.commit()
            print("Review and rating saved successfully.")
        except Exception as e:
            print(f"Error saving review and rating: {e}. Please Try Again.")
        finally:
            db.close()


    @staticmethod
    def get_reviews_by_book(book_id):
        try:
            db = Database()
            db.cursor.execute("SELECT * FROM review_and_rating WHERE book_id = %s", (book_id,))
            reviews = db.cursor.fetchall()
            return reviews
        except Exception as e:
            print(f"An error occurred while fetching reviews: {e}")
            return None
        finally:
            db.close()


    @staticmethod
    def get_average_rating(book_id):
        try:
            db = Database()
            db.cursor.execute(
                "SELECT AVG(rating) FROM review_and_rating WHERE book_id = %s", (book_id,)
            )
            average_rating = db.cursor.fetchone()
            return average_rating[0] if average_rating else None
        except Exception as e:
            print(f"An error occurred while calculating average rating: {e}")
            return None
        finally:
            db.close()


    @staticmethod
    def get_reviews_by_user(user_id):
        try:
            db = Database()
            db.cursor.execute("SELECT * FROM review_and_rating WHERE user_id = %s", (user_id,))
            reviews = db.cursor.fetchall()
            return reviews
        except Exception as e:
            print(f"An error occurred while fetching user reviews: {e}")
            return None
        finally:
            db.close()


    @staticmethod
    def delete_review(review_id):
        try:
            db = Database()
            db.cursor.execute("DELETE FROM review_and_rating WHERE review_id = %s", (review_id,))
            db.commit()
            print("Review deleted successfully.")
        except Exception as e:
            print(f"Error deleting review: {e}. Please Try Again.")
        finally:
            db.close()
