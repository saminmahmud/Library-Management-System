def CreateTables(cursor):

    cursor.execute("CREATE DATABASE IF NOT EXISTS library_db")
    cursor.execute("USE library_db")

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS user (
            user_id INT AUTO_INCREMENT PRIMARY KEY,
            username VARCHAR(50) NOT NULL,
            password VARCHAR(255) NOT NULL,
            is_admin BOOLEAN NOT NULL DEFAULT FALSE
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS book (
            book_id INT AUTO_INCREMENT PRIMARY KEY,
            title VARCHAR(100) NOT NULL,
            author VARCHAR(100) NOT NULL,
            category VARCHAR(150) NOT NULL,
            quantity INT DEFAULT 1
        )
    """)

    cursor.execute(""" 
        CREATE TABLE IF NOT EXISTS borrow (
            borrow_id INT AUTO_INCREMENT PRIMARY KEY,
            user_id INT NOT NULL,
            book_id INT NOT NULL,
            borrow_date DATE NOT NULL,
            return_date DATE,
            FOREIGN KEY (user_id) REFERENCES user(user_id),
            FOREIGN KEY (book_id) REFERENCES book(book_id)
        )
    """)


    cursor.execute("""
        CREATE TABLE IF NOT EXISTS review_and_rating (
            review_id INT AUTO_INCREMENT PRIMARY KEY,
            user_id INT NOT NULL,
            book_id INT NOT NULL,
            rating INT CHECK (rating >= 1 AND rating <= 5),
            review TEXT,
            FOREIGN KEY (user_id) REFERENCES user(user_id),
            FOREIGN KEY (book_id) REFERENCES book(book_id)
        )
    """)

