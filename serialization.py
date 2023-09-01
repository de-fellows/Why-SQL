# Author: Reid Moline

import sqlite3
import numpy as np
import string
import random as rd

def create_filled_serialization_table():
    '''
    Function that uses data from the bikeshop.sqlite database's table Products and creates a table called 
    Serialization used to help keep track of all serialized products (i.e bikes) in the bikeshop.sqlite database table Products.

    Parameter: None

    Returns: None

    '''

    connection = sqlite3.connect('bikeshop.sqlite')
    cursor = connection.cursor()
    cursor.execute('PRAGMA foreign_keys = ON;')

    # Used Doc String for below query to create table to help make it easy to read can use single or double quotes and type on one line this just is neater
    cursor.execute('''CREATE TABLE IF NOT EXISTS Serialization
                (Serial_Number TEXT, 
                UPC INTEGER, 
                Bike TEXT NOT NULL, 
                Sold INTEGER NOT NULL, 
                PRIMARY KEY (Serial_Number), 
                FOREIGN KEY (UPC) REFERENCES Products (UPC)
                );''')

    cursor.execute('SELECT UPC, Description, Quantity FROM Products WHERE Serialized = 1;')

    upc_bikes_and_quant = cursor.fetchall()
    upcs = []
    descriptions = []

    for i in range(len(upc_bikes_and_quant)):
        upcs += list(np.repeat(upc_bikes_and_quant[i][0], upc_bikes_and_quant[i][2]))
        descriptions += list(np.repeat(upc_bikes_and_quant[i][1], upc_bikes_and_quant[i][2]))

    serial_nums = []
    uppercase_letters = list(string.ascii_uppercase)
    nums = list('0123456789')


    for i in range(len(descriptions)):

        serial_number = 'WTU' + ''.join(rd.choices(nums, k= 3)) + rd.choice(uppercase_letters) + ''.join(rd.choices(nums, k= 2)) + rd.choice(uppercase_letters) + rd.choice(nums) + rd.choice(uppercase_letters)
        while serial_number in serial_nums:
            serial_number = 'WTU' + ''.join(rd.choices(nums, k= 3)) + rd.choice(uppercase_letters) + ''.join(rd.choices(nums, k= 2)) + rd.choice(uppercase_letters) + rd.choice(nums) + rd.choice(uppercase_letters)
        serial_nums.append(serial_number)

    sold = [False] * len(serial_nums)

    for i in range(len(serial_nums)):
        cursor.execute("INSERT INTO Serialization VALUES(?,?,?,?);", (serial_nums[i], str(upcs[i]), descriptions[i], sold[i]))  # UPC had to be typecasted as a string to meet the Foreign Key Constraint

    connection.commit()
    connection.close()

# if this file is run it'll go through the serialization table and execute some queries to display some useful business data that can be extracted

if __name__ == "__main__":


    conn = sqlite3.connect('bikeshop.sqlite')
    cur = conn.cursor()
    cur.execute("PRAGMA foreign_keys = ON")