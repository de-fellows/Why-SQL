import sqlite3
import names
import random as rd

connection = sqlite3.connect('introduction.sqlite') # connects us to a file with the name introduction.sqlite if already created or creates a new file called introduction.sqlite if there was no file found

cursor = connection.cursor()    # Creates a cursor which allows us to execute queries

# Remove the below code from docstrings to change the grades table to drop the grades table given and get totally different names and gpas
'''
cursor.execute("DROP TABLE grades")

cursor.execute("CREATE TABLE grades(student_id primary key, first_name text, last_name text, gpa real)") # Creats a table with four columns, the student_id which is the unique element hence the primary key, the first name, last name, and a gpa

NUM_STUDENTS = 20

for i in range(NUM_STUDENTS):
    cursor.execute("INSERT INTO grades VALUES(?,?,?,?)", (i, names.get_first_name(), names.get_last_name(), round(rd.uniform(2.0, 4.0), 2))) # Unlike python print statements, to pass in values the placeholder is a question mark and all values must be contained in a tuple
'''
cursor.execute("SELECT * FROM grades WHERE gpa LIKE '%5'") #Finding rows where last digit of gpa is 5

students_with_gpas_ending_in_five = cursor.fetchall()   # gets a list of tuples of each student with gpa ending in 5 as per above query

for student in students_with_gpas_ending_in_five:
    print(student)

# TODO: Practice some basic SQL queries below and see what you can do!

connection.commit() # required to save any changes to the database file
connection.close() # closes the connnection much like closing a file to free up space in RAM