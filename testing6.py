import tkinter as tk
from tkinter import ttk, Listbox
from tkinter import LabelFrame, Label, Entry, Button, StringVar
from tkinter import *
from PIL import Image, ImageTk
import mysql.connector
from tkinter import messagebox  # For showing messages in case of errors
from fpdf import FPDF
from pdf2image import convert_from_path


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

        # Report Frame
        report_frame = Frame(self.root, bd=2, bg="orange")
        report_frame.place(x=20, y=70, width=980, height=500)

        # Left Frame for "Make Report"
        make_report_frame = LabelFrame(report_frame, text="Report Form", bg="white", fg="black")
        make_report_frame.place(x=5, y=5, width=460, height=485)

        # Student Information Frame
        student_info_frame = LabelFrame(make_report_frame, text="Student Information", bg="white", fg="black")
        student_info_frame.place(x=5, y=5, width=450, height=100)

        # Student ID Entry
        student_id_label = Label(student_info_frame, text="Student ID:", bg="white", fg="black")
        student_id_label.place(x=10, y=10)

        self.student_id_entry = Entry(student_info_frame, width=15)
        self.student_id_entry.place(x=100, y=10)

        # Search Button
        search_button = Button(student_info_frame, text="Search ID", bg="orange", fg="white", width=10, command=self.search_student_info)
        search_button.place(x=270, y=10)

        # Display Student Name
        student_name_label = Label(student_info_frame, text="Student Found:", bg="white", fg="black")
        student_name_label.place(x=10, y=40)
        self.student_name_display = Label(student_info_frame, text="", bg="white", fg="black")
        self.student_name_display.place(x=150, y=40)

        # Course Frame
        course_frame = LabelFrame(make_report_frame, text="Course", bg="white", fg="black")
        course_frame.place(x=5, y=110, width=450, height=190)

        # Course Name Combobox
        course_name_label = Label(course_frame, text="Course Name:", bg="white", fg="black")
        course_name_label.place(x=10, y=10)

        self.course_name_combobox = ttk.Combobox(course_frame, values=[], width=37, state="readonly")
        self.course_name_combobox.place(x=150, y=10)
        self.course_name_combobox.set("Select Course")

        # Listbox for Selected Courses
        selected_courses_label = Label(course_frame, text="Course Selected:", bg="white", fg="black")
        selected_courses_label.place(x=10, y=50)
        self.selected_courses_listbox = Listbox(course_frame, height=5, width=40)
        self.selected_courses_listbox.place(x=150, y=50)

        # Delete Selected Course Button
        self.delete_course_button = Button(course_frame, text="Delete Selected Course", command=self.delete_selected_course)
        self.delete_course_button.place(x=150, y=135)

        # Bind Combobox Selection
        self.course_name_combobox.bind("<<ComboboxSelected>>", lambda event: self.add_course())

        # Emotion Status Frame
        emotion_status_frame = LabelFrame(make_report_frame, text="Emotion Status", bg="white", fg="black")
        emotion_status_frame.place(x=5, y=305, width=450, height=80)

        # Emotion Checkbuttons
        self.detail_var = BooleanVar()
        self.overall_var = BooleanVar()
        self.table_var = BooleanVar()

        self.detail_checkbox = Checkbutton(emotion_status_frame, text="Chart (Detailed)", variable=self.detail_var, bg="white")
        self.detail_checkbox.place(x=20, y=10)

        self.overall_checkbox = Checkbutton(emotion_status_frame, text="Chart (Overall)", variable=self.overall_var, bg="white")
        self.overall_checkbox.place(x=150, y=10)

        self.table_checkbox = Checkbutton(emotion_status_frame, text="Status in Table", variable=self.table_var, bg="white")
        self.table_checkbox.place(x=280, y=10)

        # Report Generate Frame
        report_generate_frame = LabelFrame(make_report_frame, text="Report Generate", bg="white", fg="black")
        report_generate_frame.place(x=5, y=390, width=450, height=60)

        # Report Preview Button
        display_label = Button(report_generate_frame, text="Report Preview", bg="orange", fg="white", command=self.display_title)
        display_label.place(x=50, y=10, width=150)

        # Generate Report Button
        generate_report_button = Button(report_generate_frame, text="Generate Report", bg="orange", fg="white", command=self.generate_pdf)
        generate_report_button.place(x=250, y=10, width=150)

        # Right Frame for PDF Preview
        preview_frame = Frame(report_frame, bg="white", bd=2)
        preview_frame.place(x=500, y=10, width=460, height=430)

        # Title Label for PDF Preview
        self.title_label = Label(preview_frame, text="", bg="white", fg="black", font=("Arial", 16, "bold"))
        self.title_label.place(x=150, y=10)

        # Name Label for PDF Preview
        self.name_label = Label(preview_frame, text="", bg="white", fg="black", font=("Arial", 16, "bold"))
        self.name_label.place(x=150, y=50)  # Adjusted to avoid overlap with title_label

    def display_title(self):
        self.title_label.config(text="Hello World")  # Update the title label to "Hello World"
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
        pdf_preview_label = Label(self.root)  # Create a new label for preview
        pdf_preview_label.config(image=image_tk)
        pdf_preview_label.image = image_tk  # Keep a reference to avoid garbage collection
        pdf_preview_label.place(x=500, y=10)  # Adjust position as necessary

    def search_student_info(self):
        student_id = self.student_id_entry.get()  # Get the Student ID from the entry

        # Clear previous selections in the Combobox
        self.course_name_combobox.set("Select Course")
        self.selected_courses_listbox.delete(0, tk.END)  # Clear previous selections in Listbox
        self.student_name_display.config(text="")  # Clear previous name display

        # Connect to the database to retrieve student info
        try:
            connection = mysql.connector.connect(
                host="localhost",
                user="root",
                password="Nightcore_1134372019!",
                database="attendnow"
            )
            cursor = connection.cursor()
            query = "SELECT student_name FROM students WHERE student_id = %s"
            cursor.execute(query, (student_id,))
            result = cursor.fetchone()

            if result:
                self.student_name_display.config(text=result[0])  # Display student name
                self.load_courses(student_id)  # Load courses for this student
            else:
                messagebox.showerror("Error", "Student ID not found.")

            cursor.close()
            connection.close()

        except mysql.connector.Error as e:
            messagebox.showerror("Database Error", str(e))

    def load_courses(self, student_id):
        # Load courses for the student
        try:
            connection = mysql.connector.connect(
                host="localhost",
                user="root",
                password="Nightcore_1134372019!",
                database="attendnow"
            )
            cursor = connection.cursor()
            query = "SELECT course FROM students WHERE student_id = %s"  # Adjust according to your table structure
            cursor.execute(query, (student_id,))
            courses = cursor.fetchall()

            # Clear previous course entries
            self.course_name_combobox['values'] = []
            self.selected_courses_listbox.delete(0, tk.END)

            # Add fetched courses to the Combobox and Listbox
            for course in courses:
                self.course_name_combobox['values'] += course  # Add to Combobox
                self.selected_courses_listbox.insert(tk.END, course[0])  # Add to Listbox

            cursor.close()
            connection.close()

        except mysql.connector.Error as e:
            messagebox.showerror("Database Error", str(e))

    def add_course(self):
        # Add selected course to the Listbox
        selected_course = self.course_name_combobox.get()
        if selected_course and selected_course not in self.selected_courses_listbox.get(0, tk.END):
            self.selected_courses_listbox.insert(tk.END, selected_course)

    def delete_selected_course(self):
        # Delete the selected course from the Listbox
        selected_index = self.selected_courses_listbox.curselection()
        if selected_index:
            self.selected_courses_listbox.delete(selected_index)

    def back_to_main(self):
        self.root.destroy()  # Close the current window


if __name__ == "__main__":
    root = tk.Tk()
    username = "Admin"  # Example username
    app = Report_Generater(root, username)
    root.mainloop()
