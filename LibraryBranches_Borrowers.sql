Create Database LibraryManagementSystem;
Use LibraryManagementSystem;

Create Table LibraryBranches(
branchID int,
branchName VARCHAR(100),
branchAddress VARCHAR(500),
Primary Key (branchID)
);

Create Table Borrowers(
borrowerID int, 
fullName VARCHAR(100),
address VARCHAR(500),
card_no VARCHAR(10),
phone_no VARCHAR(10), 
Primary Key (borrowerID)
);

Insert Into LibraryBranches VALUES(1, "Alum Rock", 
"3090 Alum Rock Ave San Jose, CA 95127"), 
(2, "Berryessa", "3355 Noble Avenue
San Jose, CA 95132"), (3, "King Library", 
"150 E San Fernando St San Jose, CA 95112");

Insert Into Borrowers VALUES(1, 'John Doe', '123 Main St, San Jose, CA, USA', '1234567890', '4567890123'),
(2, 'Jane Smith', '456 Elm St, San Jose, CA, USA', '9876543210', '1234567890'),
(3, 'Michael Johnson', '789 Oak St, Sunnyvale, CA, USA', '4567890123', '9842839133'),
(4, 'Emily Brown', '321 Pine St, Hamletville, USA', '7890123456', '8760472937'),
(5, 'David Wilson', '555 Cedar St, Boroughtown, USA', '6543210987', '5104578293');

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

Select * from Book;
Select * From BookCopies;