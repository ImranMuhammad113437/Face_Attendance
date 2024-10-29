import tkinter as tk
from tkinter import ttk, Listbox
from tkinter import Frame, Canvas, Scrollbar, Label, messagebox, StringVar, BooleanVar, Entry, Listbox
from tkinter import LabelFrame, Label, Entry, Button, StringVar
from tkinter import *
from PIL import Image, ImageTk
import teacher_interface
import mysql.connector  # Import your database library
from tkinter import Label, Frame, messagebox  # Ensure required Tkinter classes are imported
import mysql.connector
from tkinter import messagebox  # For showing messages in case of errors
from fpdf import FPDF
from pdf2image import convert_from_path
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from datetime import datetime  # Make sure this module is in the same directory or in your PYTHONPATH
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import calendar
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
import os
from tkinter import Frame, Label, Tk
from PIL import Image, ImageDraw, ImageFont, ImageTk
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import inch
from reportlab.lib.colors import gray
from reportlab.pdfgen import canvas


class Report_Generater_Interface_Teacher:
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
        main_title = Label(main_frame2, text="Teacher Interface", bg="orange", fg="white", font=("New Time Roman", 20, "bold"))
        main_title.place(x=5, y=2, width=400, height=40)

        # Display username on the top right corner
        self.username_label = Label(self.root, text=f"Logged in as: {username}", bg="orange", fg="white", font=("Arial", 12))
        self.username_label.place(x=800, y=15)
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------

        self.report_frame = Frame(self.root, bd=2, bg="orange")
        self.report_frame.place(x=450, y=70, width=560, height=510)

#------------------------------------------------------------------------------------------------------------------------------------------------------------------------

        # Left Frame for "Make Report"
        make_report_frame = LabelFrame(self.root, text="Report Form", bg="white", fg="black")
        make_report_frame.place(x=25, y=75, width=420, height=485)

#------------------------------------------------------------------------------------------------------------------------------------------------------------------------

        # Create a LabelFrame for "Student Information" inside the make_report_frame
        student_info_frame = LabelFrame(make_report_frame, text="Student Information", bg="white", fg="black")
        student_info_frame.place(x=5, y=5, width=405, height=100)  # Adjusted width to fit well inside make_report_frame

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
         # Create a LabelFrame for "Student Information" inside the make_report_frame
        date_info_frame = LabelFrame(make_report_frame, text="Month / Year", bg="white", fg="black")
        date_info_frame.place(x=5, y=110, width=405, height=50)

        # Label for Month
        month_label = Label(date_info_frame, text="Select Month:", bg="white", fg="black")
        month_label.place(x=10, y=5)  # Positioning for Month label

        # Dropdown menu for Month using Combobox
        self.month_var = StringVar()
        self.month_var.set("Select Month")  # Default option
        months = [str(i) for i in range(1, 13)]  # List of months (1 to 12)
        month_dropdown = ttk.Combobox(date_info_frame, textvariable=self.month_var, values=months, width=13)
        month_dropdown.place(x=100, y=5)  # Positioning for Month dropdown

        # Label for Year
        year_label = Label(date_info_frame, text="Select Year:", bg="white", fg="black")
        year_label.place(x=220, y=5)  # Positioning for Year label

        # Dropdown menu for Year using Combobox
        self.year_var = StringVar()
        self.year_var.set("Select Year")  # Default option
        years = [str(i) for i in range(2020, 2031)]  # Example range of years (2020 to 2030)
        year_dropdown = ttk.Combobox(date_info_frame, textvariable=self.year_var, values=years,width=13)
        year_dropdown.place(x=300, y=5)  # Positioning for Year dropdown


#------------------------------------------------------------------------------------------------------------------------------------------------------------------------

        # LabelFrame for "Course" inside the make_report_frame, below the student_info_frame
        course_frame = LabelFrame(make_report_frame, text="Course", bg="white", fg="black")
        course_frame.place(x=5, y=160, width=405, height=190)  # Positioned below student_info_frame

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
        selected_courses_label.place(x=10, y=45)  # Position the label to the left of the Listbox

        # Listbox to display selected courses
        self.selected_courses_listbox = Listbox(course_frame, height=5, width=40)
        self.selected_courses_listbox.place(x=150, y=45)  # Positioning the Listbox

        # Button to delete selected course from the Listbox
        self.delete_course_button = Button(course_frame, text="Delete Selected Course", command=self.delete_selected_course)
        self.delete_course_button.place(x=150, y=135)  # 5 pixels gap from the Listbox

        # Bind the Combobox selection event to call add_course function
        self.course_name_combobox.bind("<<ComboboxSelected>>", lambda event: self.add_course())


#------------------------------------------------------------------------------------------------------------------------------------------------------------------------
       # LabelFrame for "Emotion Status" below the course_frame
        emotion_status_frame = LabelFrame(make_report_frame, text="Emotion Status", bg="white", fg="black")
        emotion_status_frame.place(x=5, y=350, width=405, height=50)  # Adjusted height to fit in a single row

        # Variables to hold the state of the checkboxes
        self.detail_var = BooleanVar()
        self.overall_var = BooleanVar()
        self.table_var = BooleanVar()

        # Checkbuttons for "Detail", "Overall", and "Table" in a horizontal order
        self.detail_checkbox = Checkbutton(emotion_status_frame, text="Chart (Detailed)", variable=self.detail_var, bg="white")
        self.detail_checkbox.place(x=20, y=3)

        self.overall_checkbox = Checkbutton(emotion_status_frame, text="Chart (Overall)", variable=self.overall_var, bg="white")
        self.overall_checkbox.place(x=150, y=3)

        self.table_checkbox = Checkbutton(emotion_status_frame, text="Status in Table", variable=self.table_var, bg="white")
        self.table_checkbox.place(x=280, y=3)

#------------------------------------------------------------------------------------------------------------------------------------------------------------------------
        # LabelFrame for "Report Generate" below the emotion_status_frame
        report_generate_frame = LabelFrame(make_report_frame, text="Report Generate", bg="white", fg="black")
        report_generate_frame.place(x=5, y=400, width=405, height=60)  # Positioned below emotion_status_frame

        display_label = Button(report_generate_frame, bg="orange", fg="white", text="Display Info", command=self.display_student_info)
        display_label.place(x=50, y=10, width=150)

        
        # Button for "Preview Report"
        generate_report_button = Button(report_generate_frame, text="Generate Report", bg="orange", fg="white", command=self.generate_report)
        generate_report_button.place(x=250, y=10, width=150)

        
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------

      # Right Frame for PDF report preview
        self.preview_frame = Frame(self.report_frame, bg="white", bd=2)  # Set background to white
        self.preview_frame.place(x=5, y=5, width=550, height=490)

        # Create a Canvas for the scrollable area
        self.canvas = Canvas(self.preview_frame, bg="white")  # Set canvas background to white
        self.canvas.pack(side="left", fill="both", expand=True)

        # Create a frame to hold the content inside the Canvas
        self.content_frame = Frame(self.canvas, bg="white")  # Set content frame background to white
        self.canvas.create_window((0, 0), window=self.content_frame, anchor="nw")

        # Create vertical Scrollbar and link it to the Canvas
        self.y_scrollbar = Scrollbar(self.preview_frame, orient="vertical", command=self.canvas.yview)
        self.y_scrollbar.pack(side="right", fill="y")

        # Configure the canvas to use the vertical scrollbar only
        self.canvas.configure(yscrollcommand=self.y_scrollbar.set)  # Updated to link yscrollbar only

        # Bind the content frame size to update the scroll region
        self.content_frame.bind("<Configure>", self.update_scroll_region)




        

        




       

       

#------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    # Function to update the scroll region
    def update_scroll_region(self, event):
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))  # Update the scroll region to encompass the content_frame

    def fetch_attendance_data_report(self, student_id, course, month, year):
            connection = mysql.connector.connect(
                host='localhost',
                user='root',
                password='Nightcore_1134372019!',
                database='attendnow'
            )
            
            cursor = connection.cursor()
            
            # Modified SQL query to filter by student_id, course, month, and year
            query = """
                SELECT date, course_hour , attendance_status
                FROM attendance_status 
                WHERE student_id = %s 
                AND course = %s 
                AND YEAR(date) = %s 
                AND MONTH(date) = %s
                ORDER BY date
            """
            
            # Execute query with student_id, course, year, and month as parameters
            cursor.execute(query, (student_id, course, year, month))
            
            # Fetch all rows of the result
            attendance_data = cursor.fetchall()
            cursor.close()
            connection.close()
            
            return attendance_data


    def fetch_attendance_data(self, student_id, course, month, year):
        connection = mysql.connector.connect(
            host='localhost',
            user='root',
            password='Nightcore_1134372019!',
            database='attendnow'
        )
        
        cursor = connection.cursor()
        
        # Modified SQL query to filter by student_id, course, month, and year
        query = """
            SELECT date, attendance_status, course_hour 
            FROM attendance_status 
            WHERE student_id = %s 
            AND course = %s 
            AND YEAR(date) = %s 
            AND MONTH(date) = %s
            ORDER BY date
        """
        
        # Execute query with student_id, course, year, and month as parameters
        cursor.execute(query, (student_id, course, year, month))
        
        # Fetch all rows of the result
        attendance_data = cursor.fetchall()
        cursor.close()
        connection.close()
        
        return attendance_data

    def generate_report(self):
        # Fetch student ID and name from the entry and label
        student_id = self.student_id_entry.get()
        student_name = self.student_name_display.cget("text")  # Get text from the label
        selected_month = self.month_var.get()  # Fetch selected month
        selected_year = self.year_var.get()
        # Initialize the variable to hold the month text
        selected_month_text = ""

        # Check the value of selected_month and set the corresponding month name
        if selected_month == "1":
            selected_month_text = " January"
        elif selected_month == "2":
            selected_month_text = " February"
        elif selected_month == "3":
            selected_month_text = " March"
        elif selected_month == "4":
            selected_month_text = " April"
        elif selected_month == "5":
            selected_month_text = " May"
        elif selected_month == "6":
            selected_month_text = " June"
        elif selected_month == "7":
            selected_month_text = " July"
        elif selected_month == "8":
            selected_month_text = " August"
        elif selected_month == "9":
            selected_month_text = " September"
        elif selected_month == "10":
            selected_month_text = " October"
        elif selected_month == "11":
            selected_month_text = " November"
        elif selected_month == "12":
            selected_month_text = " December"
        else:
            selected_month_text = "Invalid month"  # Handle invalid month if necessary

        # Now selected_month_text holds the corresponding month name

        # Check if student ID is empty
        if not student_id:
            messagebox.showwarning("Input Error", "Please enter a Student ID.")
            return  # Exit the function if ID is empty

        # Register the Arial font
        pdfmetrics.registerFont(TTFont('Arial', 'Arial.ttf'))  # Ensure you have Arial.ttf in the same directory

        # Create a PDF canvas
        c = canvas.Canvas(student_name + ".pdf", pagesize=letter)

        # Set title properties
        title = "Report Form"
        font_name = "Arial"  # Use registered Arial font
        font_size = 16

        # Set font and color for the title
        c.setFont(font_name, font_size)
        c.setFillColor(colors.black)

        # Calculate width and height for centering the title
        width = c._pagesize[0]
        text_width = c.stringWidth(title, font_name, font_size)

        # Draw the title at the center of the page
        c.drawString((width - text_width) / 2, 10 * inch, title)  # Adjust the Y-coordinate as needed

        # Set font and color for table
        table_font_size = 12
        c.setFont(font_name, table_font_size)

        # Define table data
        table_data = [
            ["Name: " + student_name, "ID: " + student_id],
            ["Month: " + selected_month_text, "Year: " + selected_year]
        ]

        # Define padding for the table
        padding = 0.5 * inch  # Add a padding of 0.5 inches from both sides

        # Calculate cell dimensions
        available_width = width - (2 * padding)  # Reduce total width by padding on both sides
        cell_width = available_width / 2  # Divide the available width for 2 columns
        cell_height = (0.5 * inch) - 10  # Height for each row with vertical padding

        # Position for the table, just below the title
        table_start_y = (10 * inch) - (cell_height + 0.1 * inch)  # Positioning it below the title

        # Draw the table without borders
        for row_index, row in enumerate(table_data):
            for col_index, text in enumerate(row):
                x = padding + col_index * cell_width  # Calculate X position with padding
                y = table_start_y - (row_index * cell_height)  # Calculate Y position for the table

                # Draw the text in each cell with X-padding of 0.2 inches and adjust for vertical padding
                c.drawString(x + 0.2 * inch, y + 0.1 * inch, text)  # Slight offset for vertical padding

        #------------------------------------------------------------------------------------------------------------------------------------------------------------------------

        # Now add the title below the table
        # Set font size for the title below the table
        title_below_font_size = 14
        c.setFont(font_name, title_below_font_size)

        # Set the text for the title below the table
        title_below = "Attendance Status"

        # Calculate Y position for the title (add some padding after the table)
        title_below_y = y - cell_height - 0.3 * inch  # 0.3 inch padding after the table

        # Center the title below the table
        text_width = c.stringWidth(title_below, font_name, title_below_font_size)
        c.drawString((width - text_width) / 2, title_below_y, title_below)

        #------------------------------------------------------------------------------------------------------------------------------------------------------------------------

        # Fetch the list of selected courses from the listbox
        selected_courses = self.selected_courses_listbox.get(0, 'end')  # Get all selected courses as a tuple

        # Set the starting Y position for printing courses, just below the title
        course_start_y = title_below_y - 0.5 * inch  # Add some space after the title

        # Set font size for the courses
        course_font_size = 12
        c.setFont(font_name, course_font_size)
    
        # Define table headers for each course
        # Set page dimensions and margins
        page_width, page_height = A4
        left_margin = 0.5 * inch
        right_margin = 0.5 * inch
        available_width = page_width - left_margin - right_margin
        course_start_y = page_height - 1 * inch  # Starting Y position at the top of the page

        # Define table headers for each course
        headers = ["Date", "Hour", "Status"]
        num_columns = 3  # Date, Hour, Status columns
        column_width = available_width / num_columns  # Calculate column width

        # Font settings for title and table text
        font_name = "Helvetica"
        title_below_font_size = 14
        table_header_font_size = 10
        table_data_font_size = 10

        # Title text
        title_below = "Attendance Status"

        # Iterate through each selected course
        for index, course in enumerate(selected_courses):
            # Decrease Y position for each course (adjust for spacing between tables)
            course_y = course_start_y - (index * 2 * inch)  # Adjust spacing between courses

            # Print course name as a title
            c.setFont("Helvetica-Bold", 12)
            c.drawString(left_margin, course_y, f"Course: {course}")

            # Fetch the attendance data for the current course
            attendance_data = self.fetch_attendance_data_report(student_id, course, selected_month, selected_year)

            # Table Headers
            headers = ["Date", "Hour", "Status"]
            left_margin = 0.5 * inch
            column_width = 2 * inch
            table_start_y = height - 150

            c.setFont("Helvetica-Bold", 12)
            for col_index, header in enumerate(headers):
                header_x = left_margin + col_index * column_width
                c.drawString(header_x, table_start_y, header)

            # Table Rows
            row_height = 0.4 * inch
            c.setFont("Helvetica", 10)
            for data_index, data in enumerate(attendance_data):
                data_y = table_start_y - ((data_index + 1) * row_height)
                for col_index, value in enumerate(data):
                    data_x = left_margin + col_index * column_width
                    c.drawString(data_x, data_y, str(value))

            c.save()


        # Iterate through each selected course and print it on the PDF    
        #------------------------------------------------------------------------------------------------------------------------------------------------------------------------

        # Finalize the PDF
        c.save()

        print(f"PDF saved as {student_name}.pdf")


    def create_rotated_image(self,text, angle, font):
        # Calculate text size using textbbox
        bbox = font.getbbox(text)
        text_width = bbox[2] - bbox[0]  # width
        text_height = bbox[3] - bbox[1]  # height
        
        # Create an image with a transparent background, sized to fit the text
        img = Image.new('RGBA', (text_width + 10, text_height + 10), (255, 255, 255, 0))  # Add padding
        d = ImageDraw.Draw(img)
        
        # Calculate position to center text
        text_x = (img.width - text_width) / 2
        text_y = (img.height - text_height) / 2
        
        # Draw the text
        d.text((text_x, text_y), text, fill=(0, 0, 0), font=font)
        
        # Rotate the image
        img = img.rotate(angle, expand=1)
        
        # Convert the image to PhotoImage
        img = img.convert("RGBA")  # Ensure it's in RGBA mode
        img_tk = ImageTk.PhotoImage(img)  # Create a PhotoImage
        return img_tk


    def display_student_info(self):
        # Clear previous content in the content_frame
        for widget in self.content_frame.winfo_children():
            widget.destroy()

        # Fetch student ID, name, month, and year
        student_id = self.student_id_entry.get()
        student_name = self.student_name_display.cget("text")
        selected_month = self.month_var.get()  # Fetch selected month
        selected_year = self.year_var.get()  # Fetch selected year

        # Check if student ID is empty
        if not student_id:
            messagebox.showwarning("Input Error", "Please enter a Student ID.")
            return  # Exit the function if ID is empty

        # Add the title label for the report and center it
        Label(self.content_frame, text="Report Form", bg="white", fg="black", font=("Arial", 16, "bold")).pack(padx=10, pady=(10, 5), anchor="center", fill="x")

        # Create a frame for the table-like layout with a fixed width of 500
        table_frame = Frame(self.content_frame, bg="white", width=500)
        table_frame.pack(padx=10, pady=5, anchor="center")  # Set padding and anchor

        # Set the column width to 250 for both columns
        table_frame.columnconfigure(0, minsize=250)  # Set minimum width for column 0
        table_frame.columnconfigure(1, minsize=250)  # Set minimum width for column 1

        # Create rows for each label (Name, ID, Month, Year)
        # Row 1: Name and ID
        Label(table_frame, text="Name: " + student_name, bg="white", fg="black").grid(row=0, column=0, sticky="w")  # Name label
        Label(table_frame, text="ID: " + student_id, bg="white", fg="black").grid(row=0, column=1, sticky="w")  # ID label

        # Row 2: Month and Year
        Label(table_frame, text="Month: " + selected_month, bg="white", fg="black").grid(row=1, column=0, pady=5, sticky="w")  # Month label
        Label(table_frame, text="Year: " + selected_year, bg="white", fg="black").grid(row=1, column=1, pady=5, sticky="w")  # Year label

        # Display selected courses label, centered and with font size 14
        Label(self.content_frame, text="Courses Attendance", bg="white", fg="black", font=("Arial", 14)).pack(anchor="center", padx=10, pady=5)        

        selected_courses = self.selected_courses_listbox.get(0, 'end')

        for course in selected_courses:
            Label(self.content_frame, text="- " + course, bg="white", fg="black").pack(anchor="w", padx=20)
            # Create a frame for the table

            attendance_data = self.fetch_attendance_data(student_id, course,selected_month,selected_year)
            

            table_frame = Frame(self.content_frame, bg="white")
            table_frame.pack(padx=10, pady=(5, 10))  # Fill both vertically and horizontally

            # Load the Arial font
            font = ImageFont.truetype("arial.ttf", 12)  # Specify the font size as needed

            # Create table headers with text
            headers = ["Date", "Hour", "Status"]
            header_bg_color = "lightgray"  # Background color for headers

            for row, header in enumerate(headers):
                img = self.create_rotated_image(header, 0, font)  # No rotation for headers
                img_label = Label(table_frame, image=img, bg=header_bg_color)  # Set header background color
                img_label.image = img  # Keep a reference to avoid garbage collection
                img_label.grid(row=row, column=0, sticky="nsew")  # Center headers

            # Populate the table with attendance data
            for col, (date, attendance_status, course_hour) in enumerate(attendance_data, start=1):
                status_mark = ''
                if attendance_status == "Present":
                    status_mark = "P"
                elif attendance_status == "Absent":
                    status_mark = "A"
                elif attendance_status == "Half-Absent":
                    status_mark = "P/A"

                date_img = self.create_rotated_image(date, 90, font)  # Rotate date
                hour_img = self.create_rotated_image(course_hour, 90, font)  # Rotate hour
                status_img = self.create_rotated_image(status_mark, 0, font)  # No rotation for status

                # Adjusting grid placement to center-align
                date_label = Label(table_frame, image=date_img, bg="white")  # Set background color to blue
                date_label.image = date_img  # Keep a reference
                date_label.grid(row=0, column=col, sticky="nsew")  # Row 1 for dates

                hour_label = Label(table_frame, image=hour_img,bg="white")
                hour_label.image = hour_img  # Keep a reference
                hour_label.grid(row=1, column=col, sticky="nsew")  # Row 2 for hours

                status_label = Label(table_frame, image=status_img, bg="white")
                status_label.image = status_img  # Keep a reference
                status_label.grid(row=2, column=col, sticky="nsew")  # Row 3 for status

            # Configure grid weights to allow proper expansion
            for i in range(len(attendance_data) + 1):  # Number of rows
                table_frame.grid_rowconfigure(i, weight=1)

            for i in range(len(headers) + 1):  # Number of columns
                table_frame.grid_columnconfigure(i, weight=1)
        # Display Emotion Status label, centered and with font size 14
        Label(self.content_frame, text="Emotion Status", bg="white", fg="black", font=("Arial", 14)).pack(anchor="center", padx=10, pady=5)
        
        if self.detail_var.get():
            # Call the function to display the emotion status chart
            self.get_emotion_status(student_id, student_name, selected_month, selected_year)

        if self.overall_var.get():
            self.emotion_status_overall(student_id, student_name, selected_month, selected_year)

        if self.table_var.get():
            # Fetch emotional data
            emotional_data = self.emotion_status_table(student_id, student_name, selected_month, selected_year)

            # Create a frame for the emotion status table
            table_frame = Frame(self.content_frame, bg="white")
            table_frame.pack(padx=10, pady=(5, 10))  # Add some padding and fill horizontally

            # Create table header with each heading in its own cell
            Label(table_frame, text="Date", bg="white", fg="black").grid(row=0, column=0, padx=5, pady=5)  # Date in row 0, column 0
            Label(table_frame, text="Neutral", bg="white", fg="black").grid(row=0, column=1, padx=5, pady=5)  # Neutral in row 0, column 1
            Label(table_frame, text="Happy", bg="white", fg="black").grid(row=0, column=2, padx=5, pady=5)  # Happy in row 0, column 2
            Label(table_frame, text="Fear", bg="white", fg="black").grid(row=0, column=3, padx=5, pady=5)  # Fear in row 0, column 3
            Label(table_frame, text="Surprise", bg="white", fg="black").grid(row=0, column=4, padx=5, pady=5)  # Surprise in row 0, column 4
            Label(table_frame, text="Angry", bg="white", fg="black").grid(row=0, column=5, padx=5, pady=5)  # Angry in row 0, column 5

            # Populate the table with emotional data
            for row_index, (date, neutral, happy, sad, fear, surprise, angry) in enumerate(emotional_data, start=1):
                Label(table_frame, text=date, bg="white", fg="black").grid(row=row_index, column=0, padx=5, pady=5)
                Label(table_frame, text=neutral, bg="white", fg="black").grid(row=row_index, column=1, padx=5, pady=5)
                Label(table_frame, text=happy, bg="white", fg="black").grid(row=row_index, column=2, padx=5, pady=5)
                Label(table_frame, text=fear, bg="white", fg="black").grid(row=row_index, column=3, padx=5, pady=5)
                Label(table_frame, text=surprise, bg="white", fg="black").grid(row=row_index, column=4, padx=5, pady=5)
                Label(table_frame, text=angry, bg="white", fg="black").grid(row=row_index, column=5, padx=5, pady=5)

            # Update scroll region to encompass all items
            self.update_scroll_region()



    def emotion_status_table(self, student_id, student_name, selected_month, selected_year): 
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

        cursor.execute(query, (student_name, student_id, selected_month, selected_year))
        results = cursor.fetchall()
        cursor.close()
        connection.close()

        return results

    def emotion_status_overall(self, student_id, student_name, selected_month, selected_year):
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
        
        cursor.execute(query, (student_name, student_id, selected_month, selected_year))
        results = cursor.fetchall()
        
        # Close the database connection 
        connection.close()

        if not results:
            month_name = calendar.month_name[int(selected_month)]
            messagebox.showinfo("Info", f"No emotion data found for the selected student in {month_name}, {selected_year}.")
            return

        # Extracting data for the chart
        days = []  
        max_emotion_values = []
        max_emotion_labels = []

        # Define emotion color mapping
        emotion_colors = {
            'Neutral': 'green',
            'Happy': 'yellow',
            'Sad': 'blue',
            'Fear': 'purple',
            'Surprise': 'orange',
            'Angry': 'red'
        }

        for row in results:
            # Extract the day from the date
            date_str = str(row[0])  # Assuming the date is in a datetime format
            day = date_str.split('-')[2]  # Get the day (DD) from YYYY-MM-DD
            
            days.append(day)  # Append the day instead of the full date
            
            # Find the maximum emotion value and its corresponding label
            emotion_values = [row[1], row[2], row[3], row[4], row[5], row[6]]
            max_value = max(emotion_values)
            max_index = emotion_values.index(max_value)

            max_emotion_values.append(max_value)
            
            # Map emotion index to labels
            emotions = ['Neutral', 'Happy', 'Sad', 'Fear', 'Surprise', 'Angry']
            max_emotion_labels.append(emotions[max_index])

        # Plotting the bar chart with only the max emotions
        figure, ax = plt.subplots(figsize=(5, 4))  # Set the figure size to fit your needs

        # Assign the color based on the max emotion
        colors = [emotion_colors[label] for label in max_emotion_labels]

        bars = ax.bar(days, max_emotion_values, color=colors)  # Use the corresponding color for each max emotion

        # Setting the labels
        ax.set_xlabel('Day (DD)')
        ax.set_ylabel('Emotion Value')
        ax.set_title(f'Max Emotion Status for {student_name} ({calendar.month_name[int(selected_month)]}, {selected_year})')

        # Updated x-ticks and labels
        ax.set_xticks(range(len(days)))
        ax.set_xticklabels(days, rotation=90)  # Rotate labels for better visibility

        # Create a legend for the emotion colors
        handles = [plt.Rectangle((0, 0), 1, 1, color=color) for color in emotion_colors.values()]
        ax.legend(handles, emotion_colors.keys(), title="Emotions")

        # Displaying the chart in the Tkinter Frame (main_frame)
        canvas = FigureCanvasTkAgg(figure, master=self.content_frame)
        canvas.draw()

        # Set the canvas size explicitly
        canvas.get_tk_widget().config(width=500, height=300)  # Set the canvas size

        # Pack the canvas to fill the main_frame
        canvas.get_tk_widget().pack(fill="both", expand=True)


    def get_emotion_status(self, student_id, student_name, selected_month, selected_year):
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
        
        cursor.execute(query, (student_name, student_id, selected_month, selected_year))
        results = cursor.fetchall()
        
        # Close the database connection 
        connection.close()

        if not results:
            messagebox.showinfo("Info", f"No emotion data found for the selected student in {selected_month}, {selected_year}.")
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

        # Plotting the vertical stacked bar chart with a fixed width
        figure, ax = plt.subplots(figsize=(5, 4))  # Set width to 5 inches (approximately 500 pixels)

        # Stacking the bars correctly
        ax.bar(days, neutral, label='Neutral', color='green')
        ax.bar(days, happy, bottom=neutral, label='Happy', color='yellow')
        ax.bar(days, sad, bottom=[i + j for i, j in zip(neutral, happy)], label='Sad', color='blue')
        ax.bar(days, fear, bottom=[i + j + k for i, j, k in zip(neutral, happy, sad)], label='Fear', color='purple')
        ax.bar(days, surprise, bottom=[i + j + k + l for i, j, k, l in zip(neutral, happy, sad, fear)], label='Surprise', color='orange')
        ax.bar(days, angry, bottom=[i + j + k + l + m for i, j, k, l, m in zip(neutral, happy, sad, fear, surprise)], label='Angry', color='red')

        # Set x-axis ticks and rotate labels to prevent overlap
        ax.set_xticks(range(len(days)))
        ax.set_xticklabels(days, rotation=90)

        # Setting the labels
        ax.set_xlabel('Day (DD)')
        ax.set_ylabel('Emotion')
        ax.set_title(f'Emotion Status for {student_name} ({selected_month}, {selected_year})')
        ax.legend()

        # Displaying the chart in the Tkinter Frame (content_frame inside preview_frame)
        canvas = FigureCanvasTkAgg(figure, master=self.content_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)




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
        teacher_interface.Teacher_Interface(new_window, self.username)


# Example usage
if __name__ == "__main__":
    root = tk.Tk()
    report_generator_interface_teacher = Report_Generater_Interface_Teacher(root, "AdminUser")
    root.mainloop()
