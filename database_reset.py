import sqlite3
from customers import create_filled_customers_table
from transactions import create_empty_transactions_table
from serialization import create_filled_serialization_table

connection = sqlite3.connect('bikeshop.sqlite')

cursor = connection.cursor()
cursor.execute('PRAGMA foreign_keys = OFF;')    # In this case I turn off the foreign key constraint so I can drop all tables 