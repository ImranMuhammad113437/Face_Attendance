from tkinter import *
from tkinter import ttk
from PIL import Image, ImageTk
import os
import admit_interface  # Import admit_interface for the back button functionality
import mysql.connector  # Import MySQL Connector
from tkinter import messagebox


class Curriculum_Interface:
    def __init__(self, root, username):
        self.root = root
        self.username = username  # Storing username for future use
        self.root.geometry("1024x590+0+0")
        self.root.title("AttendNow - Curriculum")

        self.var_department = StringVar()
        self.var_course = StringVar()

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
        main_frame.place(x=150, y=100, width=700, height=450)

        # Upper Section Frame
        upper_frame = LabelFrame(main_frame, bd=2, relief=RIDGE, text="Curriculum Table", bg="white")
        upper_frame.place(x=5, y=5, width=687, height=185)  # Adjusted height for the gap

        # Search Frame inside the Upper Section
        search_frame = LabelFrame(upper_frame, bd=2, relief=RIDGE, text="Search System")
        search_frame.place(x=5, y=5, width=676, height=50)

        # Search Title
        search_label = Label(search_frame, text="Search By: ")
        search_label.grid(row=0, column=0)

        # Dropdown Menu for Searching
        self.search_dropdown = ttk.Combobox(search_frame, state="readonly", width=12)
        self.search_dropdown["values"] = ("Select Search", "Department", "Course")
        self.search_dropdown.current(0)
        self.search_dropdown.grid(row=0, column=1, padx=3, pady=5, sticky=W)

        # Search InputField
        self.search_input = ttk.Entry(search_frame, width=30)
        self.search_input.grid(row=0, column=2, padx=3)

        # Search Button
        search_button = Button(search_frame, text="Search", bg="orange", fg="white", width=20, command=self.show_search)
        search_button.grid(row=0, column=3, padx=3)

        # Show All Button
        show_all_button = Button(search_frame, text="Show All", bg="orange", fg="white", width=20, command=self.fetch_data)
        show_all_button.grid(row=0, column=4, padx=3)

        
        # Curriculum Editing Section Frame
        curriculum_editing_frame = LabelFrame(upper_frame, bd=2, relief=RIDGE, text="Curriculum Editing", bg="white")
        curriculum_editing_frame.place(x=5, y=60, width=676, height=90)  # Adjusted position and size

       # Input fields for Department and Course inside the Curriculum Editing section
        # Calculating button width
        button_width = 22  # 3px padding on both sides of each button, with 5 gaps

        # Input fields for Department and Course inside the Curriculum Editing section
        department_label = Label(curriculum_editing_frame, text="Department:", bg="white", fg="black", font=("Arial", 10))
        department_label.grid(row=0, column=2, padx=10, pady=3, sticky=W)
        self.department_input = ttk.Entry(curriculum_editing_frame, width=30)
        self.department_input.grid(row=0, column=3, padx=10, pady=3)

        course_label = Label(curriculum_editing_frame, text="Course:", bg="white", fg="black", font=("Arial", 10))
        course_label.grid(row=1, column=2, padx=10, pady=3, sticky=W)
        self.course_input = ttk.Entry(curriculum_editing_frame, width=30)
        self.course_input.grid(row=1, column=3, padx=10, pady=3)

        # Buttons for Add, Update, Delete, and Reset inside the Curriculum Editing section
        add_button = Button(curriculum_editing_frame, text="Add", bg="orange", fg="white", width=button_width, command=self.add_data)
        add_button.grid(row=0, column=0, padx=3, pady=3)

        delete_button = Button(curriculum_editing_frame, text="Delete", bg="orange", fg="white", width=button_width, command=self.delete_data)
        delete_button.grid(row=0, column=1, padx=3, pady=3)

        update_button = Button(curriculum_editing_frame, text="Update", bg="orange", fg="white", width=button_width, command=self.update_data)
        update_button.grid(row=1, column=0, padx=3, pady=3)

        reset_button = Button(curriculum_editing_frame, text="Reset", bg="orange", fg="white", width=button_width, command=self.reset_fields)
        reset_button.grid(row=1, column=1, padx=3, pady=3)


        # Lower Section Frame
        lower_frame = LabelFrame(main_frame, bd=2, relief=RIDGE, text="Curriculum Table Management", bg="white")
        lower_frame.place(x=5, y=200, width=687, height=237)  # Adjusted height for the gap

        # Database Frame inside the Lower Section
        database_frame = LabelFrame(lower_frame, bd=2, relief=RIDGE)
        database_frame.place(x=5, y=5, width=677, height=210)

        # Scrollbars
        scroll_left_right = ttk.Scrollbar(database_frame, orient=HORIZONTAL)
        scroll_up_down = ttk.Scrollbar(database_frame, orient=VERTICAL)

        # Student Database Treeview with only Department and Course
        self.student_database = ttk.Treeview(database_frame, columns=("Department", "Course"),
                                              xscrollcommand=scroll_left_right.set, 
                                              yscrollcommand=scroll_up_down.set)

        # Packing Scrollbars
        scroll_up_down.pack(side=RIGHT, fill=Y)       
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



    def fetch_data(self):
        try:
            # Establish connection using connection details
            conn = mysql.connector.connect(
                host="localhost",
                user="root",
                password="Nightcore_1134372019!",
                database="attendnow"
            )

            # Create a cursor and execute the query
            cursor = conn.cursor()
            cursor.execute("SELECT Department, Course FROM curriculum")
            
            # Fetch all data
            data = cursor.fetchall()

            # Check if data exists and update the treeview
            if len(data) != 0:
                self.student_database.delete(*self.student_database.get_children())  # Clear current data
                for row in data:
                    self.student_database.insert("", "end", values=row)

        except mysql.connector.Error as err:
            print(f"Error: {err}")

        finally:
            # Close connection in the finally block
            if conn.is_connected():
                cursor.close()
                conn.close()

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

    # Placeholder methods for button functionality
    def add_data(self):
        # Validate if the department and course fields are selected
        if self.department_input.get() == "Select Department" or self.course_input.get() == "Select Course":
            messagebox.showerror("Missing Field", "All fields are required to be filled!", parent=self.root)
        else:
            try:
                # Establish a database connection using connection details
                conn = mysql.connector.connect(
                    host="localhost",
                    user="root",
                    password="Nightcore_1134372019!",
                    database="attendnow"
                )
                cursor = conn.cursor()

                # Insert the data into the curriculum table
                query = "INSERT INTO curriculum (Department, Course) VALUES (%s, %s)"
                values = (self.department_input.get(), self.course_input.get())
                cursor.execute(query, values)

                # Commit the changes
                conn.commit()

                # Clear input fields after insertion
                self.reset_fields()

                # Fetch the updated data and refresh the table
                self.fetch_data()

                # Show success message
                messagebox.showinfo("Successful", "Data added successfully", parent=self.root)
            except mysql.connector.Error as err:
                messagebox.showerror("Error", f"Error: {err}", parent=self.root)
            finally:
                if conn.is_connected():
                    cursor.close()
                    conn.close()

    def update_data(self):
        pass

    def delete_data(self):
        # Get the selected item from the Treeview
        selected_item = self.student_database.selection()
        if not selected_item:
            print("Please select a record to delete.")
            return

        # Get the values of the selected item
        item_values = self.student_database.item(selected_item, 'values')
        if item_values:
            department, course = item_values

            # Confirm deletion
            confirm = messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete the course '{course}' from the department '{department}'?")
            if confirm:
                # Try deleting data from the database
                try:
                    cursor = self.conn.cursor()

                    # Delete the data from the curriculum table
                    query = "DELETE FROM curriculum WHERE Department = %s AND Course = %s"
                    values = (department, course)
                    cursor.execute(query, values)

                    # Commit the changes
                    self.conn.commit()

                    # Refresh the data in the Treeview
                    self.fetch_data()

                    print("Data deleted successfully")
                except mysql.connector.Error as err:
                    print(f"Error: {err}")
                finally:
                    cursor.close()
        else:
            print("No valid selection made.")

    def reset_fields(self):
        pass

    def get_cursor(self, event=""):
        # Get the current selected item from the Treeview
        cursor_focus = self.student_database.focus()
        
        # Get the content of the selected row (dictionary)
        content = self.student_database.item(cursor_focus)
        
        # Extract the values (Department, Course) from the content
        data = content["values"]
        
        # If data is available, set it to the input fields
        if data:
            self.department_input.delete(0, END)  # Clear previous content
            self.department_input.insert(END, data[0])  # Set Department
            
            self.course_input.delete(0, END)  # Clear previous content
            self.course_input.insert(END, data[1])  # Set Course



if __name__ == "__main__":
    root = Tk()
    app = Curriculum_Interface(root, "TeacherName")  # Replace "TeacherName" with the actual username
    root.mainloop()
