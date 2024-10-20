import tkinter as tk
from tkinter import ttk, Listbox
from tkinter import LabelFrame, Label, Entry, Button, StringVar
from tkinter import *
from PIL import Image, ImageTk
import admit_interface
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

        # Background Image
        background_img_main = Image.open(r"Image\Background.png")
        background_img_main = background_img_main.resize((1024, 590), Image.Resampling.LANCZOS)
        self.photo_background_img_main = ImageTk.PhotoImage(background_img_main)
        background_img_main_position = Label(self.root, image=self.photo_background_img_main)
        background_img_main_position.place(x=0, y=0, width=1024, height=590)

        # Logo Title Image
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

        # Student Information
        student_info_frame = LabelFrame(make_report_frame, text="Student Information", bg="white", fg="black")
        student_info_frame.place(x=5, y=5, width=450, height=100)

        # Student ID
        student_id_label = Label(student_info_frame, text="Student ID:", bg="white", fg="black")
        student_id_label.place(x=10, y=10)

        self.student_id_entry = Entry(student_info_frame, width=15)
        self.student_id_entry.place(x=100, y=10)

        # Search ID Button
        search_button = Button(student_info_frame, text="Search ID", bg="orange", fg="white", width=10, command=self.search_student_info)
        search_button.place(x=270, y=10)

        # Student Name
        student_name_label = Label(student_info_frame, text="Student Found:", bg="white", fg="black")
        student_name_label.place(x=10, y=40)
        self.student_name_display = Label(student_info_frame, text="", bg="white", fg="black")
        self.student_name_display.place(x=150, y=40)

        # Course Information
        course_frame = LabelFrame(make_report_frame, text="Course", bg="white", fg="black")
        course_frame.place(x=5, y=110, width=450, height=190)

        course_name_label = Label(course_frame, text="Course Name:", bg="white", fg="black")
        course_name_label.place(x=10, y=10)

        self.course_name_combobox = ttk.Combobox(course_frame, values=[], width=37, state="readonly")
        self.course_name_combobox.place(x=150, y=10)
        self.course_name_combobox.set("Select Course")

        selected_courses_label = Label(course_frame, text="Course Selected:", bg="white", fg="black")
        selected_courses_label.place(x=10, y=50)

        self.selected_courses_listbox = Listbox(course_frame, height=5, width=40)
        self.selected_courses_listbox.place(x=150, y=50)

        self.delete_course_button = Button(course_frame, text="Delete Selected Course", command=self.delete_selected_course)
        self.delete_course_button.place(x=150, y=135)

        self.course_name_combobox.bind("<<ComboboxSelected>>", lambda event: self.add_course())

        # Emotion Status
        emotion_status_frame = LabelFrame(make_report_frame, text="Emotion Status", bg="white", fg="black")
        emotion_status_frame.place(x=5, y=305, width=450, height=80)

        self.detail_var = BooleanVar()
        self.overall_var = BooleanVar()
        self.table_var = BooleanVar()

        self.detail_checkbox = Checkbutton(emotion_status_frame, text="Chart (Detailed)", variable=self.detail_var, bg="white")
        self.detail_checkbox.place(x=20, y=10)

        self.overall_checkbox = Checkbutton(emotion_status_frame, text="Chart (Overall)", variable=self.overall_var, bg="white")
        self.overall_checkbox.place(x=150, y=10)

        self.table_checkbox = Checkbutton(emotion_status_frame, text="Status in Table", variable=self.table_var, bg="white")
        self.table_checkbox.place(x=280, y=10)

        # Report Generate
        report_generate_frame = LabelFrame(make_report_frame, text="Report Generate", bg="white", fg="black")
        report_generate_frame.place(x=5, y=390, width=450, height=60)

        display_label = Button(report_generate_frame, text="Report Preview", bg="orange", fg="white")
        display_label.place(x=50, y=10, width=150)

        generate_report_button = Button(report_generate_frame, text="Generate Report", bg="orange", fg="white")
        generate_report_button.place(x=250, y=10, width=150)

        # Right Frame for PDF Preview
        preview_frame = Frame(report_frame, bg="white", bd=2)
        preview_frame.place(x=500, y=5, width=460, height=490)

        canvas = Canvas(preview_frame, bg="white")
        canvas.pack(side="left", fill="both", expand=True)

        scrollbar = Scrollbar(preview_frame, orient="vertical", command=canvas.yview)
        scrollbar.pack(side="right", fill="y")

        canvas.configure(yscrollcommand=scrollbar.set)

        content_frame = Frame(canvas, bg="white")
        canvas.create_window((0, 0), window=content_frame, anchor="nw")

        content_frame.bind("<Configure>", self.update_scroll_region)

    def update_scroll_region(self):
        canvas.configure(scrollregion=canvas.bbox("all"))

    def search_student_info(self):
        student_id = self.student_id_entry.get()

        self.course_name_combobox.set("")
        self.student_name_display.config(text="")

        try:
            connection = mysql.connector.connect(
                host='localhost',
                user='root',
                password='Nightcore_1134372019!',
                database='attendnow'
            )

            cursor = connection.cursor()

            query_name = "SELECT student_name FROM students WHERE student_id = %s LIMIT 1"
            cursor.execute(query_name, (student_id,))
            student_name_result = cursor.fetchone()

            if student_name_result:
                student_name = student_name_result[0]
                self.student_name_display.config(text=student_name)
            else:
                self.student_name_display.config(text="Not Found")

            query_courses = "SELECT course FROM students WHERE student_id = %s"
            cursor.execute(query_courses, (student_id,))
            course_results = cursor.fetchall()

            course_names = []

            if course_results:
                for row in course_results:
                    course = row[0]
                    course_names.append(course)

            self.course_name_combobox['values'] = course_names

            if course_names:
                self.course_name_combobox.current(0)
            else:
                self.course_name_combobox['values'] = []

        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Error: {err}")
        finally:
            cursor.close()
            connection.close()

    def delete_selected_course(self):
        selected_index = self.selected_courses_listbox.curselection()

        if selected_index:
            self.selected_courses_listbox.delete(selected_index)

    def add_course(self):
        selected_course = self.course_name_combobox.get()

        if selected_course and selected_course not in self.selected_courses_listbox.get(0, tk.END):
            self.selected_courses_listbox.insert(tk.END, selected_course)

    def back_to_main(self):
        self.root.destroy()
        root = tk.Tk()
        app = admit_interface.Admit_Interface(root, self.username)
        root.mainloop()


# Example usage
if __name__ == "__main__":
    root = tk.Tk()
    app = Report_Generater(root, "AdminUser")
    root.mainloop()