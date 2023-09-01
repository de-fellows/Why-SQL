# Author: Reid Moline

import sqlite3
import names
import random as rd


line = '_' * 30 + '\n'

connection = sqlite3.connect('introduction.sqlite') # connects us to a file with the name introduction.sqlite if already created or creates a new file called introduction.sqlite if there was no file found

cursor = connection.cursor()    # Creates a cursor which allows us to execute queries

# Remove the below code from docstrings to change the grades table to drop the grades table given and get totally different names and gpas

'''
cursor.execute("DROP TABLE IF EXISTS grades")

cursor.execute("""CREATE TABLE IF NOT EXISTS grades
                    (student_id INTEGER,
                    first_name TEXT, 
                    last_name TEXT, 
                    gpa REAL,
                    PRIMARY KEY (student_id)
                    )""") 
# Above Query Creates a table with four columns, the student_id which is the unique element hence the primary key, the first name, last name, and a gpa

NUM_STUDENTS = 20

for i in range(NUM_STUDENTS):
    cursor.execute("INSERT INTO grades VALUES(?,?,?,?)", (i, names.get_first_name(), names.get_last_name(), round(rd.uniform(2.0, 4.0), 2))) # Unlike python print statements, to pass in values the placeholder is a question mark and all values must be contained in a tuple
'''
    

cursor.execute("SELECT * FROM grades WHERE gpa LIKE '2%';") #getting all columns (The * character) from rows where GPA starts with 2

students_with_gpas_in_the_2_range = cursor.fetchall()   # gets a list of tuples of each student with gpa ending in 5 as per above query

print(line)
print('All GPAS Starting with 2\n')

for student in students_with_gpas_in_the_2_range:
    print(student)
print(line)

cursor.execute("SELECT avg(gpa) from grades;")  # Getting the average gpa from the table

print('Average GPA\n')
print(cursor.fetchone())    # Using fetchone() as I only want the first tuple hence we know only one value (the average gpa) will be found
print(line)                 # If I wanted just the value of the average gpa (not the tuple) I would do cursor.fetchone()[0]


cursor.execute("SELECT student_id FROM grades;")

list_id_tuples = cursor.fetchall()

list_ids = [id_tuple[0] for id_tuple in list_id_tuples]

new_id = rd.randint(0,1000)

while new_id in list_ids:
    new_id = rd.randint(0,1000)
list_ids.append(new_id)

cursor.execute("INSERT INTO grades VALUES(?,?,?,?);", (new_id, names.get_first_name(), names.get_last_name(), round(rd.uniform(2.0, 4.0), 2))) # Unlike python print statements, to pass in values the placeholder is a question mark and all values must be contained in a tuple

cursor.execute("SELECT last_name, first_name FROM grades WHERE student_id = ?", (new_id,)) # Notice how even though I only have one variable to pass into the query I still need to put it in a tuple

first_and_last_name = cursor.fetchall()

print("Last Name, First Name of newly inserted student\n")
print(first_and_last_name)

print(line)

cursor.execute("SELECT * FROM grades LIMIT 2;") # Get all columns from grades for only the first two entries

first_two = cursor.fetchall()

for val in first_two:
    print(val)

print(line)

# TODO: Practice some basic SQL queries below and see what you can do!
# Try using conditions and logical operator AND and OR which are very similar to python
# Try to Order by decreasing GPA to find who the top dog in the class was

cursor.execute("SELECT * FROM grades WHERE gpa LIKE '%3%' ORDER BY student_id")

students_with_a_3_anywhere = cursor.fetchall()

for line in students_with_a_3_anywhere:
    print(line)


connection.commit() # required to save any changes to the database file
connection.close() # closes the connnection much like closing a file to free up space