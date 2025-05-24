from models.database import Database


class Book:
    def __init__(self, title, author, category, quantity):
        self.title = title
        self.author = author
        self.category = category
        self.quantity = quantity

    
    def save(self):
        try:
            db = Database()
            db.cursor.execute(
                "INSERT INTO book (title, author, category, quantity) VALUES (%s, %s, %s, %s)",
                (self.title, self.author, self.category, self.quantity)
            )
            db.commit()
            print("Book created successfully.")
        except Exception as e:
            print(f"Error saving book: {e}. Please Try Again.")
        finally:
            db.close()
    
    
    @staticmethod
    def get_all_books():
        try:
            db = Database()
            db.cursor.execute("SELECT * FROM book")
            books = db.cursor.fetchall()
            return books
        except Exception as e:
            print(f"An error occurred while fetching books: {e}")
            return None
        finally:
            db.close()
    
    
    @staticmethod
    def get_book_by_id(book_id):
        try:
            db = Database()
            db.cursor.execute("SELECT * FROM book WHERE book_id = %s", (book_id,))
            book = db.cursor.fetchone()
            return book
        except Exception as e:
            print(f"An error occurred while fetching the book: {e}")
            return None
        finally:
            db.close()
    
    
    @staticmethod
    def update_book(book_id, title, author, category, quantity):
        try:
            db = Database()
            db.cursor.execute(
                "UPDATE book SET title = %s, author = %s, category = %s, quantity = %s WHERE book_id = %s",
                (title, author, category, quantity, book_id)
            )
            db.commit()
            print("Book updated successfully.")
        except Exception as e:
            print(f"Error updating book: {e}. Please Try Again.")
        finally:
            db.close()
    
    
    @staticmethod
    def delete_book(book_id):
        try:
            db = Database()
            db.cursor.execute("DELETE FROM book WHERE book_id = %s", (book_id,))
            db.commit()
            print("Book deleted successfully.")
        except Exception as e:
            print(f"Error deleting book: {e}. Please Try Again.")
        finally:
            db.close()
    
    
    @staticmethod
    def search_books_by_title(title):
        try:
            db = Database()
            db.cursor.execute("SELECT * FROM book WHERE title LIKE %s", ('%' + title + '%',))
            books = db.cursor.fetchall()
            return books
        except Exception as e:
            print(f"An error occurred while searching for books: {e}")
            return None
        finally:
            db.close()
    
    
    @staticmethod
    def search_books_by_author(author):
        try:
            db = Database()
            db.cursor.execute("SELECT * FROM book WHERE author LIKE %s", ('%' + author + '%',))
            books = db.cursor.fetchall()
            return books
        except Exception as e:
            print(f"An error occurred while searching for books: {e}")
            return None
        finally:
            db.close()
    
    
    @staticmethod
    def search_books_by_category(category):
        try:
            db = Database()
            db.cursor.execute("SELECT * FROM book WHERE category LIKE %s", ('%' + category + '%',))
            books = db.cursor.fetchall()
            return books
        except Exception as e:
            print(f"An error occurred while searching for books: {e}")
            return None
        finally:
            db.close()
  
    
    @staticmethod
    def update_book_quantity(book_id, quantity):
        try:
            db = Database()
            db.cursor.execute(
                "UPDATE book SET quantity = %s WHERE book_id = %s",
                (quantity, book_id)
            )
            db.commit()
            print("Book quantity updated successfully.")
        except Exception as e:
            print(f"Error updating book quantity: {e}. Please Try Again.")
        finally:
            db.close()


    @staticmethod
    def borrow_book(user_id, book_id):
        try:
            db = Database()
            db.cursor.execute(
                "INSERT INTO borrow (user_id, book_id, borrow_date) VALUES (%s, %s, NOW())",
                (user_id, book_id)
            )
            db.commit()
            print("Book borrowed successfully.")
        except Exception as e:
            print(f"Error borrowing book: {e}. Please Try Again.")
        finally:
            db.close()


    @staticmethod
    def return_book(user_id, book_id):
        try:
            db = Database()
            db.cursor.execute(
                "UPDATE borrow SET return_date = NOW() WHERE user_id = %s AND book_id = %s AND return_date IS NULL",
                (user_id, book_id)
            )
            db.commit()
            print("Book returned successfully.")
        except Exception as e:
            print(f"Error returning book: {e}. Please Try Again.")
        finally:
            db.close()


    @staticmethod   
    def get_borrow_history(user_id):
        try:
            db = Database()
            db.cursor.execute(
                "SELECT b.book_id, b.title, b.author, br.borrow_date, br.return_date "
                "FROM book b JOIN borrow br ON b.book_id = br.book_id "
                "WHERE br.user_id = %s",
                (user_id,)
            )
            borrow_history = db.cursor.fetchall()
            return borrow_history
        except Exception as e:
            print(f"An error occurred while fetching borrow history: {e}")
            return None
        finally:
            db.close()