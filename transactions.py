# Author: Reid Moline

import sqlite3
from datetime import date
import random as rd


def create_empty_transactions_table():

    '''
    Function that connects to the bikeshop.sqlite database and creates a table called transactions used to keep record of all sales for the store
    
    Parameters: None

    Returns: None
    '''
    conn = sqlite3.connect('bikeshop.sqlite')

    cur = conn.cursor()
    cur.execute('PRAGMA foreign_keys = ON;')
        
    cur.execute("""CREATE TABLE IF NOT EXISTS Transactions
                (Transaction_Number INT NOT NULL,
                customer_id INTEGER NOT NULL,
                Item TEXT NOT NULL,
                UPC INTEGER NOT NULL,
                Item_Cost REAL,
                Serial_Number TEXT DEFAULT NULL,
                Salesperson_ID INT,
                Payment_Type TEXT DEFAULT NULL,
                Date TEXT,
                FOREIGN KEY (customer_id) REFERENCES Customers (customer_id),
                FOREIGN KEY (UPC) REFERENCES Products (UPC)
                )""")


if __name__ == "__main__":


    connection = sqlite3.connect('bikeshop.sqlite')

    cursor = connection.cursor()
    cursor.execute('PRAGMA foreign_keys = ON;')


    line = '_' * 40 + '\n'

    #Below line if removed from docstrings will delete all transaction history

    '''
    cursor.execute("""CREATE TABLE IF NOT EXISTS Transactions
                (Transaction_Number INT NOT NULL,
                customer_id INTEGER NOT NULL,
                Item TEXT NOT NULL,
                UPC INTEGER NOT NULL,
                Item_Cost REAL,
                Serial_Number TEXT DEFAULT NULL,
                Salesperson_ID INT,
                Payment_Type TEXT DEFAULT NULL,
                Date TEXT,
                FOREIGN KEY (customer_id) REFERENCES Customers (customer_id),
                FOREIGN KEY (UPC) REFERENCES Products (UPC)
                )""")
    '''

    while True:
        
        print(line)

        employee_making_sale = input('Please Enter your Employee ID: ')
        attempt = 1

        cursor.execute("SELECT * FROM employees WHERE employee_code = ?", (employee_making_sale,))

        employee_details = cursor.fetchall()

        while employee_details == [] and attempt < 4:           # Creating a basic password protection system like would be seen in a retail setting
            print(line)
            print("Invalid Employee Code Please Try Again")
            print(f'You have {3 - attempt} attempt(s) left')

            employee_making_sale = int(input('Please Enter your Employee ID: '))

            attempt += 1

            cursor.execute("SELECT * FROM employees WHERE employee_code = ?", (employee_making_sale,))

            employee_details = cursor.fetchall()

        if employee_details == []:  # Ends program if employee doesn't input correct credentials in 3 tries
            break

        print(line)

        print("Please select what to search for the customer using the numbered options below or enter 0 to continue with a Guest Customer or 4 to quit\n")
        print("1) Phone Number")
        print("2) Customer ID")     # Primary Key so UNIQUE
        print("3) Create New Customer")

        print(line)


        cursor.execute("SELECT customer_id, customer_phone from Customers;")

        all_customer_ids_and_phones = cursor.fetchall()

        list_all_customer_ids = [all_customer_ids_and_phones[i][0] for i in range(len(all_customer_ids_and_phones))]
        list_all_customer_phones = [all_customer_ids_and_phones[i][1] for i in range(len(all_customer_ids_and_phones))]


        option = int(input("Please Enter a numbered option from above: "))

        while option not in range(5):
            print(line)

            print("Please select an option listed above.")
            option = int(input("Please Enter a numbered option from above: "))
        
        print(line)

        if option == 4:
            break

        elif option == 3:
            new_first_name = input("First Name: ")
            new_last_name = input("Last Name: ")
            new_email = input("Email (not required suggested): ")
            new_phone = input("Phone Number (required): ")

            customer_id = rd.randint(100000, 999999)

            while customer_id in list_all_customer_ids:
                customer_id = rd.randint(100000, 999999)

            while new_phone in list_all_customer_phones:
                print("Phone number already in use. Enter New Number")
                new_phone = input("Phone Number (required): ")

            cursor.execute("INSERT INTO Customers VALUES(?,?,?,?,?,?);", (customer_id, new_first_name, new_last_name, new_email, new_phone, employee_making_sale))


        elif option == 0:
            customer_id = str(0)    # Must be type casted to meet foreign key constraint

        elif option == 1:

            cust_phone = input("Please enter the phone number: ")

            cursor.execute("SELECT * FROM Customers WHERE customer_phone = ?", (cust_phone,))   

            phone_search_results = cursor.fetchall()

            while len(phone_search_results) != 1 and cust_phone != '':
                print(line)
                if len(phone_search_results) == 0:
                    print("No Results try again or press ENTER to quit")

                elif len(phone_search_results) > 1:                                 # Allows for revert to search by customer ID if family using same phone number for account
                    print("Too many results Please try searching by Customer ID")
                    option = 2
                    break

                cust_phone = input("Please enter the phone number: ")

                cursor.execute("SELECT * FROM Customers WHERE customer_phone = ?", (cust_phone,)) 

                phone_search_results = cursor.fetchall()

            if cust_phone == '':    # Gives option to quit
                break

            customer_id = phone_search_results[0][0]    # Once refined to one account we can grab the customer ID


        if option == 2:

            customer_id = input("Please enter the Customer ID: ")
            
            cursor.execute("SELECT * FROM Customers WHERE customer_id = ?", (customer_id,))   

            id_search_results = cursor.fetchall()

            while len(id_search_results) == 0 and customer_id != '': 

                print(line)

                if len(id_search_results) == 0:
                    print("No Results try again or press ENTER to quit")

                customer_id = input("Please enter the Customer ID: ")

                cursor.execute("SELECT * FROM Customers WHERE customer_id  = ?", (customer_id,)) 

                id_search_results = cursor.fetchall()


            if customer_id == '':    # Gives option to quit
                break

            customer_id = id_search_results[0][0]    # Once refined to one account we can grab the customer ID



        #Now Dealing with the Sale itself

        cursor.execute("SELECT Transaction_Number from Transactions;")
        transaction_nums = cursor.fetchall()
        list_of_transaction_numbers = [transaction_nums[i][0] for i in range(len(transaction_nums))]

        transaction_number = rd.randint(1000000, 9999999)

        while transaction_number in list_of_transaction_numbers:
            transaction_number = rd.randint(1000000, 9999999)       # Ensures the uniqueness of the generated transaction ID (it is a primary key and needs to be unique)
        
        date_of_sale = date.today()

        print(line)

        print("To stop scanning items press ENTER without scanning anything")

        scanning = True

        cursor.execute("SELECT UPC FROM Products;")     # Creates a list of all product UPC to cross reference scanned item
        all_upcs = cursor.fetchall()
        list_all_upcs = [all_upcs[i][0] for i in range(len(all_upcs))]
        

        while scanning:
            upc = input("Scan: ")


            if upc == '':   # Way to stop scanning through items
                break

            upc = int(upc)

            if upc not in list_all_upcs:
                print("UPC Not Found. Item not in inventory")
                continue

            elif upc in list_all_upcs:

                cursor.execute("SELECT * FROM Products WHERE UPC = ?", (upc,))

                all_info = cursor.fetchall()[0]


                description = all_info[1]
                quantity = all_info[2]
                price = all_info[3]
                serialized = all_info[5]

                new_quantity = int(quantity) - 1 # Makes quantity one less in inventory

                cursor.execute("UPDATE Products SET Quantity = ? WHERE UPC = ?", (new_quantity, upc)) # Makes quantity one less in inventory

                if new_quantity < 0 and serialized:     # if a bike is scanned through and not in inventory this warrants a manager because the bike can't be sold if not in inventory. Too high ticket an item to sell without being in the systems inventory
                    print("Bike not in Inventory. Manager Assistance Needed")
                    print("Bike has not been added to transaction until manager reconciles issue")
                    print(line)
                    continue

                elif new_quantity < 0 and not serialized:    # Issue with inventory that needs to be reconciled. item can still be sold if not serialized. Sometimes things get misplaced and/or stolen and inventory is wrong

                    cursor.execute("SELECT Issue_ID FROM Reconcile;")
                    issue_ids = cursor.fetchall()
                    list_issue_ids = [issue_ids[i][0] for i in range(len(issue_ids))]

                    new_issue_id = rd.randint(1000000, 9999999) # Creates an ID to reference the issue by

                    while new_issue_id in list_issue_ids:
                        new_issue_id = rd.randint(1000000, 9999999) # Ensures uniqueness of issue ID
                    

                    cursor.execute("INSERT INTO Reconcile VALUES(?,?,?,?)", (new_issue_id, upc, date_of_sale, 0))     # Creates new inventory issue to be reconciled
                    print('Item sold but Invnetory Issue needs to be Reconciled')
                    
                if serialized:

                    serial_number = input("Please Enter the Serial Number of the bike exactly as seen: ")

                    cursor.execute("SELECT Sold FROM Serialization WHERE Serial_Number = ? AND UPC = ?;", (serial_number, upc))

                    sold_status = cursor.fetchall()  # Grabs list that should be one of three things [], [(1,)], [(0,)] 

                    if sold_status == []:
                        print("Serial Number not in System Please Scan UPC and try again")

                    elif sold_status[0][0] == 1:
                        print("Bike already registered as sold. Bike can not be resold until manager reconciles this issue ")

                    elif sold_status[0][0] == 0:

                        cursor.execute("INSERT INTO Transactions VALUES(?,?,?,?,?,?,?,?,?)", (transaction_number, customer_id, description, upc, price, serial_number, employee_making_sale, None, date_of_sale ))      # Payment detail will be updated when scanning complete and total is "paid"
                        cursor.execute("UPDATE Serialization SET Sold = 1 WHERE Serial_Number = ?;", (serial_number,))
                        print("Bike Added")
                        print(line)
                        
                elif not serialized:

                    serial_number = None

                    cursor.execute("INSERT INTO Transactions VALUES(?,?,?,?,?,?,?,?,?)", (transaction_number, customer_id, description, upc, price, serial_number, employee_making_sale, None, date_of_sale ))      # Payment detail will be updated when scanning complete and total is "paid"
                    
                    print("Item Added")
                    print(line)
            

        cursor.execute("SELECT SUM(Item_Cost) FROM Transactions WHERE Transaction_Number = ?;", (transaction_number,))

        subtotal = cursor.fetchone()[0] #Accessing first index of single tuple (fetchone)

        if subtotal == None:
            print("No sale was complete because no items were scanned")

        else:

            total = subtotal * 1.05 # Adding Tax

            print(line)

            print(f"Subtotal:   {subtotal}")
            print(f"Total:      {total:.2f}")

            print(line)

            print("Please enter in total in credit/debit machine")

            payment_types = ['MC', 'VISA', 'AMEX', 'DEBIT']   # Standard Types of Payment (Cashless because that adds another element of returning change)

            payment = input("Payment Type (VISA, MC, AMEX, DEBIT): ").upper()
                
            while payment not in payment_types:
                print("Please enter proper paymeny type.")
                payment = input("Payment Type (VISA, MC, AMEX, DEBIT): ").upper()

            cursor.execute("UPDATE Transactions SET Payment_Type = ? WHERE Transaction_Number = ?", (payment, transaction_number))

            print(line)

            print("Sale Complete")

        break

    connection.commit()
    connection.close()