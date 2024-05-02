import mysql.connector
from mysql.connector import Error
from flask import Flask
from flask import jsonify
from flask import request
from flask import render_template

app = Flask(__name__)

def connect_database():
    try:
        db = mysql.connector.connect(host='localhost', user='project', password='final_proj13!', database='LibraryManagementSystem')
        if db.is_connected():
            print("The program has successfully connected to the LibraryManagementaSystem database.")
            return db
    except Error as er:
        print(f"There is an error in the connection process. {er}")

#CRUD endpoints for the Book table

@app.route('/add_book', methods=['POST'])
def add_book():
    try:
        data = request.json
        book_id = data['book_id']
        title = data['title']
        authorFirstName = data['authorFirstName']
        authorLastName = data['authorLastName']
        genre = data['genre']
        borrower_id = request.args.get('title')
        conn = connect_database()
        cursor = conn.cursor()
        if title:
            cursor.execute('SELECT * FROM Book WHERE title = %s', (title,))
        else:
            cursor.execute('SELECT * FROM Book')
        book_loans = cursor.fetchall()
        conn.close()
        return render_template('book.html', books=book)
    except Error as db_err:
        return jsonify({'error': str(db_err)}), 500

@app.route('/add_book', methods=['GET'])
def display_form():
    # Render the HTML form located in the templates directory
    return render_template('add_book.html')

@app.route('/book', methods=['GET'])
def get_books():
    title = request.args.get('title', '')  # Default empty if title is not provided
    try:
        conn = connect_database()
        cursor = conn.cursor()
        query = "SELECT * FROM Book WHERE title LIKE %s"
        cursor.execute(query, ('%' + title + '%',))
        books = cursor.fetchall()
        conn.close()
        return render_template('book.html', books=books)
    except Exception as e:
        print(f'Error: {str(e)}')
        return jsonify({'error': 'Internal Server Error'}), 500


@app.route('/books/<int:book_id>', methods=['POST'])
def update_book(book_id):
    try:
        title = request.form['title']
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        genre = request.form['genre']
        connection = connect_database()
        cursor = connection.cursor()
        cursor.execute("Update Book SET title = (%s), authorFirstName = (%s), authorLastName = (%s), genre = (%s) WHERE book_id = (%s)", (title, first_name, last_name, genre, book_id))
        connection.commit()
        connection.close()
        return render_template('responses.html', message='Successfully updated book', url = '/book')
    except Exception as ex:
        return render_template('responses.html', message='Error in book update: ' + str(ex), url = '/book')
    
@app.route('/edit_book/<int:book_id>', methods=['GET'])
def edit_book(book_id):
    connection = connect_database()
    cursor = connection.cursor()
    cursor.execute('SELECT * FROM Book WHERE book_id = %s', (book_id,))
    book = cursor.fetchone()
    connection.close()
    if book:
        return render_template('edit_book.html', book = book)
    else:
        return 'Book not found', 404

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
    
#CURD endpoints for the BookCopies table 
@app.route('/bookcopies', methods=['POST'])
def add_book_copy():
    try:
        data = request.json
        book_id = int(data['book_id'])  # Convert to integer if not already
        title = data['title']
        branch_id = int(data['branch_id'])  # Convert to integer if not already
        no_of_copies = int(data['no_of_copies'])  # Explicitly convert to integer

        conn = connect_database()
        cursor = conn.cursor()

        # Check if the entry exists
        cursor.execute('SELECT no_of_copies FROM BookCopies WHERE book_id = %s AND branch_id = %s', (book_id, branch_id))
        result = cursor.fetchone()
        if result:
            # If entry exists, increment the number of copies
            total_copies = result[0] + no_of_copies
            cursor.execute('UPDATE BookCopies SET title = %s, no_of_copies = %s WHERE book_id = %s AND branch_id = %s', (title, total_copies, book_id, branch_id))
        else:
            # Else, create a new entry
            cursor.execute('INSERT INTO BookCopies (book_id, title, branch_id, no_of_copies) VALUES (%s, %s, %s, %s)', (book_id, title, branch_id, no_of_copies))
        conn.commit()
        conn.close()
        return jsonify({'message': 'Book copy added or updated successfully'}), 201
    except Exception as e:
        if conn:
            conn.rollback()
        return jsonify({'error': str(e)}), 500
    
@app.route('/add_bookcopies', methods=['GET'])
def display_form_copies():
    # Render the HTML form located in the templates directory
    return render_template('add_bookcopies.html')


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
    

@app.route('/bookcopies/<int:book_id>', methods=['GET'])
def get_book_copies1(book_id):
    try:
        conn = connect_database()
        cursor = conn.cursor()
        # Query to get copies of the specific book by book_id
        cursor.execute('SELECT * FROM BookCopies WHERE book_id = %s', (book_id,))
        book_copies = cursor.fetchall()
        conn.close()
        # Render an HTML template and pass the book copies data
        return render_template('book_copies.html', book_copies=book_copies, book_id=book_id)
    except Exception as e:
        print(f'error: {str(e)}')
        return render_template('error.html', error=str(e))  # Assume you have an error.html template

@app.route('/bookcopies/<int:book_id>', methods=['POST'])
def update_book_copy(book_id):
    try:
        title = request.form['title']
        branch_id = request.form['branch_id']
        no_of_copies = request.form['no_of_copies']
        connection = connect_database()
        cursor = connection.cursor()
        cursor.execute("Update BookCopies SET title = (%s), branch_id = (%s), no_of_copies = (%s) WHERE book_id = (%s)", (title, branch_id, no_of_copies, book_id))
        connection.commit()
        connection.close()
        return render_template('responses.html', message='Successfully updated book copy', url = '/book')
    except Exception as ex:
        return render_template('responses.html', message='Error in book copy update: ' + str(ex), url = '/book')

@app.route('/edit_book_copy/<int:book_id>', methods=['GET'])
def edit_book_copy(book_id):
    connection = connect_database()
    cursor = connection.cursor()
    cursor.execute('SELECT * FROM BookCopies WHERE book_id = %s', (book_id,))
    book_copy = cursor.fetchone()
    connection.close()
    if book_copy:
        return render_template('edit_book_copy.html', book_copy = book_copy)
    else:
        return 'Book not found', 404
    
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
@app.route('/add_branch', methods = ['POST'])
def add_branch():
    try:
        data = request.json
        branch_id = data['branch_id']
        branchName = data['branch_name']
        branchAddress = data['branch_address']

        connection = connect_database()
        cursor = connection.cursor()
        cursor.execute('INSERT INTO LibraryBranches (branch_id, branchName, branchAddress) VALUES (%s, %s, %s)', (branch_id, branchName, branchAddress))
        connection.commit()
        connection.close()
        return jsonify({'message': 'Branch added successfully'}), 201
    except Exception as e:
        return jsonify({'error': str(e) + ' is missing'}), 500

@app.route('/add_branch', methods=['GET'])
def display_form_branch():
    # Render the HTML form located in the templates directory
    return render_template('add_branch.html')

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
        return render_template('responses.html', message='Successfully updated branch', url = '/branches')
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


@app.route('/add_borrower', methods=['GET'])
def display_form_borrower():
    # Render the HTML form located in the templates directory
    return render_template('add_borrower.html')

@app.route('/borrowers', methods=['GET'])
def get_borrowers():
    borrower_id = request.args.get('borrower_id')
    try:
        connection = connect_database()
        cursor = connection.cursor()
        if borrower_id:
            # If a borrower_id is provided, filter the results
            cursor.execute("SELECT * FROM Borrowers WHERE borrower_id = %s", (borrower_id,))
        else:
            # If no borrower_id, retrieve all borrowers
            cursor.execute("SELECT * FROM Borrowers")
        borrowers = cursor.fetchall()
        connection.close()
        return render_template('borrowers.html', borrowers=borrowers)  # assuming borrowers.html is your HTML file
    except Exception as e:
        print(f"Error: {str(e)}")
        return jsonify({'error': 'Internal Server Error'}), 500
    
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
        return render_template('responses.html', message='Successfully updated borrower', url = '/borrowers')
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
        return render_template('responses.html', message='Borrower deleted successfully', url = '/Borrowers')
    except Exception as ex:
        return render_template('responses.html', message='Error in borrower deletion: ' + str(ex))
    
#CRUD operations on loans
@app.route('/add_loans', methods=['POST'])
def add_bookloan():
    try:
        data = request.json
        book_id = data['book_id']
        branch_id = data['branch_id']
        borrower_id = data['borrower_id']
        date_out = data['date_out']
        date_due = data['date_due']

        conn = connect_database()
        cursor = conn.cursor()
        query = ''' INSERT INTO BookLoans (book_id, branch_id, borrower_id, date_out, date_due)
                VALUES (%s, %s, %s, %s, %s)
            '''
        cursor.execute(query, (book_id, branch_id, borrower_id, date_out, date_due))
        conn.commit()
        conn.close()
        return jsonify({'message': 'Book loan added successfully'}), 201
    except KeyError as ke:
        return jsonify({'error': f'Missing key": {ke}'}), 400
    except Error as db_err:
        return jsonify({'error': str(db_err)}), 500
    


@app.route('/add_loans', methods=['GET'])
def display_form_loans():
    # Render the HTML form located in the templates directory
    return render_template('add_loans.html')

@app.route('/book_loans', methods=['GET'])
def get_loans():
    borrower_id = request.args.get('borrower_id')
    try:
        conn = connect_database()
        cursor = conn.cursor()
        if borrower_id:
            cursor.execute('SELECT * FROM BookLoans WHERE borrower_id = %s', (borrower_id,))
        else:
            cursor.execute('SELECT * FROM BookLoans')
        book_loans = cursor.fetchall()
        conn.close()
        return render_template('book_loans.html', loans=book_loans)
    except Error as db_err:
        return jsonify({'error': str(db_err)}), 500

    
@app.route('/loans/<int:book_id>/<int:branch_id>/<int:borrower_id>', methods=['POST'])
def delete_book_loan(book_id, branch_id, borrower_id):
    
    try:
        conn = connect_database()
        cursor = conn.cursor()
        cursor.execute('DELETE FROM BookLoans WHERE book_id = %s AND branch_id = %s AND borrower_id = %s', (book_id, branch_id, borrower_id))  
        conn.commit()
        conn.close()
        if cursor.rowcount == 0:
            return jsonify({'error': 'No such book loan found'}), 404
        return render_template('responses.html', message='Loan deleted successfully', url = '/book_loans')
    except Exception as ex:
        return render_template('responses.html', message='Error in loan deletion: ' + str(ex))

@app.route('/loans/<int:book_id>/<int:branch_id>/<int:borrower_id>', methods=['POST'])
def update_book_loan(book_id, branch_id, borrower_id):
    try:
        date_out = request.form['date_out']
        date_due = request.form['date_due']
        connection = connect_database()
        cursor = connection.cursor()
        cursor.execute("Update BookLoans SET date_out = (%s), date_due = (%s) WHERE book_id = (%s) and branch_id = (%s) and borrower_id = (%s)", (date_out, date_due, book_id, branch_id, borrower_id))
        connection.commit()
        connection.close()
        return render_template('responses.html', message='Successfully updated book', url = '/loans')
    except Exception as ex:
        return render_template('responses.html', message='Error in book update: ' + str(ex), url = '/loans')

@app.route('/edit_loan/<int:book_id>/<int:branch_id>/<int:borrower_id>', methods=['GET'])
def edit_book_loan(book_id, branch_id, borrower_id):
    connection = connect_database()
    cursor = connection.cursor()
    cursor.execute('SELECT * FROM BookLoans WHERE book_id = (%s) and branch_id = (%s) and borrower_id = (%s)', (book_id, branch_id, borrower_id,))
    loan = cursor.fetchone()
    connection.close()
    if loan:
        return render_template('edit_loan.html', loan = loan)
    else:
        return 'Loan not found', 404
    

@app.route('/')
def index():
    branches = get_branches()
    return render_template('index.html', branches = branches)

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

@app.route('/book_loans')
def loans():
    loans = get_loans()
    return render_template('book_loans.html', loans = loans)


app.run(debug=True)