# Author: Reid Moline

import sqlite3
import names
import random as rd


def create_filled_employees_table():
    '''
    Function that connects to the bikeshop.sqlite database and creates and fills a table called Employees with employee details

    Parameters: None

    Returns: None
    '''
        
    connection = sqlite3.connect('bikeshop.sqlite')     # Connection to the db is created

    cursor = connection.cursor()                    # Cursor is created so we can execute queries
    cursor.execute('PRAGMA foreign_keys = ON;')     # Ensures that foreign key constraints are enabled for the database

    # Used Doc String for below query to create table to help make it easy to read can use single or double quotes and type on one line this just is neater
    cursor.execute('''CREATE TABLE IF NOT EXISTS Employees
                (employee_code INTEGER PRIMARY KEY,
                first_name TEXT, 
                last_name TEXT, 
                email TEXT, 
                phone INTEGER, 
                department TEXT);''')

    cursor.execute('INSERT INTO Employees VALUES(?,?,?,?,?,?)', (1234, 'Manager', 'Manager', 'manager@example.ca', 1234567890,  'Manager'))  # Creates an profile for the manager

    NUM_EMPLOYEES = 15      # Chosen constant so we generate 15 employees

    ids = []

    for i in range(NUM_EMPLOYEES):

        roles = ['Sales', 'Service']    # Gives random employee one of two department roles Sales of Service
        department = rd.choice(roles)

        id = rd.randint(1000, 9999)     # Generates random 4 digit ID

        while id in ids:                # Ensures unique id as it is the Primary Key
            id = rd.randint(1000,9999)
        ids.append(id)
        
        first_name = names.get_first_name() # generates a random first name for the user

        surname = names.get_last_name()    # generates a random last name for the user

        email = first_name + '.' + surname + '@' + 'example.ca' # gives placeholder email for employee

        phone_num = rd.randint(100000000, 999999999) # generates a random 10 digit phone number for the user

        cursor.execute('INSERT INTO Employees VALUES(?,?,?,?,?,?);',(id, first_name, surname, email, phone_num, department))    # Adds employee data to table of employees

    connection.commit() # commits changes to database
    connection.close()  # closes connection

if __name__ == "main":

    pass
#execute some queries to show the usefulness of sql for business logic