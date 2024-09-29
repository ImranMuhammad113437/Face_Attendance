from tkinter import *  # Ensure you import Tk, Button, Frame, Toplevel, etc.
from PIL import Image, ImageTk
import os
import login_page  # Import the login_page module for logout functionality
from student import Student  # Import the Student class from student.py
import student
import face_recognition
import curriculum
import data_training
import subprocess

class Admit_Interface:
    def __init__(self, root, username):
        self.root = root
        self.root.geometry("1024x590+0+0")
        self.root.title("AttendNow")

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

        # Logout Button (next to the logo)
        logout_button = Button(self.root, text="Logout", command=self.logout, bg="red", fg="white", font=("Arial", 12, "bold"))
        logout_button.place(x=175, y=15, width=80, height=30)

        # Main Frame for Admin Interface
        main_frame2 = Frame(background_img_main_position, bd=2, bg="orange")
        main_frame2.place(x=300, y=5, width=400, height=50)

        save_button = Label(main_frame2, text="Admin Interface", bg="orange", fg="white", font=("New Time Roman", 20, "bold"))
        save_button.place(x=5, y=2, width=400, height=40)

        # Display username on the top right corner
        self.username_label = Label(self.root, text=f"Logged in as: {username}", bg="orange", fg="white", font=("Arial", 12))
        self.username_label.place(x=800, y=15)

        # Navigation Bar
        main_frame = Frame(background_img_main_position, bd=2, bg="white")
        main_frame.place(x=200, y=100, width=650, height=180)  # Adjusted height for additional buttons

        student_information = Button(main_frame, text="Student Information", command=lambda: self.student_detail(username), bg="orange", fg="white", font=("League_Spartan"))
        student_information.place(x=5, y=2, width=150, height=40)

        # Curriculum Button below Student Information
        curriculum_button = Button(main_frame, text="Curriculum", command=lambda: self.open_curriculum(username), bg="orange", fg="white", font=("League_Spartan"))
        curriculum_button.place(x=5, y=50, width=150, height=40)

        train_data = Button(main_frame, text="Train Data", command=self.training_data, bg="orange", fg="white", font=("League_Spartan"))
        train_data.place(x=160, y=2, width=150, height=40)

        # Teacher Information Button below "Train Data"
        teacher_info_button = Button(main_frame, text="Teacher Information", command=self.open_teacher_info, bg="orange", fg="white", font=("League_Spartan"))
        teacher_info_button.place(x=160, y=50, width=150, height=40)

        storage_image = Button(main_frame, text="Storage", command=self.open_image, bg="orange", fg="white", font=("League_Spartan"))
        storage_image.place(x=315, y=2, width=150, height=40)

        # New Eye Detection Button below "Storage"
        eye_detection_button = Button(main_frame, text="Eye Detection", command=self.eye_detection, bg="orange", fg="white", font=("League_Spartan"))
        eye_detection_button.place(x=315, y=50, width=150, height=40)  # Positioned below "Storage"

        face_recon = Button(main_frame, text="Face Recognition", command=lambda: self.face_page(username), bg="orange", fg="white", font=("League_Spartan"))
        face_recon.place(x=470, y=2, width=150, height=40)

        # New Emotion Detection Button below "Face Recognition"
        emotion_detection_button = Button(main_frame, text="Emotion Detection", command=self.emotion_detection, bg="orange", fg="white", font=("League_Spartan"))
        emotion_detection_button.place(x=470, y=50, width=150, height=40)  # Positioned below "Face Recognition"

    # Function Buttons
    def open_image(self):
        os.startfile("data")

    def training_data(self):
        try:
            # Run the data_training.py script
            subprocess.run(["python", "data_training.py"], check=True)
        except subprocess.CalledProcessError as e:
            print(f"An error occurred while running data_training.py: {e}")
    
    def eye_detection(self):
        self.root.destroy()  # Close the current interface window
        os.system('python eye_detection.py')

    def emotion_detection(self):
        print("Emotion Detection button clicked")
        # Add functionality for emotion detection here

    # Add the new function for Teacher Information
    def open_teacher_info(self):
        print("Teacher Information button clicked")
        # Add functionality for opening teacher information here

    def student_detail(self, username):
        self.root.destroy()
        new_window = Tk()
        student.Student(new_window, username)

    def face_page(self, username):
        self.root.destroy()
        new_window = Tk()
        face_recognition.Face_Recognition(new_window, username)

    def open_curriculum(self, username):
        self.root.destroy()
        new_window = Tk()
        curriculum.Curriculum_Interface(new_window, username)

    # Logout Function
    def logout(self):
        self.root.destroy()  # Close the admit_interface window
        new_window = Tk()  # Create a new Tk window
        login_page.Login_Page(new_window)  # Open the login page again


if __name__ == "__main__":
    root = Tk()
    root.resizable(False, False)
    obj = Admit_Interface(root, "Guest")  # Replace "Guest" with actual username
    root.mainloop()
