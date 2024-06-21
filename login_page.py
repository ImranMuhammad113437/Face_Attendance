from tkinter import *
from tkinter import ttk 
from PIL  import Image, ImageTk


class Face_Attendance:
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

        #Title of the System
        
        title=Image.open(r"Image\Title.png")     
        self.phototitle=ImageTk.PhotoImage(title)
        f_lbl=Label(self.root,image=self.phototitle)
        f_lbl.place(x=251,y=267,width=275,height=57)

        logo=Image.open(r"Image\Background.png")     
        self.photologo=ImageTk.PhotoImage(logo)
        f_lbl=Label(self.root,image=self.photologo)
        f_lbl.place(x=100,y=222,width=150,height=150)

if __name__ == "__main__":
    root=Tk()
    obj=Face_Attendance(root)
    root.mainloop()