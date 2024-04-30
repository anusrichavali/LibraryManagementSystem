import mysql.connector
from mysql.connector import Error
from flask import Flask
from flask import jsonify
from flask import request
from flask import render_template

app = Flask(__name__)

def connect_database():
    try:
        db = mysql.connector.connect(host='localhost', user='root', password='Delfina13', database='LibraryManagementSystem')
        if db.is_connected():
            print("The program has successfully connected to the LibraryManagementaSystem database.")
            return db
    except Error as er:
        print(f"There is an error in the connection process. {er}")

#CURD endpoints for the Book table

@app.route('/add_book', methods=['POST'])
def add_book():
    try:
        data = request.json
        book_id = data['book_id']
        title = data['title']
        authorFirstName = data['authorFirstName']
        authorLastName = data['authorLastName']
        genre = data['genre']

        conn = connect_database()
        cursor = conn.cursor()
        cursor.execute('INSERT INTO Book (book_id, title, authorFirstName, authorLastName, genre) VALUES (%s, %s, %s, %s, %s)', (book_id, title, authorFirstName, authorLastName, genre))
        conn.commit()
        conn.close()
        return jsonify({'message': 'Book added successfully'}), 201
    except Exception as e:
        return jsonify({'error': str(e) + ' is missing'}), 500

@app.route('/add_book', methods=['GET'])
def display_form():
    # Render the HTML form located in the templates directory
    return render_template('add_book.html')

@app.route('/books', methods=['GET'])
def get_books():
    try:
        conn = connect_database()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM Book')
        books = cursor.fetchall()
        conn.close()
        return books
    except Exception as e:
        print(f'error: {str(e)}')
        return []

@app.route('/books/<int:book_id>', methods=['PUT'])
def update_book(book_id):
    try:
        data = request.json
        title = data.get('title')
        authorFirstName = data.get('authorFirstName')
        authorLastName = data.get('authorLastName')
        genre = data.get('genre')

        conn = connect_database()
        cursor = conn.cursor()
        cursor.execute('UPDATE Book SET title = %s, authorFirstName = %s, authorLastName = %s, genre = %s WHERE book_id = %s', (title, authorFirstName, authorLastName, genre, book_id))
        conn.commit()
        if cursor.rowcount == 0:
            conn.close()
            return jsonify({'error': 'No such book found'}), 404
        conn.close()
        return jsonify({'message': 'Book updated successfully'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/books/<int:book_id>', methods=['DELETE'])
def delete_book(book_id):
    try:
        conn = connect_database()
        cursor = conn.cursor()
        cursor.execute('DELETE FROM Book WHERE book_id = %s', (book_id,))
        conn.commit()
        if cursor.rowcount == 0:
            conn.close()
            return jsonify({'error': 'No such book found'}), 404
        conn.close()
        return jsonify({'message': 'Book deleted successfully'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
#CURD emdpoints for the BookCopies table 
@app.route('/bookcopies', methods=['POST'])
def add_book_copy():
    try:
        data = request.json
        book_id = data['book_id']
        branch_id = data['branch_id']
        no_of_copies = data['no_of_copies']

        conn = connect_database()
        cursor = conn.cursor() 
        cursor.execute('INSERT INTO BookCopies (book_id, branch_id, no_of_copies) VALUES (%s, %s, %s)', (book_id, branch_id, no_of_copies))
        conn.commit()
        conn.close()
        return jsonify({'message': 'Book copy added successfully'}), 201
    except Exception as e:
        return jsonify({'error': str(e) + ' is missing'}), 500

#@app.route('/bookcopies', methods=['GET'])
def get_book_copies():
    try:
        conn = connect_database()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM BookCopies')
        book_copies = cursor.fetchall()
        conn.close()
        return book_copies
    except Exception as e:
        print(f'error: {str(e)}')
        return []

@app.route('/bookcopies/<int:book_id>', methods=['PUT'])
def update_book_copy(book_id):
    try:
        data = request.json
        branch_id = data.get('branch_id')
        no_of_copies = data.get('no_of_copies')

        conn = connect_database()
        cursor = conn.cursor()
        cursor.execute('UPDATE BookCopies SET branch_id = %s, no_of_copies = %s WHERE book_id = %s', (branch_id, no_of_copies, book_id))
        conn.commit()
        if cursor.rowcount == 0:
            conn.close()
            return jsonify({'error': 'No such book copy found'}), 404
        conn.close()
        return jsonify({'message': 'Book copy updated successfully'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/bookcopies/<int:book_id>', methods=['DELETE'])
def delete_book_copy(book_id):
    try:
        conn = connect_database()
        cursor = conn.cursor()
        cursor.execute('DELETE FROM BookCopies WHERE book_id = %s', (book_id,))
        conn.commit()
        if cursor.rowcount == 0:
            conn.close()
            return jsonify({'error': 'No such book copy found'}), 404
        conn.close()
        return jsonify({'message': 'Book copy deleted successfully'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

#CRUD operations on Library Branches
@app.route('/LibraryBranches', methods = ['POST'])
def add_branch():
    try:
        data = request.json
        branch_id = data['branch_id']
        branchName = data['branch name']
        branchAddress = data['branch address']

        connection = connect_database()
        cursor = connection.cursor()
        cursor.execute('INSERT INTO LibraryBranches (branch_id, branchName, branchAddress) VALUES (%s, %s, %s)', (branch_id, branchName, branchAddress))
        connection.commit()
        connection.close()
        return jsonify({'message': 'Branch added successfully'}), 201
    except Exception as e:
        return jsonify({'error': str(e) + ' is missing'}), 500

#@app.route('/LibraryBranches', methods=['GET'])
def get_branches():
    try:
        connection = connect_database()
        cursor = connection.cursor()
        cursor.execute('SELECT * FROM LibraryBranches')
        branches = cursor.fetchall()
        connection.close()
        return branches
    except Exception as e:
        print(f'error: {str(e)}')
        return []
    
@app.route('/LibraryBranches/<int:branch_id>', methods=['POST'])
def update_branch(branch_id):
    try:
        branch_name = request.form['branch_name']
        branch_address = request.form["branch_address"]

        connection = connect_database()
        cursor = connection.cursor()
        cursor.execute("Update LibraryBranches SET branchName = (%s), branchAddress = (%s) WHERE branch_id = (%s)", (branch_name, branch_address, branch_id))
        connection.commit()
        connection.close()
        return render_template('responses.html', message='Successfully updated branch')
    except Exception as ex:
        return render_template('responses.html', message='Error in branch update: ' + str(ex))
    
@app.route('/edit_branch/<int:branch_id>', methods=['GET'])
def edit_branch(branch_id):
    connection = connect_database()
    cursor = connection.cursor()
    cursor.execute('SELECT * FROM LibraryBranches WHERE branch_id = %s', (branch_id,))
    branch = cursor.fetchone()
    connection.close()
    if branch:
        return render_template('edit_branch.html', branch=branch)
    else:
        return 'Branch not found', 404
    
@app.route('/LibraryBranches/<int:branch_id>', methods=['DELETE'])
def delete_branch(branch_id):
    try:
        conn = connect_database()
        cursor = conn.cursor()
        cursor.execute('DELETE FROM LibraryBranches WHERE branch_id = %s', (branch_id,))
        conn.commit()
        conn.close()
        return jsonify({'message': 'Branch deleted successfully'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
#CRUD operations on borrowers
@app.route('/Borrowers', methods = ['POST'])
def add_borrower():
    try:
        data = request.json
        borrower_id = data['borrower_id']
        fullName = data['full name']
        address = data['address']
        card_no = data['card number']
        phone_no = data['phone number']

        connection = connect_database()
        cursor = connection.cursor()
        cursor.execute('INSERT INTO Borrowers (borrower_id, fullName, address, card_no, phone_no) VALUES (%s, %s, %s, %s, %s)', (borrower_id, fullName, address, card_no, phone_no))
        connection.commit()
        connection.close()
        return jsonify({'message': 'Borrower added successfully'}), 201
    except Exception as e:
        return jsonify({'error': str(e) + ' is missing'}), 500

#@app.route('/Borrowers', methods=['GET'])
def get_borrowers():
    try:
        connection = connect_database()
        cursor = connection.cursor()
        cursor.execute('SELECT * FROM Borrowers')
        borrowers = cursor.fetchall()
        connection.close()
        return borrowers
    except Exception as e:
        print(f'error: {str(e)}')
        return []
    
@app.route('/Borrowers/<int:borrower_id>', methods = ['POST'])
def update_borrower(borrower_id):
    try:
        borrower_name = request.form['borrower_name']
        borrower_address = request.form["borrower_address"]
        borrower_phoneno = request.form["borrower_phone_no"]

        connection = connect_database()
        cursor = connection.cursor()
        cursor.execute("Update Borrowers SET fullName = (%s), address = (%s), phone_no = (%s) WHERE borrower_id = (%s)", (borrower_name, borrower_address, borrower_phoneno, borrower_id))
        connection.commit()
        connection.close()
        return render_template('responses.html', message='Successfully updated borrower')
    except Exception as ex:
        return render_template('responses.html', message='Error in borrower update: ' + str(ex))
    
@app.route('/edit_borrower/<int:borrower_id>', methods=['GET'])
def edit_borrower(borrower_id):
    connection = connect_database()
    cursor = connection.cursor()
    cursor.execute('SELECT borrower_id, fullName, address, phone_no FROM Borrowers WHERE borrower_id = %s', (borrower_id,))
    borrower = cursor.fetchone()
    connection.close()
    if borrower:
        return render_template('edit_borrower.html', borrower=borrower)
    else:
        return 'Borrower not found', 404
    
@app.route('/Borrowers/<int:borrower_id>', methods=['DELETE'])
def delete_borrower(borrower_id):
    try:
        conn = connect_database()
        cursor = conn.cursor() 
        cursor.execute('DELETE FROM Borrowers WHERE borrower_id = %s', (borrower_id,))
        conn.commit()
        conn.close()
        return jsonify({'message': 'Borrower deleted successfully'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
@app.route('/')
def index():
    branches = get_branches()
    borrowers = get_borrowers()
    books = get_books()
    book_copies = get_book_copies()
    return render_template('index.html', branches = branches, borrowers = borrowers, books = books, book_copies = book_copies)


@app.route('/book')
def book():
    books = get_books()
    book_copies = get_book_copies()
    return render_template('book.html',books = books, book_copies = book_copies)

@app.route('/branches')
def branches():
    branches = get_branches()
    return render_template('branches.html', branches = branches)

@app.route('/borrowers')
def borrowers():
    borrowers = get_borrowers()
    return render_template('borrowers.html', borrowers = borrowers)

app.run(debug=True)
