def CreateTables(cursor):

    cursor.execute("CREATE DATABASE IF NOT EXISTS library_db")
    cursor.execute("USE library_db")

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INT AUTO_INCREMENT PRIMARY KEY,
            username VARCHAR(50) UNIQUE NOT NULL,
            password VARCHAR(255) NOT NULL,
            is_admin BOOLEAN DEFAULT FALSE
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS books (
            id INT AUTO_INCREMENT PRIMARY KEY,
            title VARCHAR(255) NOT NULL,
            author VARCHAR(255) NOT NULL,
            category VARCHAR(100),
            quantity INT DEFAULT 1
        )
    """)

    cursor.execute(""" 
        CREATE TABLE IF NOT EXISTS borrow_records (
            id INT AUTO_INCREMENT PRIMARY KEY,
            user_id INT,
            book_id INT,
            borrow_date DATETIME,
            due_date DATETIME,
            return_date DATETIME DEFAULT NULL,
            fine INT DEFAULT 0,
            FOREIGN KEY (user_id) REFERENCES users(id),
            FOREIGN KEY (book_id) REFERENCES books(id)
        )
    """)


    cursor.execute("""
        CREATE TABLE IF NOT EXISTS reviews (
            id INT AUTO_INCREMENT PRIMARY KEY,
            book_id INT,
            user_id INT,
            review TEXT,
            rating INT CHECK(rating >= 1 AND rating <= 5),
            FOREIGN KEY (book_id) REFERENCES books(id),
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
    """)


    cursor.execute("""
        CREATE TABLE IF NOT EXISTS reservations (
            id INT AUTO_INCREMENT PRIMARY KEY,
            user_id INT,
            book_id INT,
            reservation_date DATETIME,
            FOREIGN KEY (user_id) REFERENCES users(id),
            FOREIGN KEY (book_id) REFERENCES books(id)
        )
    """)
