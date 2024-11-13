import tkinter as tk
from tkinter import ttk, Listbox
from tkinter import Frame, Canvas, Scrollbar, Label, messagebox, StringVar, BooleanVar, Entry, Listbox
from tkinter import LabelFrame, Label, Entry, Button, StringVar
from tkinter import *
from PIL import Image, ImageTk
import teacher_interface
import mysql.connector  
from tkinter import Label, Frame, messagebox  
import mysql.connector
from tkinter import messagebox  
from fpdf import FPDF
from pdf2image import convert_from_path
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from datetime import datetime  
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
        self.username = username  
        self.root.geometry("1024x590+0+0")
        self.root.title("AttendNow")

        
        background_img_main = Image.open(r"Image\Background.png")
        background_img_main = background_img_main.resize((1024, 590), Image.Resampling.LANCZOS)
        self.photo_background_img_main = ImageTk.PhotoImage(background_img_main)
        background_img_main_position = Label(self.root, image=self.photo_background_img_main)
        background_img_main_position.place(x=0, y=0, width=1024, height=590)
        

        
        left_title = Image.open(r"Image\LogoTitle_Left Top.png")
        self.photoleft_title = ImageTk.PhotoImage(left_title)
        left_title_position = Label(self.root, image=self.photoleft_title)
        left_title_position.place(x=0, y=0, width=163, height=60)

        
        back_button = Button(self.root, text="Back", command=self.back_to_main, bg="red", fg="white", font=("Arial", 12, "bold"))
        back_button.place(x=175, y=15, width=80, height=30)

        
        main_frame2 = Frame(background_img_main_position, bd=2, bg="orange")
        main_frame2.place(x=300, y=5, width=400, height=50)

        
        main_title = Label(main_frame2, text="Teacher Interface", bg="orange", fg="white", font=("New Time Roman", 20, "bold"))
        main_title.place(x=5, y=2, width=400, height=40)

        
        self.username_label = Label(self.root, text=f"Logged in as: {username}", bg="orange", fg="white", font=("Arial", 12))
        self.username_label.place(x=800, y=15)


        self.report_frame = Frame(self.root, bd=2, bg="orange")
        self.report_frame.place(x=450, y=70, width=560, height=510)



        
        make_report_frame = LabelFrame(self.root, text="Report Form", bg="white", fg="black")
        make_report_frame.place(x=25, y=75, width=420, height=485)



        
        student_info_frame = LabelFrame(make_report_frame, text="Student Information", bg="white", fg="black")
        student_info_frame.place(x=5, y=5, width=405, height=100)  

        
        student_id_label = Label(student_info_frame, text="Student ID:", bg="white", fg="black")
        student_id_label.place(x=10, y=10)  

        self.student_id_entry = Entry(student_info_frame, width=15)  
        self.student_id_entry.place(x=100, y=10)  

        
        search_button = Button(student_info_frame, text="Search ID", bg="orange", fg="white", width=10, command=self.search_student_info)  
        search_button.place(x=270, y=10)  

        
        student_name_label = Label(student_info_frame, text="Student Found:", bg="white", fg="black")
        student_name_label.place(x=10, y=40)  
        self.student_name_display = Label(student_info_frame, text="", bg="white", fg="black")  
        self.student_name_display.place(x=150, y=40)  


         
        date_info_frame = LabelFrame(make_report_frame, text="Month / Year", bg="white", fg="black")
        date_info_frame.place(x=5, y=110, width=405, height=50)

        
        month_label = Label(date_info_frame, text="Select Month:", bg="white", fg="black")
        month_label.place(x=10, y=5)  

        
        self.month_var = StringVar()
        self.month_var.set("Select Month")  
        months = [str(i) for i in range(1, 13)]  
        month_dropdown = ttk.Combobox(date_info_frame, textvariable=self.month_var, values=months, width=13)
        month_dropdown.place(x=100, y=5)  

        
        year_label = Label(date_info_frame, text="Select Year:", bg="white", fg="black")
        year_label.place(x=220, y=5)  

        
        self.year_var = StringVar()
        self.year_var.set("Select Year")  
        years = [str(i) for i in range(2020, 2031)]  
        year_dropdown = ttk.Combobox(date_info_frame, textvariable=self.year_var, values=years,width=13)
        year_dropdown.place(x=300, y=5)  




        
        course_frame = LabelFrame(make_report_frame, text="Course", bg="white", fg="black")
        course_frame.place(x=5, y=160, width=405, height=190)  

        
        course_name_label = Label(course_frame, text="Course Name:", bg="white", fg="black")
        course_name_label.place(x=10, y=10)

        
        self.course_name_combobox = ttk.Combobox(course_frame, values=[], width=37, state="readonly")
        self.course_name_combobox.place(x=150, y=10)
        self.course_name_combobox.set("Select Course")  
        

        
        selected_courses_label = Label(course_frame, text="Course Selected:", bg="white", fg="black")
        selected_courses_label.place(x=10, y=45)  

        
        self.selected_courses_listbox = Listbox(course_frame, height=5, width=40)
        self.selected_courses_listbox.place(x=150, y=45)  

        
        self.delete_course_button = Button(course_frame, text="Delete Selected Course", command=self.delete_selected_course)
        self.delete_course_button.place(x=150, y=135)  

        
        self.course_name_combobox.bind("<<ComboboxSelected>>", lambda event: self.add_course())



       
        emotion_status_frame = LabelFrame(make_report_frame, text="Emotion Status", bg="white", fg="black")
        emotion_status_frame.place(x=5, y=350, width=405, height=50)  

        
        self.detail_var = BooleanVar()
        self.overall_var = BooleanVar()
        self.table_var = BooleanVar()

        
        self.detail_checkbox = Checkbutton(emotion_status_frame, text="Chart (Detailed)", variable=self.detail_var, bg="white")
        self.detail_checkbox.place(x=20, y=3)

        self.overall_checkbox = Checkbutton(emotion_status_frame, text="Chart (Overall)", variable=self.overall_var, bg="white")
        self.overall_checkbox.place(x=150, y=3)

        self.table_checkbox = Checkbutton(emotion_status_frame, text="Status in Table", variable=self.table_var, bg="white")
        self.table_checkbox.place(x=280, y=3)


        
        report_generate_frame = LabelFrame(make_report_frame, text="Report Generate", bg="white", fg="black")
        report_generate_frame.place(x=5, y=400, width=405, height=60)  

        display_label = Button(report_generate_frame, bg="orange", fg="white", text="Display Info", command=self.display_student_info)
        display_label.place(x=50, y=10, width=150)

        
        
        generate_report_button = Button(report_generate_frame, text="Generate Report", bg="orange", fg="white", command=self.generate_report)
        generate_report_button.place(x=250, y=10, width=150)

        


      
        self.preview_frame = Frame(self.report_frame, bg="white", bd=2)  
        self.preview_frame.place(x=5, y=5, width=550, height=490)

        
        self.canvas = Canvas(self.preview_frame, bg="white")  
        self.canvas.pack(side="left", fill="both", expand=True)

        
        self.content_frame = Frame(self.canvas, bg="white")  
        self.canvas.create_window((0, 0), window=self.content_frame, anchor="nw")

        
        self.y_scrollbar = Scrollbar(self.preview_frame, orient="vertical", command=self.canvas.yview)
        self.y_scrollbar.pack(side="right", fill="y")

        
        self.canvas.configure(yscrollcommand=self.y_scrollbar.set)  

        
        self.content_frame.bind("<Configure>", self.update_scroll_region)




        

        




       

       


    
    def update_scroll_region(self, event):
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))  

    def fetch_attendance_data_report(self, student_id, course, month, year):
            connection = mysql.connector.connect(
                host='localhost',
                user='root',
                password='Nightcore_1134372019!',
                database='attendnow'
            )
            
            cursor = connection.cursor()
            
            
            query = 
            
            
            cursor.execute(query, (student_id, course, year, month))
            
            
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
        
        
        query = 
        
        
        cursor.execute(query, (student_id, course, year, month))
        
        
        attendance_data = cursor.fetchall()
        cursor.close()
        connection.close()
        
        return attendance_data

    def generate_report(self):
        
        student_id = self.student_id_entry.get()
        student_name = self.student_name_display.cget("text")  
        selected_month = self.month_var.get()  
        selected_year = self.year_var.get()
        
        selected_month_text = ""

        
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
            selected_month_text = "Invalid month"  

        

        
        if not student_id:
            messagebox.showwarning("Input Error", "Please enter a Student ID.")
            return  

        
        pdfmetrics.registerFont(TTFont('Arial', 'Arial.ttf'))  

        
        c = canvas.Canvas(student_name + ".pdf", pagesize=letter)

        
        title = "Report Form"
        font_name = "Arial"  
        font_size = 16

        
        c.setFont(font_name, font_size)
        c.setFillColor(colors.black)

        
        width = c._pagesize[0]
        text_width = c.stringWidth(title, font_name, font_size)

        
        c.drawString((width - text_width) / 2, 10 * inch, title)  

        
        table_font_size = 12
        c.setFont(font_name, table_font_size)

        
        table_data = [
            ["Name: " + student_name, "ID: " + student_id],
            ["Month: " + selected_month_text, "Year: " + selected_year]
        ]

        
        padding = 0.5 * inch  

        
        available_width = width - (2 * padding)  
        cell_width = available_width / 2  
        cell_height = (0.5 * inch) - 10  

        
        table_start_y = (10 * inch) - (cell_height + 0.1 * inch)  

        
        for row_index, row in enumerate(table_data):
            for col_index, text in enumerate(row):
                x = padding + col_index * cell_width  
                y = table_start_y - (row_index * cell_height)  

                
                c.drawString(x + 0.2 * inch, y + 0.1 * inch, text)  

        

        
        
        title_below_font_size = 14
        c.setFont(font_name, title_below_font_size)

        
        title_below = "Attendance Status"

        
        title_below_y = y - cell_height - 0.3 * inch  

        
        text_width = c.stringWidth(title_below, font_name, title_below_font_size)
        c.drawString((width - text_width) / 2, title_below_y, title_below)

        

        
        selected_courses = self.selected_courses_listbox.get(0, 'end')  

        
        course_start_y = title_below_y - 0.5 * inch  

        
        course_font_size = 12
        c.setFont(font_name, course_font_size)
    
        
        
        page_width, page_height = A4
        left_margin = 0.5 * inch
        right_margin = 0.5 * inch
        available_width = page_width - left_margin - right_margin
        course_start_y = page_height - 1 * inch  

        
        headers = ["Date", "Hour", "Status"]
        num_columns = 3  
        column_width = available_width / num_columns  

        
        font_name = "Helvetica"
        title_below_font_size = 14
        table_header_font_size = 10
        table_data_font_size = 10

        
        title_below = "Attendance Status"

        
        for index, course in enumerate(selected_courses):
            
            course_y = course_start_y - (index * 2 * inch)  

            
            c.setFont("Helvetica-Bold", 12)
            c.drawString(left_margin, course_y, f"Course: {course}")

            
            attendance_data = self.fetch_attendance_data_report(student_id, course, selected_month, selected_year)

            
            headers = ["Date", "Hour", "Status"]
            left_margin = 0.5 * inch
            column_width = 2 * inch
            table_start_y = height - 150

            c.setFont("Helvetica-Bold", 12)
            for col_index, header in enumerate(headers):
                header_x = left_margin + col_index * column_width
                c.drawString(header_x, table_start_y, header)

            
            row_height = 0.4 * inch
            c.setFont("Helvetica", 10)
            for data_index, data in enumerate(attendance_data):
                data_y = table_start_y - ((data_index + 1) * row_height)
                for col_index, value in enumerate(data):
                    data_x = left_margin + col_index * column_width
                    c.drawString(data_x, data_y, str(value))

            c.save()


        
        

        
        c.save()

        print(f"PDF saved as {student_name}.pdf")


    def create_rotated_image(self,text, angle, font):
        
        bbox = font.getbbox(text)
        text_width = bbox[2] - bbox[0]  
        text_height = bbox[3] - bbox[1]  
        
        
        img = Image.new('RGBA', (text_width + 10, text_height + 10), (255, 255, 255, 0))  
        d = ImageDraw.Draw(img)
        
        
        text_x = (img.width - text_width) / 2
        text_y = (img.height - text_height) / 2
        
        
        d.text((text_x, text_y), text, fill=(0, 0, 0), font=font)
        
        
        img = img.rotate(angle, expand=1)
        
        
        img = img.convert("RGBA")  
        img_tk = ImageTk.PhotoImage(img)  
        return img_tk


    def display_student_info(self):
        
        for widget in self.content_frame.winfo_children():
            widget.destroy()

        
        student_id = self.student_id_entry.get()
        student_name = self.student_name_display.cget("text")
        selected_month = self.month_var.get()  
        selected_year = self.year_var.get()  

        
        if not student_id:
            messagebox.showwarning("Input Error", "Please enter a Student ID.")
            return  

        
        Label(self.content_frame, text="Report Form", bg="white", fg="black", font=("Arial", 16, "bold")).pack(padx=10, pady=(10, 5), anchor="center", fill="x")

        
        table_frame = Frame(self.content_frame, bg="white", width=500)
        table_frame.pack(padx=10, pady=5, anchor="center")  

        
        table_frame.columnconfigure(0, minsize=250)  
        table_frame.columnconfigure(1, minsize=250)  

        
        
        Label(table_frame, text="Name: " + student_name, bg="white", fg="black").grid(row=0, column=0, sticky="w")  
        Label(table_frame, text="ID: " + student_id, bg="white", fg="black").grid(row=0, column=1, sticky="w")  

        
        Label(table_frame, text="Month: " + selected_month, bg="white", fg="black").grid(row=1, column=0, pady=5, sticky="w")  
        Label(table_frame, text="Year: " + selected_year, bg="white", fg="black").grid(row=1, column=1, pady=5, sticky="w")  

        
        Label(self.content_frame, text="Courses Attendance", bg="white", fg="black", font=("Arial", 14)).pack(anchor="center", padx=10, pady=5)        

        selected_courses = self.selected_courses_listbox.get(0, 'end')

        for course in selected_courses:
            Label(self.content_frame, text="- " + course, bg="white", fg="black").pack(anchor="w", padx=20)
            

            attendance_data = self.fetch_attendance_data(student_id, course,selected_month,selected_year)
            

            table_frame = Frame(self.content_frame, bg="white")
            table_frame.pack(padx=10, pady=(5, 10))  

            
            font = ImageFont.truetype("arial.ttf", 12)  

            
            headers = ["Date", "Hour", "Status"]
            header_bg_color = "lightgray"  

            for row, header in enumerate(headers):
                img = self.create_rotated_image(header, 0, font)  
                img_label = Label(table_frame, image=img, bg=header_bg_color)  
                img_label.image = img  
                img_label.grid(row=row, column=0, sticky="nsew")  

            
            for col, (date, attendance_status, course_hour) in enumerate(attendance_data, start=1):
                status_mark = ''
                if attendance_status == "Present":
                    status_mark = "P"
                elif attendance_status == "Absent":
                    status_mark = "A"
                elif attendance_status == "Half-Absent":
                    status_mark = "P/A"

                date_img = self.create_rotated_image(date, 90, font)  
                hour_img = self.create_rotated_image(course_hour, 90, font)  
                status_img = self.create_rotated_image(status_mark, 0, font)  

                
                date_label = Label(table_frame, image=date_img, bg="white")  
                date_label.image = date_img  
                date_label.grid(row=0, column=col, sticky="nsew")  

                hour_label = Label(table_frame, image=hour_img,bg="white")
                hour_label.image = hour_img  
                hour_label.grid(row=1, column=col, sticky="nsew")  

                status_label = Label(table_frame, image=status_img, bg="white")
                status_label.image = status_img  
                status_label.grid(row=2, column=col, sticky="nsew")  

            
            for i in range(len(attendance_data) + 1):  
                table_frame.grid_rowconfigure(i, weight=1)

            for i in range(len(headers) + 1):  
                table_frame.grid_columnconfigure(i, weight=1)
        
        Label(self.content_frame, text="Emotion Status", bg="white", fg="black", font=("Arial", 14)).pack(anchor="center", padx=10, pady=5)
        
        if self.detail_var.get():
            
            self.get_emotion_status(student_id, student_name, selected_month, selected_year)

        if self.overall_var.get():
            self.emotion_status_overall(student_id, student_name, selected_month, selected_year)

        if self.table_var.get():
            
            emotional_data = self.emotion_status_table(student_id, student_name, selected_month, selected_year)

            
            table_frame = Frame(self.content_frame, bg="white")
            table_frame.pack(padx=10, pady=(5, 10))  

            
            Label(table_frame, text="Date", bg="white", fg="black").grid(row=0, column=0, padx=5, pady=5)  
            Label(table_frame, text="Neutral", bg="white", fg="black").grid(row=0, column=1, padx=5, pady=5)  
            Label(table_frame, text="Happy", bg="white", fg="black").grid(row=0, column=2, padx=5, pady=5)  
            Label(table_frame, text="Fear", bg="white", fg="black").grid(row=0, column=3, padx=5, pady=5)  
            Label(table_frame, text="Surprise", bg="white", fg="black").grid(row=0, column=4, padx=5, pady=5)  
            Label(table_frame, text="Angry", bg="white", fg="black").grid(row=0, column=5, padx=5, pady=5)  

            
            for row_index, (date, neutral, happy, sad, fear, surprise, angry) in enumerate(emotional_data, start=1):
                Label(table_frame, text=date, bg="white", fg="black").grid(row=row_index, column=0, padx=5, pady=5)
                Label(table_frame, text=neutral, bg="white", fg="black").grid(row=row_index, column=1, padx=5, pady=5)
                Label(table_frame, text=happy, bg="white", fg="black").grid(row=row_index, column=2, padx=5, pady=5)
                Label(table_frame, text=fear, bg="white", fg="black").grid(row=row_index, column=3, padx=5, pady=5)
                Label(table_frame, text=surprise, bg="white", fg="black").grid(row=row_index, column=4, padx=5, pady=5)
                Label(table_frame, text=angry, bg="white", fg="black").grid(row=row_index, column=5, padx=5, pady=5)

            
            self.update_scroll_region()



    def emotion_status_table(self, student_id, student_name, selected_month, selected_year): 
        
        connection = mysql.connector.connect(
            host="localhost",  
            user="root",
            password="Nightcore_1134372019!",
            database="attendnow"
        )

        cursor = connection.cursor()

        
        query = 

        cursor.execute(query, (student_name, student_id, selected_month, selected_year))
        results = cursor.fetchall()
        cursor.close()
        connection.close()

        return results

    def emotion_status_overall(self, student_id, student_name, selected_month, selected_year):
        
        connection = mysql.connector.connect(
            host="localhost",  
            user="root",
            password="Nightcore_1134372019!",
            database="attendnow"
        )
        
        cursor = connection.cursor()

        
        query = 
        
        cursor.execute(query, (student_name, student_id, selected_month, selected_year))
        results = cursor.fetchall()
        
        
        connection.close()

        if not results:
            month_name = calendar.month_name[int(selected_month)]
            messagebox.showinfo("Info", f"No emotion data found for the selected student in {month_name}, {selected_year}.")
            return

        
        days = []  
        max_emotion_values = []
        max_emotion_labels = []

        
        emotion_colors = {
            'Neutral': 'green',
            'Happy': 'yellow',
            'Sad': 'blue',
            'Fear': 'purple',
            'Surprise': 'orange',
            'Angry': 'red'
        }

        for row in results:
            
            date_str = str(row[0])  
            day = date_str.split('-')[2]  
            
            days.append(day)  
            
            
            emotion_values = [row[1], row[2], row[3], row[4], row[5], row[6]]
            max_value = max(emotion_values)
            max_index = emotion_values.index(max_value)

            max_emotion_values.append(max_value)
            
            
            emotions = ['Neutral', 'Happy', 'Sad', 'Fear', 'Surprise', 'Angry']
            max_emotion_labels.append(emotions[max_index])

        
        figure, ax = plt.subplots(figsize=(5, 4))  

        
        colors = [emotion_colors[label] for label in max_emotion_labels]

        bars = ax.bar(days, max_emotion_values, color=colors)  

        
        ax.set_xlabel('Day (DD)')
        ax.set_ylabel('Emotion Value')
        ax.set_title(f'Max Emotion Status for {student_name} ({calendar.month_name[int(selected_month)]}, {selected_year})')

        
        ax.set_xticks(range(len(days)))
        ax.set_xticklabels(days, rotation=90)  

        
        handles = [plt.Rectangle((0, 0), 1, 1, color=color) for color in emotion_colors.values()]
        ax.legend(handles, emotion_colors.keys(), title="Emotions")

        
        canvas = FigureCanvasTkAgg(figure, master=self.content_frame)
        canvas.draw()

        
        canvas.get_tk_widget().config(width=500, height=300)  

        
        canvas.get_tk_widget().pack(fill="both", expand=True)


    def get_emotion_status(self, student_id, student_name, selected_month, selected_year):
        
        connection = mysql.connector.connect(
            host="localhost",  
            user="root",
            password="Nightcore_1134372019!",
            database="attendnow"
        )
        
        cursor = connection.cursor()

        
        query = 
        
        cursor.execute(query, (student_name, student_id, selected_month, selected_year))
        results = cursor.fetchall()
        
        
        connection.close()

        if not results:
            messagebox.showinfo("Info", f"No emotion data found for the selected student in {selected_month}, {selected_year}.")
            return

        
        days = []  
        neutral = []
        happy = []
        sad = []
        fear = []
        surprise = []
        angry = []
        
        for row in results:
            
            date_str = str(row[0])  
            day = date_str.split('-')[2]  
            
            days.append(day)  
            neutral.append(row[1])
            happy.append(row[2])
            sad.append(row[3])
            fear.append(row[4])
            surprise.append(row[5])
            angry.append(row[6])

        
        figure, ax = plt.subplots(figsize=(5, 4))  

        
        ax.bar(days, neutral, label='Neutral', color='green')
        ax.bar(days, happy, bottom=neutral, label='Happy', color='yellow')
        ax.bar(days, sad, bottom=[i + j for i, j in zip(neutral, happy)], label='Sad', color='blue')
        ax.bar(days, fear, bottom=[i + j + k for i, j, k in zip(neutral, happy, sad)], label='Fear', color='purple')
        ax.bar(days, surprise, bottom=[i + j + k + l for i, j, k, l in zip(neutral, happy, sad, fear)], label='Surprise', color='orange')
        ax.bar(days, angry, bottom=[i + j + k + l + m for i, j, k, l, m in zip(neutral, happy, sad, fear, surprise)], label='Angry', color='red')

        
        ax.set_xticks(range(len(days)))
        ax.set_xticklabels(days, rotation=90)

        
        ax.set_xlabel('Day (DD)')
        ax.set_ylabel('Emotion')
        ax.set_title(f'Emotion Status for {student_name} ({selected_month}, {selected_year})')
        ax.legend()

        
        canvas = FigureCanvasTkAgg(figure, master=self.content_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)




    def update_scroll_region(self, event=None):
        
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        
        
    
    
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
        else:
            messagebox.showwarning("Selection Error", "Please select a course to delete.")  


    
    def add_course(self):
        selected_course = self.course_name_combobox.get()  
        if selected_course not in self.selected_courses_listbox.get(0, END):  
            self.selected_courses_listbox.insert(END, selected_course)  

    def back_to_main(self):
        self.root.destroy()  
        new_window = Tk()  
        teacher_interface.Teacher_Interface(new_window, self.username)



if __name__ == "__main__":
    root = tk.Tk()
    report_generator_interface_teacher = Report_Generater_Interface_Teacher(root, "AdminUser")
    root.mainloop()
