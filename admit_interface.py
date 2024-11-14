from tkinter import * 
from PIL import Image, ImageTk
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

        left_title = Image.open(r"Image\LogoTitle_Left Top.png")
        self.photoleft_title = ImageTk.PhotoImage(left_title)
        left_title_position = Label(self.root, image=self.photoleft_title)
        left_title_position.place(x=0, y=0, width=163, height=60)

        
        logout_button = Button(self.root, text="Logout", command=self.logout, bg="red", fg="white", font=("Arial", 12, "bold"))
        logout_button.place(x=175, y=15, width=80, height=30)

       
        main_frame2 = Frame(background_img_main_position, bd=2, bg="orange")
        main_frame2.place(x=300, y=5, width=400, height=50)

        save_button = Label(main_frame2, text="Admin Interface", bg="orange", fg="white", font=("New Time Roman", 20, "bold"))
        save_button.place(x=5, y=2, width=400, height=40)

       
        self.username_label = Label(self.root, text=f"Logged in as: {username}", bg="orange", fg="white", font=("Arial", 12))
        self.username_label.place(x=800, y=15)

        
        main_frame = Frame(background_img_main_position, bd=2, bg="orange")
        main_frame.place(x=190, y=100, width=670, height=450)  

       
        facial_system_frame = LabelFrame(main_frame, text="Facial System", bg="orange", font=("Arial", 12, "bold"),fg="white", bd=0, highlightbackground="white", highlightcolor="white")
        facial_system_frame.place(x=10, y=10, width=650, height=100)

    
        face_recon = Button(facial_system_frame, text="Face Recognition", command=lambda: self.face_page(username), bg="orange", fg="white", font=("League_Spartan"))
        face_recon.place(x=5, y=10, width=150, height=40)

        eye_detection_button = Button(facial_system_frame, text="Eye Detection", command=lambda: self.eye_detection(username), bg="orange", fg="white", font=("League_Spartan"))
        eye_detection_button.place(x=160, y=10, width=150, height=40)

        emotion_detection_button = Button(facial_system_frame, text="Emotion Detection", command=lambda: self.emotion_detection_button(username), bg="orange", fg="white", font=("League_Spartan"))
        emotion_detection_button.place(x=315, y=10, width=150, height=40)

         
        train_data = Button(facial_system_frame, text="Train Data", command=self.training_data, bg="orange", fg="white", font=("League_Spartan"))
        train_data.place(x=470, y=10, width=150, height=40)


        information_management_frame = LabelFrame(main_frame, text="Information Management",  bg="orange", font=("Arial", 12, "bold"),fg="white", bd=0, highlightbackground="white", highlightcolor="white")
        information_management_frame.place(x=10, y=120, width=650, height=100)


        student_information = Button(information_management_frame, text="Student Details", command=lambda: self.student_detail(username), bg="orange", fg="white", font=("League_Spartan"))
        student_information.place(x=5, y=10, width=150, height=40)

        teacher_info_button = Button(information_management_frame, text="Faculty Info", command=lambda: self.open_teacher_info(username), bg="orange", fg="white", font=("League_Spartan"))
        teacher_info_button.place(x=160, y=10, width=150, height=40)

        curriculum_button = Button(information_management_frame, text="Curriculum Overview", command=lambda: self.open_curriculum(username), bg="orange", fg="white", font=("League_Spartan"))
        curriculum_button.place(x=315, y=10, width=150, height=40)

        timetable_button = Button(information_management_frame, text="Schedule Details", command=lambda: self.timetable(username), bg="orange", fg="white", font=("League_Spartan"))
        timetable_button.place(x=470, y=10, width=150, height=40)


        information_status_frame = LabelFrame(main_frame, text="Information Status",  bg="orange", font=("Arial", 12, "bold"),fg="white", bd=0, highlightbackground="white", highlightcolor="white")
        information_status_frame.place(x=10, y=230, width=650, height=100)

        storage_image = Button(information_status_frame, text="Storage", command=self.open_image, bg="orange", fg="white", font=("League_Spartan"))
        storage_image.place(x=5, y=10, width=150, height=40)

        attendance_summary_button = Button(information_status_frame, text="Emotional Status", command=lambda: self.attendance_summary(username), bg="orange", fg="white", font=("League_Spartan"))
        attendance_summary_button.place(x=160, y=10, width=150, height=40)

        attendance_status_button = Button(information_status_frame, text="Attendance Status", command=lambda: self.attendance_status(username), bg="orange", fg="white", font=("League_Spartan"))
        attendance_status_button.place(x=315, y=10, width=150, height=40)

   
        generate_report_button = Button(information_status_frame, text="Generate Report", command=lambda: self.generate_report(username),bg="orange", fg="white", font=("League_Spartan"))
        generate_report_button.place(x=475, y=10, width=150, height=40)

        administration_information_frame = LabelFrame(main_frame, text="Administration Information" ,bg="orange", font=("Arial", 12, "bold"), fg="white", bd=0, highlightbackground="white", highlightcolor="white")
        administration_information_frame.place(x=10, y=340, width=650, height=100)

        # Admin Registration Button in the new frame
        admin_registration_button = Button(administration_information_frame, text="Admin Registration", command=lambda: self.admin_regis(username), bg="orange", fg="white", font=("League_Spartan"))
        admin_registration_button.place(x=5, y=10, width=150, height=40)


    def admin_regis(self, username):
        self.root.destroy()
        new_window =Tk()
        admin_register.Admin_Register(new_window,username)

    def generate_report(self, username):
        self.root.destroy()  
        new_window = Tk()
        report_generater.Report_Generater(new_window, username)

    def attendance_status(self, username):
        self.root.destroy() 
        new_window = Tk()
        attendance_status_interface.Attendance_Status_Interface(new_window, username)
        
    def open_image(self):
        os.startfile("data")

    def training_data(self):
        try:
            
            subprocess.run(["python", "data_training.py"], check=True)
        except subprocess.CalledProcessError as e:
            print(f"An error occurred while running data_training.py: {e}")
    
    def eye_detection(self, username):
        self.root.destroy()  
        new_window = Tk()
        eye_detection.Eye_Detection(new_window, username)

    def emotion_detection_button(self, username):
        self.root.destroy()
        new_window = Tk()
        emotion_detection.Emotion_Detection(new_window, username)

   
    def open_teacher_info(self, username):
        self.root.destroy()
        new_window = Tk()
        teacher.Teacher_Interface(new_window, username)

    def student_detail(self, username):
        self.root.destroy()
        new_window = Tk()
        student.Student(new_window, username)

    def face_page(self, username):
        self.root.destroy()
        new_window = Tk()
        face_recognition.Face_Recognition(new_window, username)

    def attendance_summary(self, username):
        self.root.destroy()
        new_window = Tk()
        emotion_status_interface.Emotion_Status_Interface(new_window, username)
        


    def open_curriculum(self, username):
        self.root.destroy()
        new_window = Tk()
        curriculum.Curriculum_Interface(new_window, username)

    def timetable(self, username):
        self.root.destroy()
        new_window = Tk()
        timetable.Timetable_Information(new_window, username)

    
    def logout(self):
        self.root.destroy()  
        new_window = Tk()  
        login_page.Login_Page(new_window)  


if __name__ == "__main__":
    root = Tk()
    root.resizable(False, False)
    obj = Admit_Interface(root, "Guest")  
    root.mainloop()
