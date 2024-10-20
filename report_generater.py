import tkinter as tk
from tkinter import ttk, Listbox
from tkinter import LabelFrame, Label, Entry, Button, StringVar
from tkinter import *
from PIL import Image, ImageTk
import admit_interface
import mysql.connector
from tkinter import messagebox  # For showing messages in case of errors
from tkinter import *
from fpdf import FPDF
from pdf2image import convert_from_path
from PIL import Image, ImageTk


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

        report_frame = Frame(self.root, bd=2, bg="orange")
        report_frame.place(x=20, y=70, width=980, height=500)

#------------------------------------------------------------------------------------------------------------------------------------------------------------------------

        # Left Frame for "Make Report"
        make_report_frame = LabelFrame(report_frame, text="Report Form", bg="white", fg="black")
        make_report_frame.place(x=5, y=5, width=460, height=485)

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
        emotion_status_frame.place(x=5, y=305, width=450, height=80)  # Positioned below course_frame

        # Variables to hold the state of the checkboxes
        self.detail_var = BooleanVar()
        self.overall_var = BooleanVar()
        self.table_var = BooleanVar()

        # Checkbuttons for "Detail", "Overall", and "Table" in a horizontal order
        self.detail_checkbox = Checkbutton(emotion_status_frame, text="Chart (Detailed)", variable=self.detail_var, bg="white")
        self.detail_checkbox.place(x=20, y=10)

        self.overall_checkbox = Checkbutton(emotion_status_frame, text="Chart (Overall)", variable=self.overall_var, bg="white")
        self.overall_checkbox.place(x=150, y=10)

        self.table_checkbox = Checkbutton(emotion_status_frame, text="Status in Table", variable=self.table_var, bg="white")
        self.table_checkbox.place(x=280, y=10)

#------------------------------------------------------------------------------------------------------------------------------------------------------------------------
        # LabelFrame for "Report Generate" below the emotion_status_frame
        report_generate_frame = LabelFrame(make_report_frame, text="Report Generate", bg="white", fg="black")
        report_generate_frame.place(x=5, y=390, width=450, height=60)  # Positioned below emotion_status_frame

        # Placeholder for PDF preview in the right frame
        display_label = Button(report_generate_frame, text="Report Preview", bg="orange", fg="white", command=self.display_title)
        display_label.place(x=50, y=10, width=150)
        
        # Button for "Preview Report"
        generate_report_button = Button(report_generate_frame, text="Generate Report", bg="orange", fg="white", command=self.generate_pdf)
        generate_report_button.place(x=250, y=10, width=150)

        
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------

        # Right Frame for PDF report preview
        preview_frame = Frame(report_frame, bg="white", bd=2)
        preview_frame.place(x=500, y=10, width=460, height=490)

        # Label for the title
        self.title_label = Label(preview_frame, text="", bg="white", fg="black")
        self.title_label.place(x=150, y=5)
        # Label for the title
        self.name_label = Label(preview_frame, text="", bg="white", fg="black" )
        self.name_label.place(x=10, y=20)

       

#------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    # Function to display "Hello World" as a header
    def display_title(self):
        self.title_label.config(text="Report Form")  # Update the title label to "Hello World"
        self.name_label.config(text=f"Name: {self.student_name_display.cget('text')}")  # Fix the syntax issue here
    

    def generate_pdf(self):
        # Create the PDF with 'Hello World'
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)
        pdf.cell(200, 10, txt="Hello World", ln=True, align='C')
        pdf_output_path = "hello_world.pdf"
        pdf.output(pdf_output_path)

        # Convert the first page of the PDF to an image
        images = convert_from_path(pdf_output_path, first_page=0, last_page=1)
        image = images[0]
        
        # Resize image to fit the preview frame
        image = image.resize((460, 430), Image.ANTIALIAS)
        image_tk = ImageTk.PhotoImage(image)
        
        # Display the image in the label
        pdf_preview_label.config(image=image_tk)
        pdf_preview_label.image = image_tk  # Keep a reference to avoid garbage collection
    
    
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
    app = Report_Generater(root, "AdminUser")
    root.mainloop()
