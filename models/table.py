def CreateTables(cursor):

    cursor.execute("CREATE DATABASE IF NOT EXISTS library_database")
    cursor.execute("USE library_database")

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



    # # add some books
    # cursor.execute("""
    #     INSERT INTO books (title, author, category, quantity)
    #     VALUES 
    #     ('The Great Gatsby', 'F. Scott Fitzgerald', 'Fiction', 5),
    #     ('To Kill a Mockingbird', 'Harper Lee', 'Fiction', 3),
    #     ('1984', 'George Orwell', 'Dystopian', 4),
    #     ('Pride and Prejudice', 'Jane Austen', 'Romance', 2),
    #     ('The Catcher in the Rye', 'J.D. Salinger', 'Fiction', 6)
    # """)

    # # add some borrow_records
    # cursor.execute("""
    #     INSERT INTO borrow_records (user_id, book_id, borrow_date, due_date)
    #     VALUES 
    #     (1, 1, NOW(), DATE_ADD(NOW(), INTERVAL 14 DAY)),
    #     (1, 2, NOW(), DATE_ADD(NOW(), INTERVAL 14 DAY)),
    #     (2, 3, NOW(), DATE_ADD(NOW(), INTERVAL 14 DAY))
    # """)

    # # add some reviews
    # cursor.execute("""
    #     INSERT INTO reviews (book_id, user_id, review, rating)
    #     VALUES 
    #     (1, 1, 'A masterpiece of 20th century literature.', 5),
    #     (2, 1, 'A powerful story about racial injustice.', 4),
    #     (3, 2, 'A chilling depiction of a totalitarian regime.', 5),
    #     (4, 2, 'A timeless romance with sharp social commentary.', 4),
    #     (5, 1, 'A thought-provoking exploration of teenage angst.', 4)
    # """)

    # # add some reservations
    # cursor.execute("""
    #     INSERT INTO reservations (user_id, book_id, reservation_date)
    #     VALUES 
    #     (1, 1, NOW()),
    #     (2, 2, NOW()),
    #     (1, 3, NOW())
    # """)
