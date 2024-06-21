from tkinter import *
from tkinter import ttk 
from PIL import Image, ImageTk
from student import Student

class Admit_Interface:
    def __init__(self,root):
        self.root=root
        self.root.geometry("1024x590+0+0")
        self.root.title("AttendNow")

    #Background Image
        background_img=Image.open(r"Image\Background.png")
        background_img=background_img.resize((1024, 590),Image.Resampling.LANCZOS)
        self.photo_background_img=ImageTk.PhotoImage(background_img)
        background_img_position=Label(self.root,image=self.photo_background_img)
        background_img_position.place(x=0,y=0,width=1024,height=590)

    #LogoTitle Image
        left_title=Image.open(r"Image\LogoTitle_Left Top.png")     
        self.photoleft_title=ImageTk.PhotoImage(left_title)
        left_title_position=Label(self.root,image=self.photoleft_title)
        left_title_position.place(x=0,y=0,width=163,height=60)

    
    #Navigation Bar
        
        save_button=Button(text="Student Information",command=self.student_detail,bg="orange",fg="white",font=("League_Spartan"))
        save_button.place(x=200,y=15,width=150,height=40)
    

#========================Function Buttone
    def student_detail(self):
        self.new_window=Toplevel(self.root)
        self.app=Student(self.new_window)
        
if __name__ == "__main__":
    root=Tk()
    obj=Admit_Interface(root)
    root.mainloop()
