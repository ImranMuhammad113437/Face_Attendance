from tkinter import *
from tkinter import ttk
from PIL import Image, ImageTk
import os
import admit_interface  # Import admit_interface for the back button functionality
import mysql.connector  # Import MySQL Connector
from tkinter import messagebox


class Teacher_Interface:
    def __init__(self, root, username):
        self.root = root
        self.username = username  # Storing username for future use
        self.root.geometry("1024x590")  # Adjusted window size for side-by-side layout
        self.root.title("AttendNow - Curriculum")

        self.var_department = StringVar()
        self.var_course = StringVar()

        # Connect to the database
        self.conn = self.connect_to_db()

        # Background Image
        background_img_main = Image.open(r"Image\Background.png")
        background_img_main = background_img_main.resize((1200, 600), Image.Resampling.LANCZOS)
        self.photo_background_img_main = ImageTk.PhotoImage(background_img_main)
        background_img_main_position = Label(self.root, image=self.photo_background_img_main)
        background_img_main_position.place(x=0, y=0, width=1200, height=600)

        # LogoTitle Image
        left_title = Image.open(r"Image\LogoTitle_Left Top.png")
        self.photoleft_title = ImageTk.PhotoImage(left_title)
        left_title_position = Label(self.root, image=self.photoleft_title)
        left_title_position.place(x=0, y=0, width=163, height=60)

        # Title Bar
        title_frame = Frame(background_img_main_position, bd=2, bg="orange")
        title_frame.place(x=300, y=5, width=450, height=50)
        title_label = Label(title_frame, text="Teacher Management Table", bg="orange", fg="white", font=("New Time Roman", 20, "bold"))
        title_label.place(x=2, y=2, width=445, height=40)

        # Back Button
        back_button = Button(self.root, text="Back", command=self.go_back, bg="red", fg="white", font=("Arial", 12, "bold"))
        back_button.place(x=175, y=15, width=80, height=30)

        # Display username on the top right corner
        self.username_label = Label(self.root, text=f"Logged in as: {self.username}", bg="orange", fg="white", font=("Arial", 12))
        self.username_label.place(x=800, y=15)

        # Main Frame (Split into left and right)
        main_frame = Frame(self.root, bd=2, bg="orange")
        main_frame.place(x=20,y=70,width=984,height=500)

        # Left Frame for Curriculum Editing
        left_frame = LabelFrame(main_frame, bd=2, relief=RIDGE, text="Curriculum Editing", bg="white")
        left_frame.place(x=10,y=10,width=477,height=470)  # Left side (form) with height 600

        # Input fields for Teacher Registration inside the Curriculum Editing section
        # Input fields for Teacher Registration inside the Curriculum Editing section
        first_name_label = Label(left_frame, text="First Name:", bg="white", fg="black", font=("Arial", 10))
        first_name_label.grid(row=0, column=0, padx=10, pady=10, sticky=W)
        self.first_name_input = ttk.Entry(left_frame, width=40)
        self.first_name_input.grid(row=0, column=1, padx=10, pady=10)

        last_name_label = Label(left_frame, text="Last Name:", bg="white", fg="black", font=("Arial", 10))
        last_name_label.grid(row=1, column=0, padx=10, pady=10, sticky=W)
        self.last_name_input = ttk.Entry(left_frame, width=40)
        self.last_name_input.grid(row=1, column=1, padx=10, pady=10)

        email_label = Label(left_frame, text="Email Address:", bg="white", fg="black", font=("Arial", 10))
        email_label.grid(row=2, column=0, padx=10, pady=10, sticky=W)
        self.email_input = ttk.Entry(left_frame, width=40)
        self.email_input.grid(row=2, column=1, padx=10, pady=10)

        password_label = Label(left_frame, text="Password:", bg="white", fg="black", font=("Arial", 10))
        password_label.grid(row=3, column=0, padx=10, pady=10, sticky=W)
        self.password_input = ttk.Entry(left_frame, show="*", width=40)  # Hides the password input
        self.password_input.grid(row=3, column=1, padx=10, pady=10)

        # Dropdown menu for Department
        department_label = Label(left_frame, text="Department:", bg="white", fg="black", font=("Arial", 10))
        department_label.grid(row=4, column=0, padx=10, pady=10, sticky=W)


        # Creating a Combobox for the Department
        self.department_input = ttk.Combobox(left_frame, values=self.fetch_departments(), width=38)
        self.department_input.grid(row=4, column=1, padx=10, pady=10)

        # Set a default value (optional)
        if departments:  # Check if the list is not empty
            self.department_input.current(0)  # Sets the default to the first department

        course_label = Label(left_frame, text="Course:", bg="white", fg="black", font=("Arial", 10))
        course_label.grid(row=5, column=0, padx=10, pady=10, sticky=W)
        self.course_input = ttk.Entry(left_frame, width=40)
        self.course_input.grid(row=5, column=1, padx=10, pady=10)

        # Buttons for Add, Update, Delete, and Reset inside the Curriculum Editing section
        button_width = 22

        # Adjusted row numbers for button placement below input fields
        add_button = Button(left_frame, text="Add", bg="orange", fg="white", width=button_width, command=self.add_data)
        add_button.grid(row=6, column=0, padx=10, pady=10)

        delete_button = Button(left_frame, text="Delete", bg="orange", fg="white", width=button_width, command=self.delete_data)
        delete_button.grid(row=6, column=1, padx=10, pady=10)

        update_button = Button(left_frame, text="Update", bg="orange", fg="white", width=button_width, command=self.update_data)
        update_button.grid(row=7, column=0, padx=10, pady=10)

        reset_button = Button(left_frame, text="Reset", bg="orange", fg="white", width=button_width, command=self.reset_fields)
        reset_button.grid(row=7, column=1, padx=10, pady=10)

        # Right Frame for Curriculum Table
        right_frame = LabelFrame(main_frame, bd=2, relief=RIDGE, text="Curriculum Table Management", bg="white")
        right_frame.place(x=497,y=10,width=475,height=470)  # Right side (table) with height 600

        # Database Frame inside the Right Section
        database_frame = LabelFrame(right_frame, bd=2, relief=RIDGE)
        database_frame.place(x=5, y=5, width=590, height=400)

        # Scrollbars
        scroll_left_right = ttk.Scrollbar(database_frame, orient=HORIZONTAL)
        scroll_up_down = ttk.Scrollbar(database_frame, orient=VERTICAL)

        # Teacher Database Treeview with only relevant information
        self.teacher_database = ttk.Treeview(database_frame, columns=("First Name", "Last Name", "Email", "Password", "Course", "Phone Number"),
                                            xscrollcommand=scroll_left_right.set,
                                            yscrollcommand=scroll_up_down.set)

        # Packing Scrollbars
        scroll_up_down.pack(side=RIGHT, fill=Y)
        scroll_up_down.config(command=self.teacher_database.yview)

        scroll_left_right.pack(side=BOTTOM, fill=X)
        scroll_left_right.config(command=self.teacher_database.xview)

        # Setting up headings
        self.teacher_database.heading("First Name", text="First Name")
        self.teacher_database.heading("Last Name", text="Last Name")
        self.teacher_database.heading("Email", text="Email Address")
        self.teacher_database.heading("Password", text="Password")
        self.teacher_database.heading("Course", text="Course")
        self.teacher_database.heading("Phone Number", text="Phone Number")

        # Show headings only
        self.teacher_database["show"] = "headings"

        # Setting column widths
        self.teacher_database.column("First Name", width=100)
        self.teacher_database.column("Last Name", width=100)
        self.teacher_database.column("Email", width=100)
        self.teacher_database.column("Password", width=100)  # Consider hiding this in practice
        self.teacher_database.column("Course", width=100)
        self.teacher_database.column("Phone Number", width=100)

        # Packing the Treeview
        self.teacher_database.pack(fill=BOTH, expand=1)
        self.teacher_database.bind("<ButtonRelease>", self.get_cursor)

        self.fetch_data()  # Fetch data on initialization


    # Database connection parameters
    db_config = {
        'host': 'localhost',  # Adjust this as needed
        'user': 'root',
        'password': 'Nightcore_1134372019!',
        'database': 'attendnow'
    }

    def fetch_departments(self):
        try:
            # Establish the connection
            connection = mysql.connector.connect(**db_config)
            cursor = connection.cursor()

            # Query to fetch unique departments
            query = "SELECT DISTINCT department FROM curriculum"
            cursor.execute(query)

            # Fetch all unique departments
            departments = [row[0] for row in cursor.fetchall()]

            # Close the cursor and connection
            cursor.close()
            connection.close()

            return departments

        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Error: {err}")
            return []

    def connect_to_db(self):
        try:
            conn = mysql.connector.connect(
                host="localhost",
                user="root",
                password="Nightcore_1134372019!",
                database="attendnow"
            )
            return conn
        except mysql.connector.Error as err:
            print(f"Error: {err}")
            return None

    def go_back(self):
        self.root.destroy()  # Close the curriculum interface
        self.open_admit_interface()  # Reopen admit interface

    def open_admit_interface(self):
        new_window = Tk()  # Create a new Tk window
        admit_interface.Admit_Interface(new_window, self.username)  # Open the admit interface with the stored username

    def fetch_data(self):
        pass

    def add_data(self):
        pass

    def delete_data(self):
        pass
    def update_data(self):
        pass
    def reset_fields(self):
        pass

    def get_cursor(self, event=None):
        pass


if __name__ == "__main__":
    root = Tk()
    app = Teacher_Interface(root, username="Username123")
    root.mainloop()
