from tkinter import *
from tkinter import ttk
from tkinter import Frame
from PIL import Image, ImageTk
import calendar
import os
import admit_interface
import mysql.connector  # Import MySQL Connector
from tkinter import messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


class Emotion_Status_Interface:
    def __init__(self, root, username):
        self.root = root
        self.username = username  # Storing username for future use
        self.root.geometry("1024x590")  # Adjusted window size for side-by-side layout
        self.root.title("AttendNow - Emotion Status")

        # Variables for the teacher's emotion status
        self.var_teacher_course = StringVar()
        self.var_teacher = StringVar()
        

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
        title_label = Label(title_frame, text="Emotion Status Management", bg="orange", fg="white", font=("New Time Roman", 20, "bold"))
        title_label.place(x=2, y=2, width=445, height=40)

        # Back Button
        back_button = Button(self.root, text="Back", command=self.go_back, bg="red", fg="white", font=("Arial", 12, "bold"))
        back_button.place(x=175, y=15, width=80, height=30)

        # Display username on the top right corner
        self.username_label = Label(self.root, text=f"Logged in as: {self.username}", bg="orange", fg="white", font=("Arial", 12))
        self.username_label.place(x=800, y=15)

        # Main Frame (Split into left and right)
        self.main_frame = Frame(self.root, bd=2, bg="orange")
        self.main_frame.place(x=490, y=70, width=500, height=400)

        # Clear chart button
        self.clear_chart_button = Button(self.root, text="Clear Chart", command=self.clear_chart_function)
        self.clear_chart_button.place(x=490, y=480, width=100, height=30)


       # Teacher Label
        teacher_label = Label(background_img_main_position, text="Teacher:", bg="white")
        teacher_label.place(x=160, y=80, width=70, height=30)

        # Set default value for the teacher combobox
        self.var_teacher = StringVar()  # Declare the variable for the combobox
        self.var_teacher.set("Select Teacher")  # Set the default value to "Select Teacher"

        self.teacher_combobox = ttk.Combobox(background_img_main_position, textvariable=self.var_teacher, state="readonly")
        self.teacher_combobox.place(x=250, y=80, width=200, height=30)

        # Dropdown Menu 2 - Course
        course_label = Label(background_img_main_position, text="Course:", bg="white")
        course_label.place(x=160, y=120, width=70, height=30)

        # Set default value for the course combobox
        self.var_teacher_course = StringVar()  # Declare the variable for the combobox
        self.var_teacher_course.set("Select Teacher's Course")  # Set default value

        self.course_combobox = ttk.Combobox(background_img_main_position, textvariable=self.var_teacher_course, state="readonly")
        self.course_combobox['values'] = []  # Initially empty, will be populated later
        self.course_combobox.place(x=250, y=120, width=200, height=30)


        

       # Search Button
        search_button = Button(background_img_main_position, text="Search Student", command=self.search_student, bg="green", fg="white")
        search_button.place(x=160, y=160, width=290, height=40)

       # Table (Treeview) for displaying student names and IDs
        columns = ('student_id', 'student_name')

        # Create the Treeview widget
        self.student_table = ttk.Treeview(background_img_main_position, columns=columns, show='headings', yscrollcommand=lambda f, l: self.scrollbar.set(f, l))

        # Define the column headings
        self.student_table.heading('student_id', text='Student ID')
        self.student_table.heading('student_name', text='Student Name')

        # Set equal column widths
        self.student_table.column('student_id', width=145, anchor='center')
        self.student_table.column('student_name', width=145, anchor='center')

        # Place the table below the search button
        self.student_table.place(x=160, y=210, width=290, height=150)

        # Create a vertical scrollbar and link it to the Treeview
        self.scrollbar = Scrollbar(background_img_main_position, orient="vertical", command=self.student_table.yview)
        self.scrollbar.place(x=450, y=210, height=150)  # Position it next to the table

        # Bind the selection event to the on_student_select function
        self.student_table.bind("<<TreeviewSelect>>", self.on_student_select)

        # Create Label for additional input field (e.g., "Selected Student")
        selected_student_label = Label(background_img_main_position, text="Selected Student:", bg="white")
        selected_student_label.place(x=160, y=370, width=110, height=30)

        # Create a read-only Entry field
        self.selected_student_input = Entry(background_img_main_position, state='readonly')
        self.selected_student_input.place(x=290, y=370, width=160, height=30)

        # Create Label for the "Student ID"
        student_id_label = Label(background_img_main_position, text="Student ID:", bg="white")
        student_id_label.place(x=160, y=410, width=110, height=30)

        # Create a read-only Entry field for the "Student ID"
        self.student_id_input = Entry(background_img_main_position, state='readonly')
        self.student_id_input.place(x=290, y=410, width=160, height=30)

       # Create Label for the "Month"
        month_label = Label(background_img_main_position, text="Month:", bg="white")
        month_label.place(x=160, y=450, width=110, height=30)

        # Create a dropdown menu (Combobox) for the "Month"
        self.month_input = ttk.Combobox(background_img_main_position, values=[
            "January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"
        ], state='readonly')
        self.month_input.place(x=290, y=450, width=160, height=30)

        # Optionally, set the default selected value
        self.month_input.set("Select Month")

       # Create Label for the "Year"
        year_label = Label(self.root, text="Year:", bg="white")
        year_label.place(x=160, y=490, width=110, height=30)

        # Create a dropdown menu (Combobox) for the "Year"
        self.year_input = ttk.Combobox(self.root, state='readonly')
        self.year_input.place(x=290, y=490, width=160, height=30)

        # Set the default value for the year
        self.year_input.set("Select Year")

        # Call the function to fetch and populate years from the database
        self.fetch_years()

        # Create a button labeled "Get Emotion Status" below the "Student ID" input field
        get_emotion_status_button = Button(background_img_main_position, text="Get Emotion Status", command=self.get_emotion_status)
        get_emotion_status_button.place(x=160, y=530, width=290, height=30)

       

        
        self.teacher_combobox.bind("<<ComboboxSelected>>", self.on_teacher_selected)
        self.fetch_teachers()
        
       
        


#------------------------------------------------------------------------------------------------
    def fetch_years(self):
        try:
            # Establish a connection to the database (MySQL in this case)
            conn = mysql.connector.connect(
                host="localhost",
                user="root",
                password="Nightcore_1134372019!",  # Replace with your password
                database="attendnow"
            )
            cursor = conn.cursor()

            # Query to get distinct years from the date column
            query = "SELECT DISTINCT YEAR(date) FROM student_emotion ORDER BY YEAR(date) ASC"
            cursor.execute(query)

            # Fetch the result and store unique years
            years = [str(row[0]) for row in cursor.fetchall()]

            # Close the database connection
            cursor.close()
            conn.close()

            # Set the year options in the combobox
            self.year_input['values'] = years

        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Error: {err}")
    
    
    def clear_chart_function(self):
        # Clear the existing chart from the main_frame
        for widget in self.main_frame.winfo_children():
            widget.destroy()
        
        
    # Function to display selected month in terminal
    def display_selected_month(self):
        month_mapping = {
            "January": "01",
            "February": "02",
            "March": "03",
            "April": "04",
            "May": "05",
            "June": "06",
            "July": "07",
            "August": "08",
            "September": "09",
            "October": "10",
            "November": "11",
            "December": "12"
        }
        
        selected_month = self.month_input.get()  # Get the selected value from the combobox
        
        if selected_month in month_mapping:  # Ensure a valid month is selected
            numerical_value = month_mapping[selected_month]
            print(f"Selected Month: {selected_month}, Numerical Value: {numerical_value}")
            return numerical_value
        else:
            print("No month selected.")
            return None

    
    
    def get_emotion_status(self):
        student_name = self.selected_student_input.get()
        student_id = self.student_id_input.get()
        month_value = self.display_selected_month()
        month_name = calendar.month_name[int(month_value)]
        selected_year = self.year_input.get()  # Get the selected year from the year dropdown

        if not student_name or not student_id:
            messagebox.showwarning("Warning", "Please select a student.")
            return

        if selected_year == "Select Year":  # Check if a valid year is selected
            messagebox.showwarning("Warning", "Please select a year.")
            return

        # Connect to the MySQL database
        connection = mysql.connector.connect(
            host="localhost",  # Replace with your host if different
            user="root",
            password="Nightcore_1134372019!",
            database="attendnow"
        )
        
        cursor = connection.cursor()

        # SQL query to extract emotion data by student name, ID, month, and year
        query = """
            SELECT date, neutral, happy, sad, fear, surprise, angry
            FROM student_emotion
            WHERE student_name = %s 
            AND student_id = %s 
            AND MONTH(date) = %s
            AND YEAR(date) = %s
            ORDER BY date;
        """
        
        cursor.execute(query, (student_name, student_id, month_value, selected_year))
        results = cursor.fetchall()
        
        # Close the database connection 
        connection.close()

        if not results:
            messagebox.showinfo("Info", f"No emotion data found for the selected student in {month_name}, {selected_year}.")
            return

        # Extracting data for the chart
        days = []  # Change this to hold days instead of full dates
        neutral = []
        happy = []
        sad = []
        fear = []
        surprise = []
        angry = []
        
        for row in results:
            # Extract the day from the date
            date_str = str(row[0])  # Assuming the date is in a datetime format
            day = date_str.split('-')[2]  # Get the day (DD) from YYYY-MM-DD
            
            days.append(day)  # Append the day instead of the full date
            neutral.append(row[1])
            happy.append(row[2])
            sad.append(row[3])
            fear.append(row[4])
            surprise.append(row[5])
            angry.append(row[6])

        # Plotting the vertical stacked bar chart
        figure, ax = plt.subplots(figsize=(6, 4))

        # Stacking the bars correctly
        ax.bar(days, neutral, label='Neutral', color='gray')
        ax.bar(days, happy, bottom=neutral, label='Happy', color='yellow')
        ax.bar(days, sad, bottom=[i + j for i, j in zip(neutral, happy)], label='Sad', color='blue')
        ax.bar(days, fear, bottom=[i + j + k for i, j, k in zip(neutral, happy, sad)], label='Fear', color='purple')
        ax.bar(days, surprise, bottom=[i + j + k + l for i, j, k, l in zip(neutral, happy, sad, fear)], label='Surprise', color='orange')
        ax.bar(days, angry, bottom=[i + j + k + l + m for i, j, k, l, m in zip(neutral, happy, sad, fear, surprise)], label='Angry', color='red')

        # Setting the labels
        ax.set_xlabel('Day (DD)')
        ax.set_ylabel('Emotion')
        ax.set_title(f'Emotion Status for {student_name} ({month_name}, {selected_year})')
        ax.legend()

        # Displaying the chart in the Tkinter Frame (main_frame)
        canvas = FigureCanvasTkAgg(figure, master=self.main_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)

       

    def go_back(self):
        self.root.destroy() 
        new_window =Tk()
        admit_interface.Admit_Interface(new_window, self.username)
        # You can add functionality here to return to the previous interface (like admit_interface)

    def on_teacher_selected(self, event):
        selected_teacher = self.teacher_combobox.get()
        if selected_teacher:
            self.fetch_courses(selected_teacher)

    # Search button functionality to filter and display emotion status based on dropdown selections
        # Search button functionality to filter and display emotion status based on dropdown selections
    def search_student(self):
        selected_course = self.var_teacher_course.get()  # Get the selected course from the combobox
        if not selected_course or selected_course == "Select Teacher's Course":
            messagebox.showerror("Error", "Please select a course.")
            return

        try:
            # Connect to the database
            conn = mysql.connector.connect(
                host="localhost",
                user="root",
                password="Nightcore_1134372019!",
                database="attendnow"
            )
            cursor = conn.cursor()

            # Query to select students from the selected course
            query = "SELECT student_id, student_name FROM students WHERE course = %s"
            cursor.execute(query, (selected_course,))  # Use parameterized query to avoid SQL injection
            rows = cursor.fetchall()

            # Clear the existing data in the table
            for row in self.student_table.get_children():
                self.student_table.delete(row)

            # Insert the new data into the student_table
            for row in rows:
                self.student_table.insert("", "end", values=row)

            conn.close()  # Close the connection

        except Exception as e:
            messagebox.showerror("Error", f"Error due to: {str(e)}")



    # Function to update the selected student's details in the input fields
    def on_student_select(self, event):  # Add 'self' to make it an instance method
        # Get the selected row
        selected_item = self.student_table.selection()

        if selected_item:
            # Extract values from the selected row
            student_id, student_name = self.student_table.item(selected_item, 'values')

            # Set the extracted values in the corresponding Entry fields
            self.selected_student_input.config(state='normal')  # Set state to normal to update the value
            self.selected_student_input.delete(0, 'end')  # Clear the current value
            self.selected_student_input.insert(0, student_name)  # Insert the student's name
            self.selected_student_input.config(state='readonly')  # Set state back to readonly

            self.student_id_input.config(state='normal')  # Set state to normal to update the value
            self.student_id_input.delete(0, 'end')  # Clear the current value
            self.student_id_input.insert(0, student_id)  # Insert the student's ID
            self.student_id_input.config(state='readonly')  # Set state back to readonly


    def fetch_teachers(self):
        try:
            # Connect to the database
            conn = mysql.connector.connect(
                host="localhost",  # Adjust the host if necessary
                user="root",  # Your MySQL username
                password="Nightcore_1134372019!",  # Your MySQL password
                database="attendnow"  # Database name
            )
            cursor = conn.cursor()

            # Query to select teacher names from the timetable table
            cursor.execute("SELECT teacher_name FROM timetable")
            rows = cursor.fetchall()

            # Use a set to avoid duplicate teacher names
            teacher_set = {row[0] for row in rows}  # Set comprehension to keep unique names
            teacher_list = list(teacher_set)  # Convert set back to list
            self.teacher_combobox['values'] = teacher_list  # Populate combobox with unique names

            conn.close()  # Close the connection

        except Exception as e:
            messagebox.showerror("Error", f"Error due to: {str(e)}")

    def fetch_courses(self, teacher_name):
        try:
            # Connect to the database
            conn = mysql.connector.connect(
                host="localhost",  # Adjust the host if necessary
                user="root",  # Your MySQL username
                password="Nightcore_1134372019!",  # Your MySQL password
                database="attendnow"  # Database name
            )
            cursor = conn.cursor()

            # Query to select course names from the timetable where the teacher matches the selected teacher
            query = "SELECT course FROM timetable WHERE teacher_name = %s"
            cursor.execute(query, (teacher_name,))  # Use parameterized query to avoid SQL injection
            rows = cursor.fetchall()

            # Use a set to avoid duplicate course names
            course_set = {row[0] for row in rows}
            course_list = list(course_set)  # Convert set back to list for combobox
            self.course_combobox['values'] = course_list  # Populate combobox with unique courses

            conn.close()  # Close the connection

        except Exception as e:
            messagebox.showerror("Error", f"Error due to: {str(e)}")


   


# Main execution
if __name__ == "__main__":
    root = Tk()
    app = Emotion_Status_Interface(root, username="JohnDoe")
    root.mainloop()
