from models.book import Book
from models.user import User
from models.reviewAndRating import ReviewAndRating


class LibraryApp:
    def __init__(self):
        self.current_user = None
    

    def login(self):
        try:
            print("\n=== Login ===")
            username = input("Username: ")
            password = input("Password: ")
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
            print(f"Login failed due to error: {e}")
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
            print("9. View Borrow History")

            print("10. Update Password")
            if self.current_user['is_admin']:
                print("11. Add Book (Admin)")
                print("12. Update Book (Admin)")
                print("13. Update Book Quantity (Admin)")
                print("14. Delete Book (Admin)")

                print("15. Add User (Admin)")
                print("16. Search User by Id (Admin)")
                print("17. View All Users (Admin)")
                print("18. Delete User (Admin)")

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
                self.get_borrow_history()
            elif choice == "10":
                self.update_password()

            elif choice == "11" and self.current_user['is_admin']:
                self.add_book()
            elif choice == "12" and self.current_user['is_admin']:
                self.update_book()
            elif choice == "13" and self.current_user['is_admin']:
                self.update_book_quantity()
            elif choice == "14" and self.current_user['is_admin']:
                self.delete_book()
            elif choice == "15" and self.current_user['is_admin']:
                self.add_user()
            elif choice == "16" and self.current_user['is_admin']:
                self.search_user_by_id()
            elif choice == "17" and self.current_user['is_admin']:
                self.view_users()
            elif choice == "18" and self.current_user['is_admin']:
                self.delete_user()
            elif choice == "0":
                print("Logged out.")
                break
            else:
                print("Invalid choice or permission denied.")



    def add_book(self):
        title = input("Enter title: ")
        author = input("Enter author: ")
        category = input("Enter category: ")
        quantity = int(input("Enter quantity: "))
        book = Book(title, author, category, quantity)
        book.save()


    def view_book_details(self):
        book_id = int(input("Enter book ID: "))
        book = Book.get_book_by_id(book_id)
        review_and_rating = ReviewAndRating.get_reviews_by_book(book_id)
        average_rating = ReviewAndRating.get_average_rating(book_id)

        if book:
            print(book)


            if review_and_rating:
                print(f"Reviews for Book ID {book_id}:")
                for review in review_and_rating:
                    print(f"User ID {review[1]}: {review[2]} (Rating: {review[3]})")
            

            if average_rating:
                print(f"Average Rating for Book ID {book_id}: {average_rating}")
            else:
                print(f"No reviews found for Book ID {book_id}.")
            
            
            if average_rating:
                print(f"Average Rating for Book ID {book_id}: {average_rating}")
            else:
                print("No reviews found for this book.")
        else:
            print("Book not found.")


    def view_books(self):
        books = Book.get_all_books()
        for book in books:
            print(book)


    def search_books_by_title(self):
        title = input("Enter title to search: ")
        books = Book.search_books_by_title(title)
        for book in books:
            print(book)


    def search_books_by_author(self):
        author = input("Enter author to search: ")
        books = Book.search_books_by_author(author)
        for book in books:
            print(book)


    def search_books_by_category(self):
        category = input("Enter category to search: ")
        books = Book.search_books_by_category(category)
        for book in books:
            print(book)


    def update_book(self):
        book_id = int(input("Enter book ID to update: "))
        title = input("Enter new title: ")
        author = input("Enter new author: ")
        category = input("Enter new category: ")
        quantity = int(input("Enter new quantity: "))
        Book.update_book(book_id, title, author, category, quantity)


    def delete_book(self):
        book_id = int(input("Enter book ID to delete: "))
        Book.delete_book(book_id)


    def add_review_and_rating(self):
        book_id = int(input("Enter book ID to review: "))
        user_id = self.current_user["user_id"]
        review = input("Write your review: ")
        rating = int(input("Enter your rating (1-5): "))
        
        if not (1 <= rating <= 5):
            print("Rating must be between 1 and 5.")
            return
        
        review_and_rating = ReviewAndRating(book_id, user_id, review, rating)
        review_and_rating.save()

    
    def borrow_book(self):
        book_id = int(input("Enter book ID to borrow: "))
        user_id = self.current_user["user_id"]
        Book.borrow_book(user_id, book_id)
       

    def return_book(self):
        book_id = int(input("Enter book ID to return: "))
        user_id = self.current_user["user_id"]
        Book.return_book(user_id, book_id)
        
    
    def get_borrow_history(self):
        user_id = self.current_user["user_id"]
        borrow_history = Book.get_borrow_history(user_id)
        if borrow_history:
            print("Borrow History:")
            for record in borrow_history:
                print(record)
        else:
            print("No borrow history found.")


    def update_book_quantity(self):
        book_id = int(input("Enter book ID to update quantity: "))
        quantity = int(input("Enter new quantity: "))
        Book.update_book_quantity(book_id, quantity)

    
    def add_user(self):
        username = input("Enter username: ")
        password = input("Enter password: ")
        is_admin_input = input("Is admin (yes/no)? ").strip().lower()
        is_admin = is_admin_input == "yes"
        user = User(username, password, is_admin)
        user.save()


    def view_users(self):
        users = User.get_all_users()
        for user in users:
            print(user)

    
    def search_user_by_id(self):
        user_id = int(input("Enter user ID to search: "))
        user = User.get_user_by_id(user_id)
        if user:
            print(user)
        else:
            print("User not found.")


    def delete_user(self):
        user_id = int(input("Enter user ID to delete: "))
        User.delete_user(user_id)


    def update_password(self):
        new_password = input("Enter new password: ")
        User.update_password(self.current_user["user_id"], new_password)
        print("Password updated successfully.")



if __name__ == "__main__":
    app = LibraryApp()
    while True:
        print("\n====== Library Management System ======")
        if app.login():
            app.show_menu()



