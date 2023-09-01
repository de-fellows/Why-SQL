# Author: Reid Moline

import sqlite3


def create_empty_reconcile_table():

    '''
    Function that connects to the database bikeshop.sqlite and creates an empty table Reconcile used to track inventory issues that need to be addressed

    Parameters: None

    Returns: None
    '''

    connection = sqlite3.connect('bikeshop.sqlite')     # Creates a connection to the database
    cursor = connection.cursor()
    cursor.execute("PRAGMA foreign_keys = ON")        

    cursor.execute("""CREATE TABLE IF NOT EXISTS Reconcile 
                (Issue_ID INT,
                UPC INT, 
                Date TEXT,
                Fixed INT DEFAULT '0',
                PRIMARY KEY (Issue_ID),
                FOREIGN KEY (UPC) REFERENCES Products (UPC)
                )""")
    


if __name__ == "__main__":
    # Show how a manager can check for issues to be reconciled and how if there is one how they can go into products and change the quantity to reflect 0
    pass