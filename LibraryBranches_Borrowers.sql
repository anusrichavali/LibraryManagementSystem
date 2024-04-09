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
