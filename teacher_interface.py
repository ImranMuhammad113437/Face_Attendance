from tkinter import *  
from PIL import Image, ImageTk
import os
import login_page  
import face_recognition_teacher
import emotion_status_interface_teacher
import eye_detection
import emotion_detection_teacher
import attendance_status_interface_teacher
import report_generater_interface_teacher
import start_class_interface_teacher

class Teacher_Interface:  
    def __init__(self, root, username):
        self.root = root
        self.root.geometry("1024x590+0+0")
        self.root.title("AttendNow - Teacher Interface")  


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

        save_button = Label(main_frame2, text="Teacher Interface", bg="orange", fg="white", font=("New Time Roman", 20, "bold"))
        save_button.place(x=5, y=2, width=400, height=40)

        
        self.username_label = Label(self.root, text=f"Logged in as: {username}", bg="orange", fg="white", font=("Arial", 12))
        self.username_label.place(x=800, y=15)

        
        main_frame = Frame(background_img_main_position, bd=2, bg="orange")
        main_frame.place(x=190, y=100, width=670, height=400)  



       
        facial_system_frame = LabelFrame(main_frame, text="Facial System", bg="orange", font=("Arial", 12, "bold"),fg="white", bd=0, highlightbackground="white", highlightcolor="white")
        facial_system_frame.place(x=10, y=10, width=650, height=100)

        
        face_recon = Button(facial_system_frame, text="Face Recognition", command=lambda: self.face_page(username), bg="orange", fg="white", font=("League_Spartan"))
        face_recon.place(x=5, y=10, width=150, height=40)

        eye_detection_button = Button(facial_system_frame, text="Eye Detection", command=lambda: self.eye_detection(username), bg="orange", fg="white", font=("League_Spartan"))
        eye_detection_button.place(x=160, y=10, width=150, height=40)

        emotion_detection_button = Button(facial_system_frame, text="Emotion Detection", command=lambda: self.emotion_detection_button(username), bg="orange", fg="white", font=("League_Spartan"))
        emotion_detection_button.place(x=315, y=10, width=150, height=40)

        
        new_feature_button = Button(facial_system_frame, text="Start Class", command=lambda: self.new_feature(username), bg="orange", fg="white", font=("League_Spartan"))
        new_feature_button.place(x=470, y=10, width=150, height=40)  



        
        information_status_frame = LabelFrame(main_frame, text="Information Status",  bg="orange", font=("Arial", 12, "bold"),fg="white", bd=0, highlightbackground="white", highlightcolor="white")
        information_status_frame.place(x=10, y=120, width=650, height=100)

        attendance_summary_button = Button(information_status_frame, text="Emotional Status", command=lambda: self.attendance_summary(username), bg="orange", fg="white", font=("League_Spartan"))
        attendance_summary_button.place(x=5, y=10, width=150, height=40)

        attendance_status_button = Button(information_status_frame, text="Attendance Status", command=lambda: self.attendance_status(username), bg="orange", fg="white", font=("League_Spartan"))
        attendance_status_button.place(x=160, y=10, width=150, height=40)

        
        generate_report_button = Button(information_status_frame, text="Generate Report", command=lambda: self.generate_report(username),bg="orange", fg="white", font=("League_Spartan"))
        generate_report_button.place(x=315, y=10, width=150, height=40)


    def new_feature(self, username):
        self.root.destroy()
        new_window = Tk()
        start_class_interface_teacher.Start_Class_Interface_Teacher(new_window, username)


    def generate_report(self, username):
        self.root.destroy()  
        new_window = Tk()
        report_generater_interface_teacher.Report_Generater_Interface_Teacher(new_window, username)

    def attendance_status(self, username):
        self.root.destroy()  
        new_window = Tk()
        attendance_status_interface_teacher.Attendance_Status_Interface_Teacher(new_window, username)
        

    
    def eye_detection(self, username):
        self.root.destroy()  
        new_window = Tk()
        eye_detection.Eye_Detection(new_window, username)

    def emotion_detection_button(self, username):
        self.root.destroy()
        new_window = Tk()
        emotion_detection_teacher.Emotion_Detection_Teacher(new_window, username)

    
    def face_page(self, username):
        self.root.destroy()
        new_window = Tk()
        face_recognition_teacher.Face_Recognition_Teacher(new_window, username)

    def attendance_summary(self, username):
        self.root.destroy()
        new_window = Tk()
        emotion_status_interface_teacher.Emotion_Status_Interface_Teacher(new_window, username)

    
    def logout(self):
        self.root.destroy()
        new_window = Tk()  
        login_page.Login_Page(new_window)




if __name__ == "__main__":
    root = Tk()
    root.resizable(False, False)
    obj = Teacher_Interface(root, "Jackie Chan")  
    root.mainloop()
