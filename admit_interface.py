from tkinter import *
from tkinter import ttk 
from PIL import Image, ImageTk
from student import Student
from data_training import Data_Training
from face_recognition import Face_Recognition
import os


class Admit_Interface:
    def __init__(self,root):
        self.root=root
        self.root.geometry("1024x590+0+0")
        self.root.title("AttendNow")

    #Background Image
        background_img_main=Image.open(r"Image\Background.png")
        background_img_main=background_img_main.resize((1024, 590),Image.Resampling.LANCZOS)
        self.photo_background_img_main=ImageTk.PhotoImage(background_img_main)
        background_img_main_position=Label(self.root,image=self.photo_background_img_main)
        background_img_main_position.place(x=0,y=0,width=1024,height=590)

    #LogoTitle Image
        left_title=Image.open(r"Image\LogoTitle_Left Top.png")     
        self.photoleft_title=ImageTk.PhotoImage(left_title)
        left_title_position=Label(self.root,image=self.photoleft_title)
        left_title_position.place(x=0,y=0,width=163,height=60)

        main_frame2=Frame(background_img_main_position,bd=2,bg="orange")
        main_frame2.place(x=200,y=5,width=700,height=50)

        save_button=Label(main_frame2,text="Admin Interface",bg="orange",fg="white",font=("New Time Roman", 20, "bold"))
        save_button.place(x=5,y=2 ,width=600,height=40)


    
    #Navigation Bar

        main_frame=Frame(background_img_main_position,bd=2,bg="white")
        main_frame.place(x=200,y=100,width=650,height=50)

        student_information=Button(main_frame,text="Student Information",command=self.student_detail,bg="orange",fg="white",font=("League_Spartan"))
        student_information.place(x=5,y=2 ,width=150,height=40)

        train_data=Button(main_frame,text="Train Data",command=self.training_data,bg="orange",fg="white",font=("League_Spartan"))
        train_data.place(x=160,y=2,width=150,height=40)

        storage_image=Button(main_frame,text="Storage",command=self.open_image,bg="orange",fg="white",font=("League_Spartan"))
        storage_image.place(x=315,y=2,width=150,height=40)

        face_recon=Button(main_frame,text="Face Recognition",command=self.face_page,bg="orange",fg="white",font=("League_Spartan"))
        face_recon.place(x=470,y=2,width=150,height=40)
        





       

    

#========================Function Button==============================
    
    def open_image(self):
        os.startfile("data")
    
    def training_data(self):
        self.new_window=Toplevel(self.root)
        self.app=Data_Training(self.new_window)
        

    def student_detail(self):
        self.new_window=Toplevel(self.root)
        self.app=Student(self.new_window)

    def face_page(self):
        self.new_window=Toplevel(self.root)
        self.app=Face_Recognition(self.new_window)
        
        
if __name__ == "__main__":
    root=Tk()
    obj=Admit_Interface(root)
    root.mainloop()
