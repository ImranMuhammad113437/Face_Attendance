from tkinter import *
from tkinter import ttk
from PIL import Image, ImageTk
import os
import mysql.connector
from tkinter import messagebox

class Timetable_Information:
    def __init__(self, root, username):
        self.root = root
        self.username = username  # Storing username for future use
        self.root.geometry("1024x590+0+0")
        self.root.title("AttendNow - Timetable Information")

#-----------Variable-----------------
        self.var_department = StringVar()
        self.var_course = StringVar()
        self.var_teacher_name = StringVar()
        self.var_timing =StringVar()
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
        title_label = Label(title_frame, text="Timetable Information", bg="orange", fg="white", font=("New Time Roman", 20, "bold"))
        title_label.place(x=2, y=2, width=445, height=40)

        # Back Button
        back_button = Button(self.root, text="Back", command=self.go_back, bg="blue", fg="white", font=("Arial", 12, "bold"))
        back_button.place(x=175, y=15, width=80, height=30)

        # Display username on the top right corner
        self.username_label = Label(self.root, text=f"Logged in as: {self.username}", bg="orange", fg="white", font=("Arial", 12))
        self.username_label.place(x=800, y=15)

        # Main Frame for Timetable Information Interface
        main_frame = Frame(background_img_main_position, bd=2, bg="orange")
        main_frame.place(x=150, y=100, width=700, height=450)

        # Upper Section Frame
        upper_frame = LabelFrame(main_frame, bd=2, relief=RIDGE, text="Timetable Information Table", bg="white")
        upper_frame.place(x=5, y=5, width=687, height=185)  # Adjusted height for the gap

        # Search Frame inside the Upper Section
        search_frame = LabelFrame(upper_frame, bd=2, relief=RIDGE, text="Search System")
        search_frame.place(x=5, y=5, width=676, height=50)

        # Search Title
        search_label = Label(search_frame, text="Search By: ")
        search_label.grid(row=0, column=0)

        # Dropdown Menu for Searching
        self.search_dropdown = ttk.Combobox(search_frame, state="readonly", width=12)
        self.search_dropdown["values"] = (
                                        "Select Search", 
                                        "Department",
                                        "Course", 
                                        "Teacher Name",
                                        "Timing"
                                        )
        self.search_dropdown.current(0)
        self.search_dropdown.grid(row=0, column=1, padx=3, pady=5, sticky=W)

        # Search input as a dropdown
        self.search_input = ttk.Combobox(search_frame, values=[], width=27, state='readonly')
        self.search_input.grid(row=0, column=2, padx=3)

        # Search Button
        search_button = Button(search_frame, text="Search", bg="orange", fg="white", width=20, command=self.show_search)
        search_button.grid(row=0, column=3, padx=3)

        # Show All Button
        show_all_button = Button(search_frame, text="Show All", bg="orange", fg="white", width=20, command=self.fetch_data)
        show_all_button.grid(row=0, column=4, padx=3)

        # Timetable Editing Section Frame
        timetable_editing_frame = LabelFrame(upper_frame, bd=2, relief=RIDGE, text="Timetable Editing", bg="white")
        timetable_editing_frame.place(x=5, y=60, width=676, height=120)  # Adjusted height to fit more rows

#------------------------------Department-----------------------------------------        
        # Department Label and Combobox
        department_label = Label(timetable_editing_frame, text="Department:", bg="white", fg="black", font=("Arial", 10))
        department_label.grid(row=0, column=0, padx=5, pady=2, sticky=W)  # Reduced padding

        # Department Combobox with textvariable
        self.var_department = StringVar()  # Create the StringVar
        self.department_input = ttk.Combobox(timetable_editing_frame, width=28, textvariable=self.var_department)

        # Sample values for department dropdown (can be fetched from the database)
        self.department_input['values'] = self.get_departments()
        # Set the default value (optional)
        self.department_input.current(0)  # This will set the first value in the list as default

        self.department_input.grid(row=0, column=1, padx=5, pady=2)
        self.department_input.bind("<<ComboboxSelected>>", self.update_courses)
#------------------------------------------------------------------------------------

#------------------------------Course-----------------------------------------        
        # Course Label and Combobox
        course_label = Label(timetable_editing_frame, text="Course:", bg="white", fg="black", font=("Arial", 10))
        course_label.grid(row=0, column=2, padx=5, pady=2, sticky=W)

        # Create StringVar for course
        self.var_course = StringVar()  # Create the StringVar
        self.course_input = ttk.Combobox(timetable_editing_frame, width=28, textvariable=self.var_course)

        # Sample values for course dropdown (can be fetched from the database)
        self.course_input['values'] = ("Select Course",)

        # Set the default value (optional)
        self.course_input.current(0)  # This will set the first value in the list as default

        self.course_input.grid(row=0, column=3, padx=5, pady=2)
#------------------------------------------------------------------------------------


        # Input fields for Teacher Name and Timing in row 1
        teacher_label = Label(timetable_editing_frame, text="Teacher Name:", bg="white", fg="black", font=("Arial", 10))
        teacher_label.grid(row=1, column=0, padx=5, pady=2, sticky=W)
        self.teacher_input = ttk.Combobox(timetable_editing_frame, width=28, textvariable=self.var_teacher_name)
        self.teacher_input['values'] = self.fetch_teacher_names()  # Add teacher names here
        self.teacher_input.grid(row=1, column=1, padx=5, pady=2)
        self.teacher_input.current(0)

        # Timing Dropdown Menu
        timing_label = Label(timetable_editing_frame, text="Timing:", bg="white", fg="black", font=("Arial", 10))
        timing_label.grid(row=1, column=2, padx=5, pady=2, sticky=W)

        # Dropdown options for timing
        time_options = [
            "Select Timing",
            "08:00 - 09:00",
            "09:00 - 10:00",
            "10:00 - 11:00",
            "11:00 - 12:00",
            "12:00 - 01:00",
            "01:00 - 02:00",
            "02:00 - 03:00",
            "03:00 - 04:00",
            "04:00 - 05:00"
        ]

        # Timing input as a dropdown
        self.timing_input = ttk.Combobox(timetable_editing_frame, values=time_options, width=27, textvariable=self.var_timing)
        self.timing_input.grid(row=1, column=3, padx=5, pady=2)

        # Optionally set the default value (e.g., "8:00 - 9:00")
        self.timing_input.current(0)  # This will set the default to the first option


        # Buttons for Add, Update, Delete, and Reset in row 2
        button_width = 10
        add_button = Button(timetable_editing_frame, text="Add", bg="orange", fg="white", width=button_width, command=self.add_data)
        add_button.grid(row=2, column=0, padx=2, pady=2)  # Reduced button padding

        delete_button = Button(timetable_editing_frame, text="Delete", bg="orange", fg="white", width=button_width, command=self.delete_data)
        delete_button.grid(row=2, column=1, padx=2, pady=2)

        
        reset_button = Button(timetable_editing_frame, text="Reset", bg="orange", fg="white", width=button_width, command=self.reset_fields)
        reset_button.grid(row=2, column=2, padx=2, pady=2)

        # Lower Section Frame
        lower_frame = LabelFrame(main_frame, bd=2, relief=RIDGE, text="Timetable Table Management", bg="white")
        lower_frame.place(x=5, y=200, width=687, height=237)  # Adjusted height for the gap

        # Database Frame inside the Lower Section
        database_frame = LabelFrame(lower_frame, bd=2, relief=RIDGE)
        database_frame.place(x=5, y=5, width=677, height=210)

        # Scrollbars
        scroll_left_right = ttk.Scrollbar(database_frame, orient=HORIZONTAL)
        scroll_up_down = ttk.Scrollbar(database_frame, orient=VERTICAL)

        # Timetable Database Treeview with Department, Course, Teacher Name, and Timing
        self.timetable_database = ttk.Treeview(database_frame, 
                                            columns=(
                                                "Department", 
                                                "Course", 
                                                "Teacher Name", 
                                                "Timing"),
                                            xscrollcommand=scroll_left_right.set, 
                                            yscrollcommand=scroll_up_down.set)

        # Packing Scrollbars
        scroll_up_down.pack(side=RIGHT, fill=Y)
        scroll_up_down.config(command=self.timetable_database.yview)

        # Setting up headings
        self.timetable_database.heading("Department", text="Department")
        self.timetable_database.heading("Course", text="Course")
        self.timetable_database.heading("Teacher Name", text="Teacher Name")
        self.timetable_database.heading("Timing", text="Timing")

        # Show headings only
        self.timetable_database["show"] = "headings"

        # Setting column widths
        self.timetable_database.column("Department", width=150)
        self.timetable_database.column("Course", width=150)
        self.timetable_database.column("Teacher Name", width=150)
        self.timetable_database.column("Timing", width=150)

        self.timetable_database.pack(fill=BOTH, expand=1)
        
        self.timetable_database.bind("<ButtonRelease>",self.get_cursor)
        self.search_dropdown.bind("<<ComboboxSelected>>", self.update_search_input)
        # Final step, fetch all data from the database to display
        self.fetch_data()

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
            messagebox.showerror("Database Error", f"Error: {err}")
            return None

    
    # Function to update search_input dropdown based on selection in search_dropdown
    def update_search_input(self,event):
        selected_option = self.search_dropdown.get()

        # Clear the current values in search_input dropdown
        self.search_input.set("")

        # Connect to the database
        try:
            connection = mysql.connector.connect(
                host="localhost",
                user="root",
                password="Nightcore_1134372019!",
                database="attendnow"
            )
            cursor = connection.cursor()

            if selected_option == "Department":
                # Query to fetch distinct departments
                cursor.execute("SELECT DISTINCT department FROM timetable")
                values = cursor.fetchall()
                departments = [row[0] for row in values]  # Extract department names from the result
                self.search_input["values"] = departments
            elif selected_option == "Course":
                # Query to fetch distinct courses
                cursor.execute("SELECT DISTINCT course FROM timetable")
                values = cursor.fetchall()
                courses = [row[0] for row in values]  # Extract course names from the result
                self.search_input["values"] = courses
            elif selected_option == "Teacher Name":
                # Query to fetch distinct teacher names
                cursor.execute("SELECT DISTINCT teacher_name FROM timetable")
                values = cursor.fetchall()
                teachers = [row[0] for row in values]  # Extract teacher names from the result
                self.search_input["values"] = teachers
            elif selected_option == "Timing":
                # Query to fetch distinct timings
                cursor.execute("SELECT DISTINCT timing FROM timetable")
                values = cursor.fetchall()
                timings = [row[0] for row in values]  # Extract timings from the result
                self.search_input["values"] = timings
            else:
                self.search_input["values"] = []  # Reset when no valid selection is made

            # Set default value to the first option after fetching
            self.search_input.current(0)

        except mysql.connector.Error as err:
            # Handle any errors
            messagebox.showerror("Database Error", f"Error: {str(err)}")
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()
    
    
    def fetch_data(self):
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM timetable")
        rows = cursor.fetchall()
        if rows:
            self.timetable_database.delete(*self.timetable_database.get_children())
            for row in rows:
                self.timetable_database.insert("", END, values=row)

    def fetch_teacher_names(self):
        try:
            # Establish a connection to the database
            conn = mysql.connector.connect(
                host="localhost",
                user="root",
                password="Nightcore_1134372019!",
                database="attendnow"
            )

            my_cursor = conn.cursor()

            # Fetch the full_name directly from the teacher_user table
            sql = "SELECT full_name FROM teacher_user"
            my_cursor.execute(sql)

            # Populate the list with the fetched names
            teacher_names = [name[0] for name in my_cursor.fetchall()]

            # Add the default "Select Teacher" at the beginning of the list
            teacher_names.insert(0, "Select Teacher")

            # Close the cursor and connection
            my_cursor.close()
            conn.close()

            # Populate the Combobox with teacher names
            self.teacher_input['values'] = teacher_names

            # Select "Select Teacher" by default
            self.teacher_input.current(0)

        except mysql.connector.Error as e:
            messagebox.showerror("Database Error", f"Error connecting to database: {str(e)}")



    def show_search(self):
        # Get selected search category and search term entered by the user
        search_by = self.search_dropdown.get()
        search_term = self.search_input.get()

        # Check if a valid search term has been entered
        if not search_term or search_term == "Select Option":
            messagebox.showerror("Input Error", "Please enter a valid search term.")
            return

        # Create cursor for executing the query
        cursor = self.conn.cursor()

        # Initialize query and condition based on search category
        if search_by == "Department":
            query = "SELECT * FROM timetable WHERE department = %s"
        elif search_by == "Course":
            query = "SELECT * FROM timetable WHERE course = %s"
        elif search_by == "Teacher Name":
            query = "SELECT * FROM timetable WHERE teacher_name = %s"
        elif search_by == "Timing":
            query = "SELECT * FROM timetable WHERE timing = %s"
        else:
            messagebox.showerror("Search Error", "Please select a valid search option.")
            return

        try:
            # Execute the query with the search term
            cursor.execute(query, (search_term,))
            rows = cursor.fetchall()

            if rows:
                # Clear any existing data in the Treeview
                self.timetable_database.delete(*self.timetable_database.get_children())
                # Insert the rows fetched from the database into the Treeview
                for row in rows:
                    self.timetable_database.insert("", "end", values=row)
            else:
                # Show an error message if no rows match the search term
                messagebox.showinfo("No Results", "No results found for the search term.")
        except mysql.connector.Error as err:
            # Handle any database errors
            messagebox.showerror("Database Error", f"Error: {str(err)}")
        finally:
            cursor.close()



    def update_courses(self, event):
        selected_department = self.var_department.get()  # Get the selected department
        self.course_input["values"] = self.get_courses(selected_department)  # Fetch corresponding courses
        self.course_input.current(0)  # Reset the course dropdown

    def get_courses(self, department):
        # Connect to the MySQL database
        connection = mysql.connector.connect(
            host="localhost",
            user="root",  # Your MySQL username
            password="Nightcore_1134372019!",  # Your MySQL password
            database="attendnow"
        )
        
        cursor = connection.cursor()
        cursor.execute("SELECT course FROM curriculum WHERE department = %s", (department,))  # Adjust column names as needed
        courses = [row[0] for row in cursor.fetchall()]  # Fetch course names based on selected department

        cursor.close()
        connection.close()

        return ["Select Course"] + courses  # Add default option

    def get_departments(self):
            # Connect to the MySQL database
            connection = mysql.connector.connect(
                host="localhost",
                user="root",  # Your MySQL username
                password="Nightcore_1134372019!",  # Your MySQL password
                database="attendnow"
            )
            
            cursor = connection.cursor()
            cursor.execute("SELECT DISTINCT department FROM curriculum")  # Adjust the column name as needed
            departments = [row[0] for row in cursor.fetchall()]  # Fetch all unique department names

            cursor.close()
            connection.close()

            return ["Select Department"] + departments  # Add default option

    def get_cursor(self,event=""):
        cursor_focus=self.timetable_database.focus()
        content=self.timetable_database.item(cursor_focus)
        data=content["values"]
        self.var_department.set(data[0]),
        self.var_course.set(data[1]),
        self.var_teacher_name.set(data[2]),
        self.var_timing.set(data[3])
        

    def add_data(self):
        # Check if the user has selected default values
        if (self.department_input.get() == "Select Department" or
            self.course_input.get() == "Select Course" or
            self.teacher_input.get() == "Select Teacher" or
            self.timing_input.get() == "Select Timing"):
            
            # Show a message box if any field has the default value
            messagebox.showerror("Input Error", "Please make sure to select all options: Department, Course, Teacher, and Timing.")
            return  # Exit the function to avoid inserting invalid data

        # Proceed with inserting data into the database if all fields are properly selected
        cursor = self.conn.cursor()
        query = "INSERT INTO timetable (department, course, teacher_name, timing) VALUES (%s, %s, %s, %s)"
        values = (  
                    self.department_input.get(), 
                    self.course_input.get(), 
                    self.teacher_input.get(), 
                    self.timing_input.get())
        cursor.execute(query, values)
        self.conn.commit()
        
        # Refresh the data display after adding the new entry
        self.fetch_data()

        
    def delete_data(self):
        cursor = self.conn.cursor()

        # Updated query to include multiple conditions
        query = """
            DELETE FROM timetable 
            WHERE department = %s 
            AND course = %s 
            AND teacher_name = %s 
            AND timing = %s
        """
        
        # Execute the query with values for department, course, teacher_name, and timing
        cursor.execute(query, (
            self.department_input.get(),
            self.course_input.get(),
            self.teacher_input.get(),
            self.timing_input.get()
        ))

        # Commit the transaction to the database
        self.conn.commit()

        # Fetch the updated data
        self.fetch_data()

        

    def reset_fields(self):
        self.department_input.delete(0, END)
        self.course_input.delete(0, END)
        self.teacher_input.delete(0, END)
        self.timing_input.delete(0, END)

    def go_back(self):
        self.root.destroy()
        import admit_interface
        admit_interface.Admit_Interface(Tk(), self.username)



if __name__ == "__main__":
    root = Tk()
    app = Timetable_Information(root, "TeacherName")  # Replace "TeacherName" with the actual username
    root.mainloop()
