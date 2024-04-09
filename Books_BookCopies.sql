CREATE TABLE Book (
    book_id INT PRIMARY KEY,
    title VARCHAR(255),
    authorFirstName VARCHAR(100),
    authorLastName VARCHAR(100),
    genre VARCHAR(100)
);

CREATE TABLE BookCopies (
    book_id INT,
    branch_id INT,
    no_of_copies INT,
    FOREIGN KEY (book_id) REFERENCES Book(book_id)
   
);


INSERT INTO Book (book_id, title, authorFirstName, authorLastName, genre) VALUES
(1, 'The Great Gatsby', 'F. Scott', 'Fitzgerald', 'Classic'),
(2, 'To Kill a Mockingbird', 'Harper', 'Lee', 'Fiction'),
(3, '1984', 'George', 'Orwell', 'Dystopian'),
(4, 'The Catcher in the Rye', 'J.D.', 'Salinger', 'Fiction'),
(5, 'Pride and Prejudice', 'Jane', 'Austen', 'Romance'),
(6, 'Moby-Dick', 'Herman', 'Melville', 'Adventure'),
(7, 'War and Peace', 'Leo', 'Tolstoy', 'Historical Fiction'),
(8, 'The Odyssey', 'Homer', '', 'Epic'),
(9, 'Hamlet', 'William', 'Shakespeare', 'Tragedy'),
(10, 'The Divine Comedy', 'Dante', 'Alighieri', 'Epic Poem');

INSERT INTO BookCopies (book_id, branch_id, no_of_copies) VALUES
(1, 1, 3),
(2, 3, 2),
(3, 1, 4),
(4, 2, 5),
(5, 1, 3),
(6, 2, 3),
(7, 2, 2),
(8, 3, 4),
(9, 2, 5),
(10, 3, 3);
