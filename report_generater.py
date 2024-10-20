import tkinter as tk
from tkinter import ttk, Listbox
from tkinter import Frame, Canvas, Scrollbar, Label, messagebox, StringVar, BooleanVar, Entry, Listbox
from tkinter import LabelFrame, Label, Entry, Button, StringVar
from tkinter import *
from PIL import Image, ImageTk
import admit_interface
import mysql.connector  # Import your database library
from tkinter import Label, Frame, messagebox  # Ensure required Tkinter classes are imported
import mysql.connector
from tkinter import messagebox  # For showing messages in case of errors
from fpdf import FPDF
from pdf2image import convert_from_path
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from datetime import datetime  # Make sure this module is in the same directory or in your PYTHONPATH


class Report_Generater:
    def __init__(self, root, username):
        self.root = root
        self.username = username  # Assign username to the class instance
        self.root.geometry("1024x590+0+0")
        self.root.title("AttendNow")

        # ------------------------------------- Background Image ------------------------------------------------------
        background_img_main = Image.open(r"Image\Background.png")
        background_img_main = background_img_main.resize((1024, 590), Image.Resampling.LANCZOS)
        self.photo_background_img_main = ImageTk.PhotoImage(background_img_main)
        background_img_main_position = Label(self.root, image=self.photo_background_img_main)
        background_img_main_position.place(x=0, y=0, width=1024, height=590)
        # -------------------------------------------------------------------------------------------------------------

        # ------------------------------------- LogoTitle Image -------------------------------------------------------
        left_title = Image.open(r"Image\LogoTitle_Left Top.png")
        self.photoleft_title = ImageTk.PhotoImage(left_title)
        left_title_position = Label(self.root, image=self.photoleft_title)
        left_title_position.place(x=0, y=0, width=163, height=60)

        # Back Button
        back_button = Button(self.root, text="Back", command=self.back_to_main, bg="red", fg="white", font=("Arial", 12, "bold"))
        back_button.place(x=175, y=15, width=80, height=30)

        # Main Frame for Admin Interface
        main_frame2 = Frame(background_img_main_position, bd=2, bg="orange")
        main_frame2.place(x=300, y=5, width=400, height=50)

        # Main Title Label
        main_title = Label(main_frame2, text="Admin Interface", bg="orange", fg="white", font=("New Time Roman", 20, "bold"))
        main_title.place(x=5, y=2, width=400, height=40)

        # Display username on the top right corner
        self.username_label = Label(self.root, text=f"Logged in as: {username}", bg="orange", fg="white", font=("Arial", 12))
        self.username_label.place(x=800, y=15)
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------

        self.report_frame = Frame(self.root, bd=2, bg="orange")
        self.report_frame.place(x=490, y=70, width=500, height=500)

#------------------------------------------------------------------------------------------------------------------------------------------------------------------------

        # Left Frame for "Make Report"
        make_report_frame = LabelFrame(self.root, text="Report Form", bg="white", fg="black")
        make_report_frame.place(x=25, y=75, width=460, height=485)

#------------------------------------------------------------------------------------------------------------------------------------------------------------------------

        # Create a LabelFrame for "Student Information" inside the make_report_frame
        student_info_frame = LabelFrame(make_report_frame, text="Student Information", bg="white", fg="black")
        student_info_frame.place(x=5, y=5, width=450, height=100)  # Adjusted width to fit well inside make_report_frame

        # Label and Entry for Student ID
        student_id_label = Label(student_info_frame, text="Student ID:", bg="white", fg="black")
        student_id_label.place(x=10, y=10)  # Position for the label

        self.student_id_entry = Entry(student_info_frame, width=15)  # Adjusted width of the entry
        self.student_id_entry.place(x=100, y=10)  # Adjusted position to align with the label

        # Create the "Search ID" button
        search_button = Button(student_info_frame, text="Search ID", bg="orange", fg="white", width=10, command=self.search_student_info)  # Set width for uniformity
        search_button.place(x=270, y=10)  # Positioning the button to the right of the entry

        # Label to display the Student Name
        student_name_label = Label(student_info_frame, text="Student Found:", bg="white", fg="black")
        student_name_label.place(x=10, y=40)  # Position for the name label
        self.student_name_display = Label(student_info_frame, text="", bg="white", fg="black")  # Label to display name
        self.student_name_display.place(x=150, y=40)  # Position for the name display

#------------------------------------------------------------------------------------------------------------------------------------------------------------------------

        # LabelFrame for "Course" inside the make_report_frame, below the student_info_frame
        course_frame = LabelFrame(make_report_frame, text="Course", bg="white", fg="black")
        course_frame.place(x=5, y=110, width=450, height=190)  # Positioned below student_info_frame

        # Label and Combobox for Course Name
        course_name_label = Label(course_frame, text="Course Name:", bg="white", fg="black")
        course_name_label.place(x=10, y=10)

        # Assuming course_frame is defined elsewhere in your code
        self.course_name_combobox = ttk.Combobox(course_frame, values=[], width=37, state="readonly")
        self.course_name_combobox.place(x=150, y=10)
        self.course_name_combobox.set("Select Course")  # Set the default option to "Select Course"
        # Set the default option (index 0)

        # Label for "Course Selected:"
        selected_courses_label = Label(course_frame, text="Course Selected:", bg="white", fg="black")
        selected_courses_label.place(x=10, y=50)  # Position the label to the left of the Listbox

        # Listbox to display selected courses
        self.selected_courses_listbox = Listbox(course_frame, height=5, width=40)
        self.selected_courses_listbox.place(x=150, y=50)  # Positioning the Listbox

        # Button to delete selected course from the Listbox
        self.delete_course_button = Button(course_frame, text="Delete Selected Course", command=self.delete_selected_course)
        self.delete_course_button.place(x=150, y=135)  # 5 pixels gap from the Listbox

        # Bind the Combobox selection event to call add_course function
        self.course_name_combobox.bind("<<ComboboxSelected>>", lambda event: self.add_course())


#------------------------------------------------------------------------------------------------------------------------------------------------------------------------
       # LabelFrame for "Emotion Status" below the course_frame
        emotion_status_frame = LabelFrame(make_report_frame, text="Emotion Status", bg="white", fg="black")
        emotion_status_frame.place(x=5, y=305, width=450, height=100)  # Adjusted height to fit in a single row

        # Label for Month
        month_label = Label(emotion_status_frame, text="Select Month:", bg="white", fg="black")
        month_label.place(x=10, y=10)  # Positioning for Month label

        # Dropdown menu for Month using Combobox
        self.month_var = StringVar()
        self.month_var.set("Select Month")  # Default option
        months = [str(i) for i in range(1, 13)]  # List of months (1 to 12)
        month_dropdown = ttk.Combobox(emotion_status_frame, textvariable=self.month_var, values=months, width=13)
        month_dropdown.place(x=100, y=10)  # Positioning for Month dropdown

        # Label for Year
        year_label = Label(emotion_status_frame, text="Select Year:", bg="white", fg="black")
        year_label.place(x=220, y=10)  # Positioning for Year label

        # Dropdown menu for Year using Combobox
        self.year_var = StringVar()
        self.year_var.set("Select Year")  # Default option
        years = [str(i) for i in range(2020, 2031)]  # Example range of years (2020 to 2030)
        year_dropdown = ttk.Combobox(emotion_status_frame, textvariable=self.year_var, values=years,width=13)
        year_dropdown.place(x=300, y=10)  # Positioning for Year dropdown

        # Variables to hold the state of the checkboxes
        self.detail_var = BooleanVar()
        self.overall_var = BooleanVar()
        self.table_var = BooleanVar()

        # Checkbuttons for "Detail", "Overall", and "Table" in a horizontal order
        self.detail_checkbox = Checkbutton(emotion_status_frame, text="Chart (Detailed)", variable=self.detail_var, bg="white")
        self.detail_checkbox.place(x=20, y=40)

        self.overall_checkbox = Checkbutton(emotion_status_frame, text="Chart (Overall)", variable=self.overall_var, bg="white")
        self.overall_checkbox.place(x=150, y=40)

        self.table_checkbox = Checkbutton(emotion_status_frame, text="Status in Table", variable=self.table_var, bg="white")
        self.table_checkbox.place(x=280, y=40)

#------------------------------------------------------------------------------------------------------------------------------------------------------------------------
        # LabelFrame for "Report Generate" below the emotion_status_frame
        report_generate_frame = LabelFrame(make_report_frame, text="Report Generate", bg="white", fg="black")
        report_generate_frame.place(x=5, y=390, width=450, height=60)  # Positioned below emotion_status_frame

        display_label = Button(report_generate_frame, bg="orange", fg="white", text="Display Info", command=self.display_student_info)
        display_label.place(x=50, y=10, width=150)

        
        # Button for "Preview Report"
        generate_report_button = Button(report_generate_frame, text="Generate Report", bg="orange", fg="white", command=self.generate_report)
        generate_report_button.place(x=250, y=10, width=150)

        
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------

       # Right Frame for PDF report preview
        self.preview_frame = Frame(self.report_frame, bg="white", bd=2)
        self.preview_frame.place(x=5, y=5, width=460, height=490)

        # Create a Canvas for the scrollable area
        self.canvas = Canvas(self.preview_frame, bg="white")
        self.canvas.pack(side="left", fill="both", expand=True)

        # Create a Scrollbar and link it to the Canvas
        self.scrollbar = Scrollbar(self.preview_frame, orient="vertical", command=self.canvas.yview)
        self.scrollbar.pack(side="right", fill="y")

        # Configure the canvas to use the scrollbar
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        # Create a frame to hold the content inside the Canvas
        self.content_frame = Frame(self.canvas, bg="white")
        self.canvas.create_window((0, 0), window=self.content_frame, anchor="nw")

        self.content_frame.bind("<Configure>", self.update_scroll_region)


       

       

#------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    def fetch_attendance_data(self, student_id, course):
        connection = mysql.connector.connect(
            host='localhost',
            user='root',
            password='Nightcore_1134372019!',
            database='attendnow'
        )
        
        cursor = connection.cursor()
        query = """
            SELECT date, attendance_status, course_hour 
            FROM attendance_status 
            WHERE student_id = %s AND course = %s 
            ORDER BY date
        """
        cursor.execute(query, (student_id, course))
        
        # Fetch all rows of the result
        attendance_data = cursor.fetchall()
        cursor.close()
        connection.close()
        
        return attendance_data


    def generate_report(self):
        # Fetch student ID and name from the entry and label
        student_id = self.student_id_entry.get()
        student_name = self.student_name_display.cget("text")  # Get text from the label

        # Check if student ID is empty
        if not student_id:
            messagebox.showwarning("Input Error", "Please enter a Student ID.")
            return  # Exit the function if ID is empty

        # Fetch the list of selected courses from the listbox
        selected_courses = self.selected_courses_listbox.get(0, 'end')  # Get all selected courses as a tuple

        # Print the values to the terminal
        print("Student ID:", student_id)
        print("Student Name:", student_name)
        print("Selected Courses:")
        for course in selected_courses:
            print("-", course)

        # Check which checkboxes are ticked and print their statuses
        print("\nSelected Options:")
        if self.detail_var.get():
            print("- Chart (Detailed) is ticked.")
        else:
            print("- Chart (Detailed) is not ticked.")
        
        if self.overall_var.get():
            print("- Chart (Overall) is ticked.")
        else:
            print("- Chart (Overall) is not ticked.")
        
        if self.table_var.get():
            print("- Status in Table is ticked.")
        else:
            print("- Status in Table is not ticked.")


    def display_student_info(self):
        # Clear previous content in the content_frame
        for widget in self.content_frame.winfo_children():
            widget.destroy()

        # Fetch student ID and name from the entry and label
        student_id = self.student_id_entry.get()
        student_name = self.student_name_display.cget("text")

        # Check if student ID is empty
        if not student_id:
            messagebox.showwarning("Input Error", "Please enter a Student ID.")
            return  # Exit the function if ID is empty

        # Add the title label for the report and center it
        Label(self.content_frame, text="Report Form", bg="white", fg="black", font=("Arial", 16, "bold")).pack(padx=10, pady=(10, 5), anchor="center", fill="x")

        # Create a single label to display the name and ID on one line
        Label(self.content_frame, text="Name: " + student_name + " | ID: " + student_id, bg="white", fg="black").pack(anchor="w", padx=10, pady=5)

        # Display selected courses
        Label(self.content_frame, text="Courses Attendance:", bg="white", fg="black").pack(anchor="w", padx=10, pady=5)
        selected_courses = self.selected_courses_listbox.get(0, 'end')

        for course in selected_courses:
            Label(self.content_frame, text="- " + course, bg="white", fg="black").pack(anchor="w", padx=20)

            # Fetch attendance data for the specific course
            attendance_data = self.fetch_attendance_data(student_id, course)

            # Create a frame for the table
            table_frame = Frame(self.content_frame, bg="white")
            table_frame.pack(padx=10, pady=(5, 10), fill="x")  # Add some padding and fill horizontally

            # Create table header
            Label(table_frame, text="Date" + "                 " + "Hour" + "                 "+ "Status", bg="white", fg="black").pack(anchor="w",padx=5)
           
            # Populate the table with attendance data
            for date, attendance_status, course_hour in attendance_data:
                status_mark = ''
                if attendance_status == "Present":
                    status_mark = "P"
                elif attendance_status == "Absent":
                    status_mark = "A"
                elif attendance_status == "Half-Absent":
                    status_mark = "P/A"

                # Create a new frame for each row of data
                row_frame = Frame(table_frame, bg="white")
                row_frame.pack(side="top", fill="x")  # Stack rows vertically
                
                Label(row_frame, text=date, bg="white", fg="black").pack(side="left", padx=5)
                Label(row_frame, text=course_hour, bg="white", fg="black").pack(side="left", padx=5)  # Display course_hour
                Label(row_frame, text=status_mark, bg="white", fg="black").pack(side="left", padx=5)

        # Check which checkboxes are ticked and display their statuses
        Label(self.content_frame, text="Emotion Status:", bg="white", fg="black").pack(anchor="w", padx=10, pady=5)
        
        if self.detail_var.get():
            Label(self.content_frame, text="- Chart (Detailed) is ticked.", bg="white", fg="black").pack(anchor="w", padx=10)
        else:
            Label(self.content_frame, text="- Chart (Detailed) is not ticked.", bg="white", fg="black").pack(anchor="w", padx=10)

        if self.overall_var.get():
            Label(self.content_frame, text="- Chart (Overall) is ticked.", bg="white", fg="black").pack(anchor="w", padx=10)
        else:
            Label(self.content_frame, text="- Chart (Overall) is not ticked.", bg="white", fg="black").pack(anchor="w", padx=10)

        if self.table_var.get():
            Label(self.content_frame, text="- Status in Table is ticked.", bg="white", fg="black").pack(anchor="w", padx=10)
        else:
            Label(self.content_frame, text="- Status in Table is not ticked.", bg="white", fg="black").pack(anchor="w", padx=10)

        # Update scroll region to encompass all items
        self.update_scroll_region()



    def update_scroll_region(self, event=None):
        # Update the scroll region of the canvas
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        
        
    
    
    def search_student_info(self):
        student_id = self.student_id_entry.get()  # Get the Student ID from the entry

        # Clear previous selections in the Combobox
        self.course_name_combobox.set("")  # Clear the Combobox display
        self.student_name_display.config(text="")  # Clear previous student name display

        # Connect to the MySQL database
        try:
            connection = mysql.connector.connect(
                host='localhost',  # Update with your host
                user='root',       # Update with your MySQL username
                password='Nightcore_1134372019!',  # Update with your MySQL password
                database='attendnow'  # The database name
            )

            cursor = connection.cursor()

            # SQL query to fetch the student name based on the student ID
            query_name = "SELECT student_name FROM students WHERE student_id = %s LIMIT 1"  # Get the student name
            cursor.execute(query_name, (student_id,))
            
            # Fetch the student name result
            student_name_result = cursor.fetchone()

            if student_name_result:  # If a result is found
                student_name = student_name_result[0]  # Get the student name
                self.student_name_display.config(text=student_name)  # Update the label with the name
            else:
                self.student_name_display.config(text="Not Found")  # Update label if no student found

            # SQL query to fetch the courses based on the student ID
            query_courses = "SELECT course FROM students WHERE student_id = %s"  # Get all courses for the student
            cursor.execute(query_courses, (student_id,))
            
            # Fetch all results for courses
            course_results = cursor.fetchall()

            # Create a list to hold course names
            course_names = []

            if course_results:  # If results are found
                for row in course_results:
                    course = row[0]  # Get the course name from the result
                    course_names.append(course)  # Add the course to the list

            # Update the Combobox with the list of courses
            self.course_name_combobox['values'] = course_names  # Set the new list of courses
            if course_names:  # If there are courses, set the first one as default
                self.course_name_combobox.current(0)

            else:
                self.course_name_combobox['values'] = []  # Clear values if no courses found

        except mysql.connector.Error as err:
            # Show an error message if something goes wrong
            messagebox.showerror("Database Error", f"Error: {err}")
        finally:
            # Close the cursor and connection
            cursor.close()
            connection.close()


    def delete_selected_course(self):
        # Get the currently selected item index
        selected_index = self.selected_courses_listbox.curselection()

        if selected_index:  # Check if an item is selected
            self.selected_courses_listbox.delete(selected_index)  # Delete the selected item
        else:
            messagebox.showwarning("Selection Error", "Please select a course to delete.")  # Warn if nothing is selected


    # Define the add_course method within the class
    def add_course(self):
        selected_course = self.course_name_combobox.get()  # Get the selected course from Combobox
        if selected_course not in self.selected_courses_listbox.get(0, END):  # Check if the course is not already added
            self.selected_courses_listbox.insert(END, selected_course)  # Add the selected course to the Listbox

    def back_to_main(self):
        self.root.destroy()  # Close the current window
        new_window = Tk()  # Create a new Tk window for the admit interface
        admit_interface.Admit_Interface(new_window, self.username)


# Example usage
if __name__ == "__main__":
    root = tk.Tk()
    report_generator = Report_Generater(root, "AdminUser")
    root.mainloop()
