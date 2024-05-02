# Library Management System
<img width="1466" alt="Screenshot 2024-05-01 at 10 40 58 PM" src="https://github.com/anusrichavali/LibraryManagementSystem/assets/41877636/eb7afad8-38b4-4be5-9adb-11cb117d5dc1">
This project is a Library Management System developed using Python and MySQL, with Flask as the web framework. It provides CRUD operations for books, borrowers, library branches, book copies, and book loans. The system has a web-based interface, allowing users to interact with the library's data.

## Features
- Add, update, and delete books, borrowers, library branches, book copies, and book loans.
- View existing data through a user-friendly web interface.
- Built with Python/Flask for backend and MySQL for database management.

## Installation
To set up the project locally, follow these steps:

1. Clone the repository:
   ```bash
   git clone <https://github.com/anusrichavali/LibraryManagementSystem>
2. Set up a virtual environment and install required dependencies:
   ```bash
   cd <project-directory>
   python -m venv venv
   source venv/bin/activate  # On Windows, use venv\Scripts\activate
   pip install -r requirements.txt
3. Configure MySQL and create the database:
- Ensure MySQL is installed and running.
- Create a new database named LibraryManagementSystem.
- Run the provided SQL script to set up the database schema and initial data.
4. Configure the Flask application:
- Update the connect_database() function in library_management_api.py with your MySQL credentials.

## To Run
To start the Flask development server, run:
```bash
 python library_management_api.py
