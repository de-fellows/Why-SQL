import sqlite3
import random as rd
import names

NUM_CUSTOMERS = 48

connection = sqlite3.connect('bikeshop.sqlite')

cursor = connection.cursor()

cursor.execute("DROP TABLE Customers")
cursor.execute('CREATE TABLE Customers(customer_id INTEGER, customer_first_name TEXT, customer_last_name TEXT, customer_email TEXT, customer_phone INTEGER, PRIMARY KEY (customer_id))')

cursor.execute("INSERT INTO Customers VALUES(?,?,?,?,?)", (0, None, None, None, None))

potential_domains = ['gmail.com', 'hotmail.com', 'telus.net', 'shaw.ca', 'outlook.com', 'yahoo.com', 'live.ca', 'ucalgary.ca', 'icloud.com'] #list of random domains to be used to generate random emails

for i in range(NUM_CUSTOMERS):
    customer_id = i + 1

    rand_first_name = names.get_first_name() #generates a random first name for the user

    rand_surname = names.get_last_name()    #generates a random last name for the user

    rand_email = rand_first_name + '.' + rand_surname + '@' + rd.choice(potential_domains)

    rand_phone_num = rd.randint(100000000, 999999999) #generates a random 10 digit phone number for the user

    cursor.execute('INSERT INTO Customers VALUES(?,?,?,?,?)',(customer_id, rand_first_name, rand_surname, rand_email, rand_phone_num))

cursor.execute('SELECT max(customer_id) FROM Customers')
largest_customer_id = cursor.fetchone()[0]  #accesses first element of tuple returned(48,) which is 48

cursor.execute('INSERT INTO Customers VALUES(?,?,?,?,?)', (largest_customer_id + 1, 'Reid','Moline', None, 4032737373))

connection.commit()
connection.close()