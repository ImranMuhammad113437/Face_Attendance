from tkinter import *
from tkinter import ttk 
from PIL  import Image, ImageTk


class Student:
    def __init__(self,root):
        self.root=root
        self.root.geometry("1024x590+0+0")
        self.root.title("AttendNow")

    #Background Image
        background_img=Image.open(r"C:\Users\night\Desktop\Face_Attendance\Image\Background.png")
        background_img=background_img.resize((1024, 590),Image.Resampling.LANCZOS)
        self.photo_background_img=ImageTk.PhotoImage(background_img)
        background_img_position=Label(self.root,image=self.photo_background_img)
        background_img_position.place(x=0,y=0,width=1024,height=590)

    #LogoTitle Image
        left_title=Image.open(r"C:\Users\night\Desktop\Face_Attendance\Image\LogoTitle_Left Top.png")     
        self.photoleft_title=ImageTk.PhotoImage(left_title)
        left_title_position=Label(self.root,image=self.photoleft_title)
        left_title_position.place(x=0,y=0,width=163,height=60)
        
        main_frame=Frame(background_img_position,bd=2)
        main_frame.place(x=20,y=70,width=800,height=400)

if __name__ == "__main__":
    root=Tk()
    obj=Student(root)
    root.mainloop()