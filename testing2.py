import mysql.connector
from tkinter import *
from tkinter.ttk import Combobox

# Create the main application window or any parent widget as needed.
root = Tk()
root.geometry("400x300")

# Connect to the database
try:
    connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="Nightcore_1134372019!",  # replace with your actual password
        database="attendnow"
    )

    cursor = connection.cursor()
    cursor.execute("SELECT DISTINCT teacher_name FROM timetable")  # Fetch unique teacher names
    teacher_names = [row[0] for row in cursor.fetchall()]  # Extract teacher names into a list

except mysql.connector.Error as err:
    print(f"Error: {err}")
    teacher_names = []  # Empty list if there's an error

finally:
    if connection.is_connected():
        cursor.close()
        connection.close()

# Initialize the Combobox with the teacher names
teacher_var = StringVar()
teacher_combobox = Combobox(root, textvariable=teacher_var)
teacher_combobox['values'] = teacher_names  # Populate with fetched teacher names
teacher_combobox.place(x=80, y=100, width=150, height=30)
teacher_combobox.set("Select Teacher")  # Default text

root.mainloop()
