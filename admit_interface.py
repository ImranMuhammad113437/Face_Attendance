from tkinter import * 
from PIL import Image, ImageTk, ImageDraw
import os
import login_page  
from student import Student  
import student
import face_recognition
import curriculum
import data_training
import teacher
import subprocess
import timetable
import emotion_status_interface
import eye_detection
import emotion_detection
import attendance_status_interface
import report_generater
import admin_register
from tkinter import Button, Frame, PhotoImage
from tkinter import Tk, Frame, Label
from tkinter import Frame, Label, Tk
from PIL import Image, ImageTk
import mysql.connector
import tkinter as tk
from tkinter import Frame, Label
from datetime import datetime
from tkinter import Label, Frame

class Admit_Interface:
    def __init__(self, root, username):
        self.root = root
        self.root.geometry("1024x590+0+0")
        self.root.title("AttendNow")


        background_img_main = Image.open(r"Image\Background.png")   
        background_img_main = background_img_main.resize((1024, 590), Image.Resampling.LANCZOS)
        self.photo_background_img_main = ImageTk.PhotoImage(background_img_main)
        background_img_main_position = Label(self.root, image=self.photo_background_img_main)
        background_img_main_position.place(x=0, y=0, width=1024, height=590)

       
        self.main_frame2 = Frame(background_img_main_position, bd=2, bg="orange")
        self.main_frame2.place(x=240, y=10, width=774, height=60)


        save_button = Label(self.main_frame2, text="Dashboard", bg="orange", fg="white", font=("New Time Roman", 20, "bold"))
        save_button.place(x=10, y=10, width=160, height=40)

        # Load and place the course image in the frame
        self.add_image_to_frame(
            frame=self.main_frame2,
            image_path="Image/image_2024-11-19_015242032-removebg-preview.png",
            x=694, y=0, width=60, height=60
        )

        # Create the username label
        self.username_label = Label(self.main_frame2, text=f"{username}", bg="orange", fg="white", font=("Arial", 12))

        # Update x-position of the username so it aligns to the right of the image
        label_width = self.username_label.winfo_reqwidth()  # Get the width of the username label
        image_x_position = 694  # Position of the image
        image_width = 60  # Width of the image
        self.username_label.place(x=image_x_position - label_width - 20, y=0, height=60)  # 10px gap to the image


       
        # Function to change button color and image on hover
        def on_enter(event, button, original_bg, hover_bg, original_fg, hover_fg, new_image):
            button.config(bg=hover_bg, fg=hover_fg, image=new_image)
            button.image = new_image  # Update image reference

        def on_leave(event, button, original_bg, original_fg, original_image):
            button.config(bg=original_bg, fg=original_fg, image=original_image)
            button.image = original_image  # Restore original image

        self.background_img_main_position = root  # Root window passed from outside
        self.main_left_frame = Frame(self.background_img_main_position, bd=0, bg="orange")
        self.main_left_frame.place(x=10, y=10, width=220, height=570)

        # Load and resize the Logo image
        logo_image = Image.open("Image/LogoTitle_Left Top.png").resize((200, 60))  # Adjust size as needed
        logo_image = ImageTk.PhotoImage(logo_image)

        # Place the image above the "Student Information" button
        logo_label = Label(self.main_left_frame, image=logo_image, bg="orange")
        logo_label.image = logo_image  # Keep a reference to avoid garbage collection
        logo_label.place(x=10, y=10, width=200, height=60)  # Adjust position and size as needed

        # Load and resize the image for the "Student Information" button
        self.student_icon = Image.open("Image/graduated.png").resize((20, 20))
        self.student_icon = ImageTk.PhotoImage(self.student_icon)

        # Create the "Student Information" button with the icon on the left, including padding (padx)
        self.student_information = Button(self.main_left_frame, text="Student Information", command=lambda: self.student_detail(username),bg="orange", fg="white", font=("League_Spartan"),
                                            image=self.student_icon, compound="left", padx=10, relief="flat", bd=2)
        self.student_information.place(x=0, y=90, width=220, height=40)  # Adjust position to leave space for the logo above

        # Keep a reference to the "Student Information" image to prevent garbage collection
        self.student_information.image = self.student_icon

        

        # Load the hover image for "Student Information" button
        self.student_icon_hover = Image.open("Image/graduated (1).png").resize((20, 20))
        self.student_icon_hover = ImageTk.PhotoImage(self.student_icon_hover)

        # Bind events for hover effect (change color and image when mouse hovers)
        
        self.original_bg = "orange"  # Original button background color
        self.original_bg_logout= "red"  # Original button background color
        self.hover_bg = "white"  # Hover background color
        self.original_fg = "white"  # Original button text color
        self.hover_fg = "black"  # Hover text color

        self.student_information.bind("<Enter>", lambda event: on_enter(event, self.student_information, self.original_bg, self.hover_bg, self.original_fg, self.hover_fg, self.student_icon_hover))
        self.student_information.bind("<Leave>", lambda event: on_leave(event, self.student_information, self.original_bg, self.original_fg, self.student_icon))

        # Load and resize the image for the "Teacher Information" button
        self.teacher_icon = Image.open("Image/training.png").resize((20, 20))
        self.teacher_icon = ImageTk.PhotoImage(self.teacher_icon)

        # Create the "Teacher Information" button with the icon on the left, including padding (padx)
        self.teacher_info_button = Button(self.main_left_frame, text="Teacher Information", command=lambda: self.open_teacher_info(username),bg="orange", fg="white", font=("League_Spartan"),
                                          image=self.teacher_icon, compound="left", padx=10, relief="flat", bd=2)
        self.teacher_info_button.place(x=0, y=140, width=220, height=40)  # Positioned below the "Student Information" button

        # Keep a reference to the "Teacher Information" image to prevent garbage collection
        self.teacher_info_button.image = self.teacher_icon

        # Load the hover image for "Teacher Information" button
        self.teacher_icon_hover = Image.open("Image/training (1).png").resize((20, 20))
        self.teacher_icon_hover = ImageTk.PhotoImage(self.teacher_icon_hover)

        # Bind events for hover effect (change color and image when mouse hovers)
        self.teacher_info_button.bind("<Enter>", lambda event: on_enter(event, self.teacher_info_button, self.original_bg, self.hover_bg, self.original_fg, self.hover_fg, self.teacher_icon_hover))
        self.teacher_info_button.bind("<Leave>", lambda event: on_leave(event, self.teacher_info_button, self.original_bg, self.original_fg, self.teacher_icon))

        # Load and resize the image for the "Course Information" button
        self.curriculum_icon = Image.open("Image/homework.png").resize((20, 20))
        self.curriculum_icon = ImageTk.PhotoImage(self.curriculum_icon)

        # Create the "Course Information" button with the icon on the left, including padding (padx)
        self.curriculum_button = Button(self.main_left_frame, text="Course Information", command=lambda: self.open_curriculum(username),bg="orange", fg="white", font=("League_Spartan"),
                                        image=self.curriculum_icon, compound="left", padx=10, relief="flat", bd=2)
        self.curriculum_button.place(x=0, y=190, width=220, height=40)  # Positioned below the "Teacher Information" button

        # Keep a reference to the "Course Information" image to prevent garbage collection
        self.curriculum_button.image = self.curriculum_icon

        # Load the hover image for "Course Information" button
        self.curriculum_icon_hover = Image.open("Image/homework (1).png").resize((20, 20))
        self.curriculum_icon_hover = ImageTk.PhotoImage(self.curriculum_icon_hover)

        # Bind events for hover effect (change color and image when mouse hovers)
        self.curriculum_button.bind("<Enter>", lambda event: on_enter(event, self.curriculum_button, self.original_bg, self.hover_bg, self.original_fg, self.hover_fg, self.curriculum_icon_hover))
        self.curriculum_button.bind("<Leave>", lambda event: on_leave(event, self.curriculum_button, self.original_bg, self.original_fg, self.curriculum_icon))

        # Load and resize the image for the "Timetable Information" button
        self.timetable_icon = Image.open("Image/calendar.png").resize((20, 20))
        self.timetable_icon = ImageTk.PhotoImage(self.timetable_icon)

        # Create the "Timetable Information" button with the icon on the left, including padding (padx)
        self.timetable_button = Button(self.main_left_frame, text="Timetable Information", command=lambda: self.timetable(username),bg="orange", fg="white", font=("League_Spartan"),
                                       image=self.timetable_icon, compound="left", padx=10, relief="flat", bd=2)
        self.timetable_button.place(x=0, y=240, width=220, height=40)  # Positioned below the "Course Information" button

        # Keep a reference to the "Timetable Information" image to prevent garbage collection
        self.timetable_button.image = self.timetable_icon

        # Load the hover image for "Timetable Information" button
        self.timetable_icon_hover = Image.open("Image/calendar (1).png").resize((20, 20))
        self.timetable_icon_hover = ImageTk.PhotoImage(self.timetable_icon_hover)

        # Bind events for hover effect (change color and image when mouse hovers)
        self.timetable_button.bind("<Enter>", lambda event: on_enter(event, self.timetable_button, self.original_bg, self.hover_bg, self.original_fg, self.hover_fg, self.timetable_icon_hover))
        self.timetable_button.bind("<Leave>", lambda event: on_leave(event, self.timetable_button, self.original_bg, self.original_fg, self.timetable_icon))

        # Load and resize the image for the "Train System" button
        self.train_system_icon = Image.open("Image/ai-powered-models.png").resize((20, 20))
        self.train_system_icon = ImageTk.PhotoImage(self.train_system_icon)

        # Create the "Train System" button with the icon on the left, including padding (padx)
        self.train_system_button = Button(self.main_left_frame, text="Train System", command=self.training_data, bg="orange", fg="white", font=("League_Spartan"),
                                        image=self.train_system_icon, compound="left", padx=10, relief="flat", bd=2)
        self.train_system_button.place(x=0, y=390, width=220, height=40)  # Positioned above the "Image Storage" button

        # Keep a reference to the "Train System" image to prevent garbage collection
        self.train_system_button.image = self.train_system_icon

        # Load the hover image for "Train System" button
        self.train_system_icon_hover = Image.open("Image/ai-powered-models (1).png").resize((20, 20))
        self.train_system_icon_hover = ImageTk.PhotoImage(self.train_system_icon_hover)

        # Bind events for hover effect (change color and image when mouse hovers)
        self.train_system_button.bind("<Enter>", lambda event: on_enter(event, self.train_system_button, self.original_bg, self.hover_bg, self.original_fg, self.hover_fg, self.train_system_icon_hover))
        self.train_system_button.bind("<Leave>", lambda event: on_leave(event, self.train_system_button, self.original_bg, self.original_fg, self.train_system_icon))

       
        # Load and resize the image for the "Image Storage" button
        self.image_storage_icon = Image.open("Image/database.png").resize((20, 20))
        self.image_storage_icon = ImageTk.PhotoImage(self.image_storage_icon)

        # Create the "Image Storage" button with the icon on the left, including padding (padx)
        self.image_storage_button = Button(self.main_left_frame, text="Image Storage", command=self.open_image, bg="orange", fg="white", font=("League_Spartan"),
                                        image=self.image_storage_icon, compound="left", padx=10, relief="flat", bd=2)
        self.image_storage_button.place(x=0, y=440, width=220, height=40)  # Positioned above the "Admin Setting" button

        # Keep a reference to the "Image Storage" image to prevent garbage collection
        self.image_storage_button.image = self.image_storage_icon

        # Load the hover image for "Image Storage" button
        self.image_storage_icon_hover = Image.open("Image/database (1).png").resize((20, 20))
        self.image_storage_icon_hover = ImageTk.PhotoImage(self.image_storage_icon_hover)

        # Bind events for hover effect (change color and image when mouse hovers)
        self.image_storage_button.bind("<Enter>", lambda event: on_enter(event, self.image_storage_button, self.original_bg, self.hover_bg, self.original_fg, self.hover_fg, self.image_storage_icon_hover))
        self.image_storage_button.bind("<Leave>", lambda event: on_leave(event, self.image_storage_button, self.original_bg, self.original_fg, self.image_storage_icon))

        


        # Load and resize the image for the "Admin Setting" button
        self.admin_setting_icon = Image.open("Image/setting.png").resize((20, 20))
        self.admin_setting_icon = ImageTk.PhotoImage(self.admin_setting_icon)

        # Create the "Admin Setting" button with the icon on the left, including padding (padx)
        self.admin_setting_button = Button(self.main_left_frame, text="Admin Setting", command=lambda: self.admin_regis(username),bg="orange", fg="white", font=("League_Spartan"),
                                        image=self.admin_setting_icon, compound="left", padx=10, relief="flat", bd=2)
        self.admin_setting_button.place(x=0, y=490, width=220, height=40)  # Positioned below the "Timetable Information" button

        # Keep a reference to the "Admin Setting" image to prevent garbage collection
        self.admin_setting_button.image = self.admin_setting_icon

        # Load the hover image for "Admin Setting" button
        self.admin_setting_icon_hover = Image.open("Image/setting (1).png").resize((20, 20))
        self.admin_setting_icon_hover = ImageTk.PhotoImage(self.admin_setting_icon_hover)

        # Bind events for hover effect (change color and image when mouse hovers)
        self.admin_setting_button.bind("<Enter>", lambda event: on_enter(event, self.admin_setting_button, self.original_bg, self.hover_bg, self.original_fg, self.hover_fg, self.admin_setting_icon_hover))
        self.admin_setting_button.bind("<Leave>", lambda event: on_leave(event, self.admin_setting_button, self.original_bg, self.original_fg, self.admin_setting_icon))




        # Load the logout icon
        self.logout_icon = Image.open("Image/logout.png").resize((20, 20))
        self.logout_icon = ImageTk.PhotoImage(self.logout_icon)

        # Create the "Logout" button with the icon on the left, including padding (padx)
        self.logout_button = Button(self.main_left_frame, text="Logout", command=self.logout,bg="red", fg="white", font=("Arial", 12, "bold"),
                                    image=self.logout_icon, compound="left", padx=10, relief="flat", bd=2)
        self.logout_button.place(x=0, y=530, width=220, height=40)  # Place the button at the bottom

        # Keep a reference to the "Logout" image to prevent garbage collection
        self.logout_button.image = self.logout_icon

        # Load the hover image for the "Logout" button
        self.logout_icon_hover = Image.open("Image/logout.png").resize((20, 20))
        self.logout_icon_hover = ImageTk.PhotoImage(self.logout_icon_hover)

        # Bind events for hover effect (change color and image when mouse hovers)
        self.logout_button.bind("<Enter>", lambda event: on_enter(event, self.logout_button, self.original_bg_logout, "red", self.original_fg, "white", self.logout_icon_hover))
        self.logout_button.bind("<Leave>", lambda event: on_leave(event, self.logout_button, self.original_bg_logout, self.original_fg, self.logout_icon))

#----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

        # Create the first frame
        self.student_frame = Frame(background_img_main_position, bd=2, bg="orange")
        self.student_frame.place(x=240, y=80, width=250, height=100)


        # Load and place the student image in the frame
        self.add_image_to_frame(
            frame=self.student_frame,
            image_path="Image/students.png",
            x=10, y=10, width=80, height=80
        )

        # Add a label to the frame
        self.student_label = Label(self.student_frame,text="Student",bg="orange",fg="White",font=("Arial", 15, "bold"))
        self.student_label.place(x=110, y=10, width=80, height=40)

        # Function to get the number of students from the database
        def get_student_count():
            # Connect to MySQL database
            conn = mysql.connector.connect(
                host="localhost",
                user="root",
                password="Nightcore_1134372019!",
                database="attendnow"
            )
            cursor = conn.cursor()

            # Execute the query to count distinct student IDs
            cursor.execute("SELECT COUNT(DISTINCT student_id) FROM students")
            result = cursor.fetchone()
            student_count = result[0] if result else 0

            # Close the connection
            cursor.close()
            conn.close()

            return student_count

        # Get the student count from the database
        student_count = get_student_count()

        # Add the second label to display the student count below the student label
        self.student_count_label = Label(self.student_frame, text=f"{student_count}", bg="orange", fg="White", font=("Arial", 20))
        self.student_count_label.place(x=110, y=50, width=80, height=40)

#----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

        # Create the second frame
        self.teacher_frame = Frame(background_img_main_position, bd=2, bg="orange")
        self.teacher_frame.place(x=240 + 250 + 10, y=80, width=250, height=100)

        # Load and place the student image in the frame
        self.add_image_to_frame(
            frame=self.teacher_frame,
            image_path="Image/teacher.png",
            x=10, y=10, width=80, height=80
        )

        # Add a label to the frame
        self.teacher_label = Label(self.teacher_frame,text="Teacher",bg="orange",fg="White",font=("Arial", 15, "bold"))
        self.teacher_label.place(x=110, y=10, width=80, height=40)

        # Function to get the number of teachers from the database
        def get_teacher_count():
            # Connect to MySQL database
            conn = mysql.connector.connect(
                host="localhost",
                user="root",
                password="Nightcore_1134372019!",
                database="attendnow"
            )
            cursor = conn.cursor()

            # Execute the query to count distinct teacher usernames
            cursor.execute("SELECT COUNT(DISTINCT user_name) FROM teacher_user")
            result = cursor.fetchone()
            teacher_count = result[0] if result else 0

            # Close the connection
            cursor.close()
            conn.close()

            return teacher_count

        # Get the teacher count from the database
        teacher_count = get_teacher_count()

        # Add the second label to display the teacher count below the teacher label
        self.teacher_count_label = Label(self.teacher_frame, text=f"{teacher_count}", bg="orange", fg="White", font=("Arial", 20))
        self.teacher_count_label.place(x=110, y=50, width=80, height=40)
#----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

        # Create the third frame
        self.course_frame = Frame(background_img_main_position, bd=2, bg="orange")
        self.course_frame.place(x=240 + (250 + 10) * 2, y=80, width=250, height=100)

        # Load and place the course image in the frame
        self.add_image_to_frame(
            frame=self.course_frame,
            image_path="Image/education.png",
            x=10, y=10, width=80, height=80
        )

        # Add a label to the frame
        self.course_label = Label(self.course_frame,text="Course",bg="orange",fg="White",font=("Arial", 15, "bold"))
        self.course_label.place(x=110, y=10, width=80, height=40)

        # Function to get the number of courses from the database
        def get_course_count():
            # Connect to MySQL database
            conn = mysql.connector.connect(
                host="localhost",
                user="root",
                password="Nightcore_1134372019!",
                database="attendnow"
            )
            cursor = conn.cursor()

            # Execute the query to count the courses in the curriculum table
            cursor.execute("SELECT COUNT(course) FROM curriculum")
            result = cursor.fetchone()
            course_count = result[0] if result else 0

            # Close the connection
            cursor.close()
            conn.close()

            return course_count

        # Get the course count from the database
        course_count = get_course_count()

        # Add the second label to display the course count below the course label
        self.course_count_label = Label(self.course_frame, text=f"{course_count}", bg="orange", fg="White", font=("Arial", 20))
        self.course_count_label.place(x=110, y=50, width=80, height=40)
#----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

        # Create a frame named "Facial Testing System" with the specified position and size
        self.facial_testing_frame = Frame(background_img_main_position, width=320, height=220, bg="orange", bd=2)
        self.facial_testing_frame.place(x=240, y=190)

        # Add a label at the top left of the frame with the specified font and colors
        label = Label(self.facial_testing_frame, text="Facial Testing System", bg="orange", fg="white", font=("Arial", 12, "bold"))
        label.place(x=10, y=10)

        # Load the first image (electronics.png) using PIL (Pillow)
        image_path_1 = "Image/electronics.png"
        image_1 = Image.open(image_path_1)  # Open the image file
        image_1 = image_1.resize((120, 120))  # Resize the image to 120x120 pixels
        photo_1 = ImageTk.PhotoImage(image_1)  # Convert the image to a Tkinter-compatible format

        # Load the hover image for the first image
        hover_image_path_1 = "Image/electronics (1).png"
        hover_image_1 = Image.open(hover_image_path_1)  # Open the hover image
        hover_image_1 = hover_image_1.resize((120, 120))  # Resize the hover image
        hover_photo_1 = ImageTk.PhotoImage(hover_image_1)  # Convert the hover image to Tkinter-compatible format

        
        def on_image_1_hover_in(event):
            image_button_1.config(image=hover_photo_1, bg="white")  # Change image and background on hover

        def on_image_1_hover_out(event):
            image_button_1.config(image=photo_1, bg="orange")  # Revert image and background when hover ends

        image_button_1 = Button(self.facial_testing_frame, image=photo_1, command=lambda: self.face_page(username),bg="orange", bd=0, highlightthickness=0)
        image_button_1.place(x=20, y=50)  # Position the first image below the label

        # Bind hover events to the first image button
        image_button_1.bind("<Enter>", on_image_1_hover_in)  # On hover in
        image_button_1.bind("<Leave>", on_image_1_hover_out)  # On hover out

        # Add a label below the first image (Face Recognition)
        label_1 = Label(self.facial_testing_frame, text="Face Recognition", bg="orange", fg="white", font=("Arial", 10, "bold"))
        label_1.place(x=20, y=180)  # Position label below the first image

        # Keep a reference to the first image to prevent it from being garbage collected
        image_button_1.image = photo_1

        # Load the second image (observation.png) using PIL (Pillow)
        image_path_2 = "Image/observation.png"
        image_2 = Image.open(image_path_2)  # Open the image file
        image_2 = image_2.resize((120, 120))  # Resize the image to 120x120 pixels
        photo_2 = ImageTk.PhotoImage(image_2)  # Convert the image to Tkinter-compatible format

        # Load the hover image for the second image
        hover_image_path_2 = "Image/observation (1).png"
        hover_image_2 = Image.open(hover_image_path_2)  # Open the hover image
        hover_image_2 = hover_image_2.resize((120, 120))  # Resize the hover image
        hover_photo_2 = ImageTk.PhotoImage(hover_image_2)  # Convert the hover image to Tkinter-compatible format

        def on_image_2_hover_in(event):
            image_button_2.config(image=hover_photo_2, bg="white")  # Change image and background on hover

        def on_image_2_hover_out(event):
            image_button_2.config(image=photo_2, bg="orange")  # Revert image and background when hover ends

        image_button_2 = Button(self.facial_testing_frame, image=photo_2, command=lambda: self.emotion_detection_button(username),bg="orange", bd=0, highlightthickness=0)
        image_button_2.place(x=180, y=50)  # Position the second image to the right side of the frame

        # Bind hover events to the second image button
        image_button_2.bind("<Enter>", on_image_2_hover_in)  # On hover in
        image_button_2.bind("<Leave>", on_image_2_hover_out)  # On hover out

        # Add a label below the second image (Emotion Detection)
        label_2 = Label(self.facial_testing_frame, text="Emotion Detection", bg="orange", fg="white", font=("Arial", 10, "bold"))
        label_2.place(x=180, y=180)  # Position label below the second image

        # Keep a reference to the second image to prevent it from being garbage collected
        image_button_2.image = photo_2

#----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
        # Create a new frame named "Report/Status" on the right side
        self.report_status_frame = Frame(background_img_main_position, width=440, height=220, bg="orange", bd=2)
        self.report_status_frame.place(x=570, y=190)  # Position it to the right of the "Facial Testing System" frame

         # Add a label at the top left of the frame with the specified font and colors
        label = Label(self.report_status_frame, text="Status / Report", bg="orange", fg="white", font=("Arial", 12, "bold"))
        label.place(x=10, y=10)
       
        # Image 1: Emotion Status
        image_path_3 = "Image/mind.png"
        image_3 = Image.open(image_path_3)
        image_3 = image_3.resize((120, 120))
        photo_3 = ImageTk.PhotoImage(image_3)

        hover_image_path_3 = "Image/mind (1).png"
        hover_image_3 = Image.open(hover_image_path_3)
        hover_image_3 = hover_image_3.resize((120, 120))
        hover_photo_3 = ImageTk.PhotoImage(hover_image_3)


        def on_image_3_hover_in(event):
            image_button_3.config(image=hover_photo_3, bg="white")

        def on_image_3_hover_out(event):
            image_button_3.config(image=photo_3, bg="orange")

        image_button_3 = Button(self.report_status_frame, image=photo_3, command=lambda: self.attendance_summary(username),bg="orange", bd=0, highlightthickness=0)
        image_button_3.place(x=20, y=50)

        image_button_3.bind("<Enter>", on_image_3_hover_in)
        image_button_3.bind("<Leave>", on_image_3_hover_out)

        label_3 = Label(self.report_status_frame, text="Emotion Status", bg="orange", fg="white", font=("Arial", 10, "bold"))
        label_3.place(x=20, y=180)

        image_button_3.image = photo_3  # Keep a reference to the first image

        # Image 2: Attendance Status
        image_path_4 = "Image/attendance.png"
        image_4 = Image.open(image_path_4)
        image_4 = image_4.resize((120, 120))
        photo_4 = ImageTk.PhotoImage(image_4)

        hover_image_path_4 = "Image/attendance (1).png"
        hover_image_4 = Image.open(hover_image_path_4)
        hover_image_4 = hover_image_4.resize((120, 120))
        hover_photo_4 = ImageTk.PhotoImage(hover_image_4)

        def on_image_4_hover_in(event):
            image_button_4.config(image=hover_photo_4, bg="white")

        def on_image_4_hover_out(event):
            image_button_4.config(image=photo_4, bg="orange")

        image_button_4 = Button(self.report_status_frame, image=photo_4, command=lambda: self.attendance_status(username),bg="orange", bd=0, highlightthickness=0)
        image_button_4.place(x=160, y=50)

        image_button_4.bind("<Enter>", on_image_4_hover_in)
        image_button_4.bind("<Leave>", on_image_4_hover_out)

        label_4 = Label(self.report_status_frame, text="Attendance Status", bg="orange", fg="white", font=("Arial", 10, "bold"))
        label_4.place(x=160, y=180)

        image_button_4.image = photo_4  # Keep a reference to the second image

        # Image 3: Generate Report
        image_path_5 = "Image/finance-and-business.png"
        image_5 = Image.open(image_path_5)
        image_5 = image_5.resize((120, 120))
        photo_5 = ImageTk.PhotoImage(image_5)

        hover_image_path_5 = "Image/finance-and-business (1).png"
        hover_image_5 = Image.open(hover_image_path_5)
        hover_image_5 = hover_image_5.resize((120, 120))
        hover_photo_5 = ImageTk.PhotoImage(hover_image_5)

        def on_image_5_hover_in(event):
            image_button_5.config(image=hover_photo_5, bg="white")

        def on_image_5_hover_out(event):
            image_button_5.config(image=photo_5, bg="orange")

        image_button_5 = Button(self.report_status_frame, image=photo_5, command=lambda: self.generate_report(username),bg="orange", bd=0, highlightthickness=0)
        image_button_5.place(x=300, y=50)

        image_button_5.bind("<Enter>", on_image_5_hover_in)
        image_button_5.bind("<Leave>", on_image_5_hover_out)

        label_5 = Label(self.report_status_frame, text="Generate Report", bg="orange", fg="white", font=("Arial", 10, "bold"))
        label_5.place(x=300, y=180)

        image_button_5.image = photo_5  # Keep a reference to the third image

#----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

       

        

#----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    def training_data(self):
        try:
            
            subprocess.run(["python", "data_training.py"], check=True)
        except subprocess.CalledProcessError as e:
            print(f"An error occurred while running data_training.py: {e}")

    def open_image(self):
        os.startfile("data")
    
    def generate_report(self, username):
        self.root.destroy()  
        new_window = Tk()
        report_generater.Report_Generater(new_window, username)
    
    def attendance_status(self, username):
        self.root.destroy() 
        new_window = Tk()
        attendance_status_interface.Attendance_Status_Interface(new_window, username)

    def attendance_summary(self, username):
        self.root.destroy()
        new_window = Tk()
        emotion_status_interface.Emotion_Status_Interface(new_window, username)

    def emotion_detection_button(self, username):
        self.root.destroy()
        new_window = Tk()
        emotion_detection.Emotion_Detection(new_window, username)
    
    def face_page(self, username):
        self.root.destroy()
        new_window = Tk()
        face_recognition.Face_Recognition(new_window, username)

    def logout(self):
        self.root.destroy()  
        new_window = Tk()  
        login_page.Login_Page(new_window)

    def admin_regis(self, username):
        self.root.destroy()
        new_window =Tk()
        admin_register.Admin_Register(new_window,username)
    
    def timetable(self, username):
        self.root.destroy()
        new_window = Tk()
        timetable.Timetable_Information(new_window, username)

    def open_curriculum(self, username):
        self.root.destroy()
        new_window = Tk()
        curriculum.Curriculum_Interface(new_window, username)
    
    def open_teacher_info(self, username):
        self.root.destroy()
        new_window = Tk()
        teacher.Teacher_Interface(new_window, username)
    
    def student_detail(self, username):
            self.root.destroy()
            new_window = Tk()
            student.Student(new_window, username)


    def add_image_to_frame(self, frame, image_path, x, y, width, height):
        """
        Add an image to the specified frame.
        """
        image = Image.open(image_path)
        resized_image = image.resize((width, height))  # Resize the image to fit the specified dimensions
        photo = ImageTk.PhotoImage(resized_image)

        # Add the image to a Label and place it in the frame
        image_label = Label(frame, image=photo, bg="orange")
        image_label.place(x=x, y=y, width=width, height=height)

        # Keep the reference to the image to avoid garbage collection
        image_label.image = photo
    #-------------------------------------------------------------------------------------

if __name__ == "__main__":
    root = Tk()
    root.resizable(False, False)
    obj = Admit_Interface(root, "Imran Adil Oyong Muhammad")  
    root.mainloop()
