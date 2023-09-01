# Author: Reid Moline

import sqlite3
import random as rd
import names

def create_filled_customers_table():
    
    '''
    Function that connects to the database bikeshop.sqlite and creates a filled out table for customers including randomly generated information for the customers
    that is in line with what a company may store for a customer account in a retail setting

    Parameters: None

    Returns: None
    '''

    NUM_CUSTOMERS = 48  # Chosen Arbitrary Number of Customers to generate

    connection = sqlite3.connect('bikeshop.sqlite')    # Creates connection to database

    cursor = connection.cursor()    # Creates cursor to execute queries 
    cursor.execute('PRAGMA foreign_keys = ON;')

    # Used Doc String for below query to create table to help make it easy to read can use single or double quotes and type on one line this just is neater
    cursor.execute('''CREATE TABLE IF NOT EXISTS Customers
                (customer_id INTEGER NOT NULL,
                customer_first_name TEXT ,
                customer_last_name TEXT,
                customer_email TEXT, 
                customer_phone INTEGER, 
                created_by INTEGER,
                PRIMARY KEY (customer_id)
                FOREIGN KEY (created_by) REFERENCES Employees (employee_code)
                );''')

    cursor.execute("INSERT INTO Customers VALUES(?,?,?,?,?,?);", (0, 'Guest', 'Customer', None, None, 1234))     # Creates Guest Customer Profile

    potential_domains = ['gmail.com', 'hotmail.com', 'telus.net', 'shaw.ca', 'outlook.com', 'yahoo.com', 'live.ca', 'ucalgary.ca', 'icloud.com'] # List of random domains to be used to generate random emails

    ids = []

    cursor.execute("SELECT employee_code FROM Employees WHERE department = 'Sales';")
    sales_emp_ids = cursor.fetchall()
    list_sales_employee_ids = [sales_emp_ids[i][0] for i in range(len(sales_emp_ids))]

    for i in range(NUM_CUSTOMERS):
        customer_id = rd.randint(100000,999999) # generates random 6 digit customer id
        
        while customer_id in ids:                       # Ensrures generated id is unique as it is the primary key
            customer_id = rd.randint(100000,999999)
        
        ids.append(customer_id)

        rand_first_name = names.get_first_name() # generates a random first name for the user

        rand_surname = names.get_last_name()    # generates a random last name for the user

        rand_email = rand_first_name + '.' + rand_surname + '@' + rd.choice(potential_domains)  # generates fake email to mimic a customers email

        rand_phone_num = rd.randint(100000000, 999999999) # generates a random 10 digit phone number for the user

        rand_employee = rd.choice(list_sales_employee_ids)

        cursor.execute('INSERT INTO Customers VALUES(?,?,?,?,?,?);',(customer_id, rand_first_name, rand_surname, rand_email, rand_phone_num, rand_employee))

    cursor.execute('SELECT max(customer_id) FROM Customers;')
    largest_customer_id = cursor.fetchone()[0]  # accesses first element of tuple returned (48,) which is 48

    cursor.execute('INSERT INTO Customers VALUES(?,?,?,?,?,?);', (largest_customer_id + 1, 'Reid','Moline', None, 4032737373, rand_employee))    # Before you try to call this number note it is for Pizza 73

    connection.commit() # Commits changes to database  
    connection.close()  # Closes connection


if __name__ == "__main__": 

    conn = sqlite3.connect('bikeshop.sqlite')
    cur = conn.cursor()
    cur.execute("PRAGMA foreign_keys = ON")

    cur.execute("SELECT employee_code FROM Employees;")

    all_emp_ids = cur.fetchall()    # list of one element tuples

    randomly_selected_emp_id = all_emp_ids[rd.randrange(0,len(all_emp_ids))][0] # Grabs one employee id from the employee table randomly
    
    print(f"Employee ID: {randomly_selected_emp_id}")
    print('_' * 20 + '\n')

    cur.execute("SELECT COUNT(*) FROM Customers WHERE created_by = ?", (randomly_selected_emp_id,))

    total_profiles_created_by_employee = cur.fetchone()[0]

    print(f"Total Profiles Created: {total_profiles_created_by_employee}")

    cur.execute("SELECT COUNT(*) FROM Customers WHERE customer_email IS NULL AND created_by = ?;", (randomly_selected_emp_id,)) # NOTE the IS NULL query to check where no email

    profiles_created_by_employee_with_no_email = cur.fetchone()[0]

    print(f"Number of profiles created with no email: {profiles_created_by_employee_with_no_email}")

    if total_profiles_created_by_employee == 0:             # In case an employee hasn't created any profiles
        print("No Email Capture Percentage can be given")

    else:
        email_capture_percentage = ((total_profiles_created_by_employee - profiles_created_by_employee_with_no_email) / total_profiles_created_by_employee) * 100

        print(f"Employee Email Capture: {email_capture_percentage:.2f}%")   # Important for the business to track where how often employees get the customers email

    # For you TODO Try adding more customers to the database noting you'd need to first find some employee ids to insert given the foreign key constraint.

    # For you TODO Try adding customers without an email and check how the email capture percentage changes with this

    conn.commit()
    conn.close()