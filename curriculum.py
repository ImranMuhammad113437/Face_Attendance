from tkinter import *
from tkinter import ttk
from PIL import Image, ImageTk
import os
import admit_interface  # Import admit_interface for the back button functionality
import mysql.connector  # Import MySQL Connector

class Curriculum_Interface:
    def __init__(self, root, username):
        self.root = root
        self.username = username  # Storing username for future use
        self.root.geometry("1024x590+0+0")
        self.root.title("AttendNow - Curriculum")

        # Connect to the database
        self.conn = self.connect_to_db()

        # Background Image
        background_img_main = Image.open(r"Image\Background.png")
        background_img_main = background_img_main.resize((1024, 590), Image.Resampling.LANCZOS)
        self.photo_background_img_main = ImageTk.PhotoImage(background_img_main)
        background_img_main_position = Label(self.root, image=self.photo_background_img_main)
        background_img_main_position.place(x=0, y=0, width=1024, height=590)

        # LogoTitle Image
        left_title = Image.open(r"Image\LogoTitle_Left Top.png")
        self.photoleft_title = ImageTk.PhotoImage(left_title)
        left_title_position = Label(self.root, image=self.photoleft_title)
        left_title_position.place(x=0, y=0, width=163, height=60)

        # Title Bar
        title_frame = Frame(background_img_main_position, bd=2, bg="orange")
        title_frame.place(x=300, y=5, width=450, height=50)
        title_label = Label(title_frame, text="Curriculum Management Table", bg="orange", fg="white", font=("New Time Roman", 20, "bold"))
        title_label.place(x=2, y=2, width=445, height=40)

        # Back Button
        back_button = Button(self.root, text="Back", command=self.go_back, bg="red", fg="white", font=("Arial", 12, "bold"))
        back_button.place(x=175, y=15, width=80, height=30)

        # Display username on the top right corner
        self.username_label = Label(self.root, text=f"Logged in as: {self.username}", bg="orange", fg="white", font=("Arial", 12))
        self.username_label.place(x=800, y=15)

        # Main Frame for Curriculum Interface
        main_frame = Frame(background_img_main_position, bd=2, bg="orange")
        main_frame.place(x=150, y=100, width=700, height=400)

        # Upper Section Frame
        upper_frame = LabelFrame(main_frame, bd=2, relief=RIDGE, text="Curriculum Table", bg="white")
        upper_frame.place(x=5, y=5, width=687, height=185)  # Adjusted height for the gap

        # Search Frame inside the Upper Section
        search_frame = LabelFrame(upper_frame, bd=2, relief=RIDGE, text="Search System")
        search_frame.place(x=5, y=5, width=677, height=50)

        # Search Title
        search_label = Label(search_frame, text="Search By: ")
        search_label.grid(row=0, column=0)

        # Dropdown Menu for Searching
        self.search_dropdown = ttk.Combobox(search_frame, state="readonly", width=12)
        self.search_dropdown["values"] = ("Select Search", "Department", "Course")
        self.search_dropdown.current(0)
        self.search_dropdown.grid(row=0, column=1, padx=3, pady=5, sticky=W)

        # Search InputField
        self.search_input = ttk.Entry(search_frame, width=15)
        self.search_input.grid(row=0, column=2, padx=3)

        # Search Button
        search_button = Button(search_frame, text="Search", bg="orange", fg="white", width=12, command=self.show_search)
        search_button.grid(row=0, column=3, padx=3)

        # Show All Button
        show_all_button = Button(search_frame, text="Show All", bg="orange", fg="white", width=10, command=self.fetch_data)
        show_all_button.grid(row=0, column=4, padx=3)

        # Lower Section Frame
        lower_frame = LabelFrame(main_frame, bd=2, relief=RIDGE, text="Curriculum Table Management", bg="white")
        lower_frame.place(x=5, y=200, width=687, height=185)  # Adjusted height for the gap

        # Database Frame inside the Lower Section
        database_frame = LabelFrame(lower_frame, bd=2, relief=RIDGE)
        database_frame.place(x=5, y=5, width=677, height=170)

        # Scrollbars
        scroll_left_right = ttk.Scrollbar(database_frame, orient=HORIZONTAL)
        scroll_up_down = ttk.Scrollbar(database_frame, orient=VERTICAL)

        # Student Database Treeview with only Department and Course
        self.student_database = ttk.Treeview(database_frame, columns=("Department", "Course"),
                                              xscrollcommand=scroll_left_right.set, 
                                              yscrollcommand=scroll_up_down.set)

        # Packing Scrollbars
        scroll_left_right.pack(side=BOTTOM, fill=X)
        scroll_up_down.pack(side=RIGHT, fill=Y)       
        scroll_left_right.config(command=self.student_database.xview)
        scroll_up_down.config(command=self.student_database.yview)

        # Setting up headings
        self.student_database.heading("Department", text="Department")
        self.student_database.heading("Course", text="Course")

        # Show headings only
        self.student_database["show"] = "headings"

        # Setting column widths
        self.student_database.column("Department", width=200)  # Adjusted width if necessary
        self.student_database.column("Course", width=200)      # Adjusted width if necessary

        # Packing the Treeview
        self.student_database.pack(fill=BOTH, expand=1)
        self.student_database.bind("<ButtonRelease>", self.get_cursor)

        self.fetch_data()  # Fetch data on initialization

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

    # Method to fetch data from the database
    def fetch_data(self):
        if self.conn:
            cursor = self.conn.cursor()
            query = "SELECT Department, Course FROM curriculum"
            cursor.execute(query)
            rows = cursor.fetchall()
            if len(rows) != 0:
                self.student_database.delete(*self.student_database.get_children())  # Clear current data
                for row in rows:
                    self.student_database.insert('', END, values=row)
            cursor.close()

    # Placeholder method for search functionality
    def show_search(self):
        if self.conn and self.search_input.get():
            cursor = self.conn.cursor()
            search_column = self.search_dropdown.get()
            search_value = self.search_input.get()
            query = f"SELECT Department, Course FROM curriculum WHERE {search_column} LIKE '%{search_value}%'"
            cursor.execute(query)
            rows = cursor.fetchall()
            if len(rows) != 0:
                self.student_database.delete(*self.student_database.get_children())
                for row in rows:
                    self.student_database.insert('', END, values=row)
            cursor.close()

    def get_cursor(self, event):
        # Logic to handle selection in the Treeview
        pass


if __name__ == "__main__":
    root = Tk()
    root.resizable(False, False)
    obj = Curriculum_Interface(root, "Guest")  # Replace "Guest" with actual username
    root.mainloop()
