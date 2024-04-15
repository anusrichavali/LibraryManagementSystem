import mysql.connector
from mysql.connector import Error
from flask import Flask
from flask import jsonify
from flask import request

app = Flask(__name__)

def connect_database():
    try:
        db = mysql.connector.connect(host='localhost', user='admin', password='dbproject_6868!?', database='LibraryManagementSystem')
        if db.is_connected():
            print("The program has successfully connected to the LibraryManagementaSystem database.")
            return db
    except Error as er:
        print(f"There is an error in the connection process. {er}")
        
app.run()