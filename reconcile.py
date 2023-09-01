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

    conn = sqlite3.connect('bikeshop.sqlite')
    cur = conn.cursor()
    cur.execute("PRAGMA foreign_keys = ON")


    cur.execute("SELECT UPC FROM Reconcile WHERE Fixed = 0;")

    unfixed_inventory_issues = cur.fetchall()

    if len(unfixed_inventory_issues) != 0:

        print("UPC's with negative quantity showing")
        print('_' * 20 + '\n')
        
        for i in range(len(unfixed_inventory_issues)):

            print(unfixed_inventory_issues[i][0])   # Prints out each upc from

    # For you TODO Given this list of issues try and create queries to fix the quantity to be 0 and don't forget to close the issue

    conn.commit()
    conn.close()