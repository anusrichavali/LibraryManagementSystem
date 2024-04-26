import mysql.connector
from mysql.connector import Error
from flask import Flask
from flask import jsonify
from flask import request
from flask import render_template

app = Flask(__name__)

def connect_database():
    try:
        db = mysql.connector.connect(host='localhost', user='root', password='Delfina13!', database='LibraryManagementSystem')
        if db.is_connected():
            print("The program has successfully connected to the LibraryManagementaSystem database.")
            return db
    except Error as er:
        print(f"There is an error in the connection process. {er}")
@app.route('/')      
def index():
    return render_template('index.html')

#CURD endpoints for the Book table

@app.route('/books', methods=['POST'])
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

@app.route('/books', methods=['GET'])
def get_books():
    try:
        conn = connect_database()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM Book')
        books = cursor.fetchall()
        conn.close()
        return jsonify(books), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

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

@app.route('/bookcopies', methods=['GET'])
def get_book_copies():
    try:
        conn = connect_database()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM BookCopies')
        book_copies = cursor.fetchall()
        conn.close()
        return jsonify(book_copies), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

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

@app.route('/LibraryBranches', methods=['GET'])
def get_branches():
    try:
        connection = connect_database()
        cursor = connection.cursor()
        cursor.execute('SELECT * FROM LibraryBranches')
        branches = cursor.fetchall()
        connection.close()
        return jsonify(branches), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
@app.route('/LibraryBranches/<int:branch_id>', methods = ['PUT'])
def update_branch(branch_id):
    try:
        data = request.get_json()
        categories_to_update = data.keys()
        columns = ['branchName', 'branchAddress']
        for i in categories_to_update:
            if i not in columns:
                raise Exception("Invalid column name provided.")

        connection = connect_database()
        cursor = connection.cursor()
        if 'branchName' in categories_to_update:
            branchName = data['branchName']
            cursor.execute("Update LibraryBranches SET branchName = (%s) WHERE branch_id = (%s)", (branchName, branch_id))
        if 'branchAddress' in categories_to_update:
            branchAddress = data['branchAddress']
            cursor.execute("Update LibraryBranches SET branchAddress = (%s) WHERE branch_id = (%s)", (branchAddress, branch_id))
        connection.commit()
        connection.close()
        return jsonify({'message': 'branch successfully updated'}), 201
    except Exception as ex:
        return jsonify({'error in branch update': str(ex)}), 500
    
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

@app.route('/Borrowers', methods=['GET'])
def get_borrowers():
    try:
        connection = connect_database()
        cursor = connection.cursor()
        cursor.execute('SELECT * FROM Borrowers')
        branches = cursor.fetchall()
        connection.close()
        return jsonify(branches), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
@app.route('/Borrowers/<int:borrower_id>', methods = ['PUT'])
def update_borrower(borrower_id):
    try:
        data = request.get_json()
        categories_to_update = data.keys()
        columns = ['fullName', 'address', 'phone_no']
        for i in categories_to_update:
            if i not in columns:
                raise Exception("Invalid column name provided.")

        connection = connect_database()
        cursor = connection.cursor()
        if 'fullName' in categories_to_update:
            fullName = data['full name']
            cursor.execute("Update Borrowers SET fullName = (%s) WHERE borrower_id = (%s)", (fullName, borrower_id))
        if 'address' in categories_to_update:
            address = data['address']
            cursor.execute("Update Borrowers SET address = (%s) WHERE borrower_id = (%s)", (address, borrower_id))
        if 'phone_no' in categories_to_update:
            phone_no = data['phone_no']
            cursor.execute("Update Borrowers SET phone_no = (%s) WHERE borrower_id = (%s)", (phone_no, borrower_id))
        connection.commit()
        connection.close()
        return jsonify({'message': 'borrower information successfully updated'}), 201
    except Exception as ex:
        return jsonify({'error in task update': str(ex)}), 500
    
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

app.run(debug=True)

