import sqlite3
import names
import random as rd

connection = sqlite3.connect('bikeshop.sqlite')

cursor = connection.cursor()

cursor.execute('CREATE TABLE Employees(employee_id INTEGER primary key, first_name TEXT, last_name TEXT, email TEXT, phone INTEGER)')

NUM_EMPLOYEES = 10

for i in range(NUM_EMPLOYEES):

    id = i

    first_name = names.get_first_name() #generates a random first name for the user

    surname = names.get_last_name()    #generates a random last name for the user

    email = first_name + '.' + surname + '@' + 'calgarybikeshop.ca'

    phone_num = rd.randint(100000000, 999999999) #generates a random 10 digit phone number for the user

    cursor.execute('INSERT INTO Employees VALUES(?,?,?,?,?)',(id, first_name, surname, email, phone_num))

connection.commit()
connection.close()