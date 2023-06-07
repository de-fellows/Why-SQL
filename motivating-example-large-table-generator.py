import pandas as pd
import datetime as dt
import random as rd

NUM_SALES = 20  # Constant to show how many transaction occour

transaction_numbers = [i+1 for i in range(NUM_SALES)]

potential_payment_types = ['MC', 'Visa', 'AMEX', 'Debit', 'Cash']   # Standard Types of Payment

payment_types = rd.choices(potential_payment_types, k= NUM_SALES)

time_of_purchase = [dt.datetime.strptime('05/15/2023 10:00', "%m/%d/%Y %H:%M") + dt.timedelta(minutes = 10 * i) for i in range(NUM_SALES)]  

employees_on_staff = ['Reid Moline', 'John Doe', 'Bruce Wayne', 'Peter Parker', 'Clarke Kent']  # Hypothetical Employees on Staff

employee_in_charge_of_sale = rd.choices(employees_on_staff, k= NUM_SALES)

customers = ['Micheal Jordan', 'Wayne Gretzky', 'Tiger Woods', 'Willie Mays', 'Tom Brady'] # Hypothetical Customers

purchasing_customer = rd.choices(customers, k= NUM_SALES)

items = [['2023 Kona Process 153', 'B1', 4299.99, 2499.97], ['2022 Trek Checkpoint AL5', 'B2', 2899.99, 1349.97], ['2023 Commencal Supreme DH', 'B3', 5299.99, 2298.97], ['2023 Specialized Enduro Comp', 'B4', 7199.99, 2242.97], ['2023 Specialized Turbo Levo SL', 'B5', 11599.99, 8000.97], ['2023 Rocky Mountain Growler 40', 'B6', 1989.99, 1299.97]]

items_sold = rd.choices(items, k = NUM_SALES)
item_descriptions = [items_sold[i][0] for i in range(NUM_SALES)]
item_codes = [items_sold[i][1] for i in range(NUM_SALES)]
item_retail = [items_sold[i][2] for i in range(NUM_SALES)]
item_wholesale = [items_sold[i][3] for i in range(NUM_SALES)]

df_dict = {'Transaction Number' : transaction_numbers, 'Time of Purchase': time_of_purchase, 'Sold By': employee_in_charge_of_sale, 'Item Code' : item_codes, 'Item Description' : item_descriptions, 'MSRP (CAD)' : item_retail, 'Cost (CAD)' : item_wholesale, 'Customer': purchasing_customer, 'Payment Type': payment_types}

df = pd.DataFrame(df_dict)

df.to_csv('motivating-example-large-table.txt', index=False)