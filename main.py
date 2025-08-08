import getpass
from datetime import datetime, timedelta
from models.book import Book
from models.insertData import insert_dummy_data
from models.user import User
from models.reviewAndRating import ReviewAndRating
from models.reservation import Reservation
import bcrypt

class LibraryApp:
    BORROW_DAYS = 14
    FINE_PER_DAY = 10

    def __init__(self):
        self.current_user = None


    def register(self):
        try:
            print("\n=== Register ===")
            username = input("Enter new username: ")
            password = getpass.getpass("Enter password: ")
            confirm_password = getpass.getpass("Confirm password: ")

            if password != confirm_password:
                print("Passwords do not match!")
                return False

            admin_choice = input("Is Admin? (y/n): ").lower()
            is_admin = True if admin_choice == 'y' else False

            existing_user = User.login(username, password) 
            if existing_user:
                print("Username already exists.")
                return False

            user = User(username, password, is_admin)
            user.save()
            print("User registered successfully.")
            return True
        except Exception as e:
            print(f"Registration failed: {e}")
            return False
        

    def create_admin(self):
        username = "admin"
        password = "admin"

        from models.user import User
        existing_user = User.login(username, password) 
        if not existing_user:
            user = User(username, password, True) 
            user.save()
            insert_dummy_data()
     

    def login(self):
        try:
            print("\n=== Login ===")
            username = input("Username: ")
            password = getpass.getpass("Password: ")
            user = User.login(username, password)
            if user:
                self.current_user = {
                    "user_id": user[0],
                    "username": user[1],
                    "is_admin": user[2]
                }
                print(f"Welcome, {self.current_user['username']}!")
                return True
            else:
                print("Invalid username or password.")
                return False
        except Exception as e:
            print(f"Login failed: {e}")
            return False

    def show_menu(self):
        while True:
            print("\n=== Menu ===")
            print("1. View All Books")
            print("2. View Book Details")
            print("3. Search Book by Title")
            print("4. Search Book by Author")
            print("5. Search Book by Category")
            print("6. Add Review and Rating")
            print("7. Borrow Book")
            print("8. Return Book")
            print("9. View Borrow History and Fines")
            print("10. Reserve a Book")
            print("11. Cancel Reservation")
            print("12. Update Password")
            if self.current_user['is_admin']:
                print("13. Add Book (Admin)")
                print("14. Update Book (Admin)")
                print("15. Update Book Quantity (Admin)")
                print("16. Delete Book (Admin)")
                print("17. Add User (Admin)")
                print("18. Search User by Id (Admin)")
                print("19. View All Users (Admin)")
                print("20. Delete User (Admin)")
                print("21. View Reservations (Admin)")
                print("22. Cancel User Reservation (Admin)")

            print("0. Logout")

            choice = input("Enter your choice: ")

            if choice == "1":
                self.view_books()
            elif choice == "2":
                self.view_book_details()
            elif choice == "3":
                self.search_books_by_title()
            elif choice == "4":
                self.search_books_by_author()
            elif choice == "5":
                self.search_books_by_category()
            elif choice == "6":
                self.add_review_and_rating()
            elif choice == "7":
                self.borrow_book()
            elif choice == "8":
                self.return_book()
            elif choice == "9":
                self.view_borrow_history_and_fines()
            elif choice == "10":
                self.reserve_book()
            elif choice == "11":
                self.cancel_reservation()
            elif choice == "12":
                self.update_password()

            elif choice == "13" and self.current_user['is_admin']:
                self.add_book()
            elif choice == "14" and self.current_user['is_admin']:
                self.update_book()
            elif choice == "15" and self.current_user['is_admin']:
                self.update_book_quantity()
            elif choice == "16" and self.current_user['is_admin']:
                self.delete_book()
            elif choice == "17" and self.current_user['is_admin']:
                self.add_user()
            elif choice == "18" and self.current_user['is_admin']:
                self.search_user_by_id()
            elif choice == "19" and self.current_user['is_admin']:
                self.view_users()
            elif choice == "20" and self.current_user['is_admin']:
                self.delete_user()
            elif choice == "21" and self.current_user['is_admin']:
                self.view_reservations()
            elif choice == "22" and self.current_user['is_admin']:
                self.cancel_user_reservation()

            elif choice == "0":
                print("Logged out.")
                break
            else:
                print("Invalid choice or permission denied.")

    # -- User methods --

    def add_book(self):
        title = input("Enter title: ")
        author = input("Enter author: ")
        category = input("Enter category: ")
        quantity = int(input("Enter quantity: "))
        book = Book(title, author, category, quantity)
        book.save()
        print("Book added successfully.")

    def view_book_details(self):
        book_id = int(input("Enter book ID: "))
        book = Book.get_book_by_id(book_id)
        if not book:
            print("Book not found.")
            return

        print(f"ID: {book[0]} | Title: {book[1]} | Author: {book[2]} | Category: {book[3]} | Quantity: {book[4]}")

        reviews = ReviewAndRating.get_reviews_by_book(book_id)
        if reviews:
            print("\nReviews and Ratings:")
            for r in reviews:
                print(f"User ID {r[2]}: {r[3]} (Rating: {r[4]})")
        else:
            print("No reviews for this book.")

        avg_rating = ReviewAndRating.get_average_rating(book_id)
        if avg_rating:
            print(f"\nAverage Rating: {avg_rating}")

    def view_books(self):
        books = Book.get_all_books()
        for book in books:
            print(f"ID: {book[0]} | Title: {book[1]} | Author: {book[2]} | Category: {book[3]} | Quantity: {book[4]}")

    def search_books_by_title(self):
        title = input("Enter title to search: ")
        books = Book.search_books_by_title(title)
        if books:
            for book in books:
                print(f"ID: {book[0]} | Title: {book[1]} | Author: {book[2]} | Category: {book[3]} | Quantity: {book[4]}")
        else:
            print("No books found.")

    def search_books_by_author(self):
        author = input("Enter author to search: ")
        books = Book.search_books_by_author(author)
        if books:
            for book in books:
                print(f"ID: {book[0]} | Title: {book[1]} | Author: {book[2]} | Category: {book[3]} | Quantity: {book[4]}")
        else:
            print("No books found.")

    def search_books_by_category(self):
        category = input("Enter category to search: ")
        books = Book.search_books_by_category(category)
        if books:
            for book in books:
                print(f"ID: {book[0]} | Title: {book[1]} | Author: {book[2]} | Category: {book[3]} | Quantity: {book[4]}")
        else:
            print("No books found.")

    def add_review_and_rating(self):
        book_id = int(input("Enter book ID to review: "))
        review = input("Write your review: ")
        rating = int(input("Enter rating (1 to 5): "))
        if rating < 1 or rating > 5:
            print("Invalid rating, must be 1 to 5.")
            return
        review_obj = ReviewAndRating(book_id, self.current_user["user_id"], review, rating)
        review_obj.save()
        print("Review added successfully.")

    def borrow_book(self):
        book_id = int(input("Enter book ID to borrow: "))
        history = Book.get_borrow_history_with_fines(self.current_user["user_id"])
        
        for record in history:
            if record["title"] == Book.get_book_by_id(book_id)[1] and record["return_date"] == "Not returned":
                print("You already borrowed this book and not returned yet.")
                return

        if Reservation.has_reservation(book_id):
            first_res = Reservation.get_first_reservation(book_id)
            if first_res.user_id != self.current_user["user_id"]:
                print("This book is reserved by another user. You cannot borrow it now.")
                return
            else:
                Reservation.delete_reservation(first_res.id)

        success, msg = Book.borrow_book(self.current_user["user_id"], book_id, self.BORROW_DAYS)
        print(msg)

    def return_book(self):
        book_id = int(input("Enter book ID to return: "))
        success, msg, fine = Book.return_book(self.current_user["user_id"], book_id, self.FINE_PER_DAY)
        print(msg)
        if success and fine > 0:
            print(f"You have a fine of {fine} units for late return.")

    def view_borrow_history_and_fines(self):
        history = Book.get_borrow_history_with_fines(self.current_user["user_id"], self.FINE_PER_DAY)
        for record in history:
            print(f"Book: {record['title']} | Borrowed: {record['borrow_date']} | Due: {record['due_date']} | Returned: {record['return_date']} | Fine: {record['fine']}")

    def reserve_book(self):
        book_id = int(input("Enter book ID to reserve: "))
        # Check if copies available
        available = Book.get_available_copies(book_id)
        if available > 0:
            print("Book copies are available now. You can borrow directly without reservation.")
            return

        # Check if user already reserved
        if Reservation.user_has_reservation(self.current_user["user_id"], book_id):
            print("You already reserved this book.")
            return

        Reservation.add_reservation(self.current_user["user_id"], book_id)
        print("Book reserved successfully.")

    def cancel_reservation(self):
        book_id = int(input("Enter book ID to cancel reservation: "))
        if Reservation.user_has_reservation(self.current_user["user_id"], book_id):
            Reservation.delete_user_reservation(self.current_user["user_id"], book_id)
            print("Reservation cancelled.")
        else:
            print("You have no reservation for this book.")

    def update_password(self):
        current_pass = getpass.getpass("Enter current password: ")
        user = User.login(self.current_user["username"], current_pass)
        if not user:
            print("Incorrect current password.")
            return
        new_pass = getpass.getpass("Enter new password: ")
        confirm_pass = getpass.getpass("Confirm new password: ")
        if new_pass != confirm_pass:
            print("Passwords do not match.")
            return
        User.update_password(self.current_user["user_id"], new_pass)
        print("Password updated successfully.")

    # -- Admin functions --

    def update_book(self):
        book_id = int(input("Enter book ID to update: "))
        book = Book.get_book_by_id(book_id)
        if not book:
            print("Book not found.")
            return
        title = input(f"New title ({book[1]}): ") or book[1]
        author = input(f"New author ({book[2]}): ") or book[2]
        category = input(f"New category ({book[3]}): ") or book[3]
        quantity_str = input(f"New quantity ({book[4]}): ")
        quantity = int(quantity_str) if quantity_str else book[4]
        Book.update_book(book_id, title, author, category, quantity)
        print("Book updated successfully.")

    def update_book_quantity(self):
        book_id = int(input("Enter book ID: "))
        book = Book.get_book_by_id(book_id)
        if not book:
            print("Book not found.")
            return
        quantity = int(input("Enter new quantity: "))
        Book.update_book_quantity(book_id, quantity)
        print("Quantity updated.")

    def delete_book(self):
        book_id = int(input("Enter book ID to delete: "))
        Book.delete_book(book_id)
        print("Book deleted.")

    def add_user(self):
        username = input("Enter new username: ")
        password = getpass.getpass("Enter password: ")
        admin_choice = input("Is admin? (y/n): ").lower()
        is_admin = admin_choice == 'y'
        user = User(username, password, is_admin)
        user.save()
        print("User added.")

    def search_user_by_id(self):
        user_id = int(input("Enter user ID: "))
        user = User.get_user_by_id(user_id)
        if user:
            print(f"ID: {user[0]}, Username: {user[1]}, Admin: {user[2]}")
        else:
            print("User not found.")

    def view_users(self):
        users = User.get_all_users()
        for user in users:
            print(f"ID: {user[0]}, Username: {user[1]}, Admin: {user[2]}")

    def delete_user(self):
        user_id = int(input("Enter user ID to delete: "))
        User.delete_user(user_id)
        print("User deleted.")

    def view_reservations(self):
        reservations = Reservation.get_all_reservations()
        for res in reservations:
            print(f"Res ID: {res[0]}, User: {res[1]}, Book: {res[2]}, Date: {res[3]}")

    def cancel_user_reservation(self):
        res_id = int(input("Enter reservation ID to cancel: "))
        Reservation.delete_reservation(res_id)
        print("Reservation cancelled.")


def main():
    app = LibraryApp()
    logged_in = False
    app.create_admin() 
    while not logged_in:
        print("\n=== Library Management System ===")
        print("1. Login")
        print("2. Register")
        print("0. Exit")
        choice = input("Enter your choice: ")

        if choice == "1":
            logged_in = app.login()
            if logged_in:
                app.show_menu()
        elif choice == "2":
            app.register()
        elif choice == "0":
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")
    


if __name__ == "__main__":
    main()
