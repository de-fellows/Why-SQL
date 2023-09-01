# Author: Reid Moline
'''
This file is used to revert the database to my original configuration by regenerating all tables by dropping them, creating them, and refiling them using their respective code

This will delete all recorded transactions and also empty the reconcile database. Serves as a hard reset of the database.
'''
import sqlite3
from employees import create_filled_employees_table
from customers import create_filled_customers_table
from transactions import create_empty_transactions_table
from serialization import create_filled_serialization_table
from products import  create_filled_products_table
from reconcile import create_empty_reconcile_table


def drop_all(): 
    '''
    Function that drops all tables in the database bikeshop.sqlite

    Parameters: None

    Returns: None
    
    '''

    connection = sqlite3.connect('bikeshop.sqlite')
    cursor = connection.cursor()
    cursor.execute('PRAGMA foreign_keys = ON;') 

    cursor.execute("DROP TABLE IF EXISTS Reconcile;") 
    cursor.execute("DROP TABLE IF EXISTS Transactions;")
    cursor.execute("DROP TABLE IF EXISTS Serialization;")
    cursor.execute("DROP TABLE IF EXISTS Customers;")
    cursor.execute("DROP TABLE IF EXISTS Employees;")
    cursor.execute("DROP TABLE IF EXISTS Products;")


    connection.commit()
    connection.close()

drop_all()

create_empty_transactions_table()

create_empty_reconcile_table()

create_filled_employees_table()

create_filled_customers_table()

create_filled_products_table()

create_filled_serialization_table()