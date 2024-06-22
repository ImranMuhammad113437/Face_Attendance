from tkinter import *
from tkinter import ttk
from PIL import Image, ImageTk
from tkinter import messagebox
import mysql.connector
import cv2

import os
import numpy as np


class Data_Training:
    def __init__(self,root):
        self.root=root
        self.root.geometry("1024x590+0+0")
        self.root.title("AttendNow")\
        

        #Background Image
        background_img_data_training=Image.open(r"Image\Background.png")
        background_img_data_training=background_img_data_training.resize((1024, 590),Image.Resampling.LANCZOS)
        self.photo_background_img_data_training=ImageTk.PhotoImage(background_img_data_training)
        background_img_data_training_position=Label(self.root,image=self.photo_background_img_data_training)
        background_img_data_training_position.place(x=0,y=0,width=1024,height=590)


        #Left Side Logo
        left_title=Image.open(r"Image\LogoTitle_Left Top.png")     
        self.photoleft_title=ImageTk.PhotoImage(left_title)
        left_title_position=Label(self.root,image=self.photoleft_title)
        left_title_position.place(x=0,y=0,width=163,height=60)


        #Navigation Bar
        main_frame=Frame(background_img_data_training_position,bd=2,bg="white")
        main_frame.place(x=200,y=5,width=500,height=50)

        save_button=Button(main_frame,text="Student Information",bg="orange",fg="white",font=("League_Spartan"))
        save_button.place(x=5,y=2 ,width=150,height=40)

        train_data=Button(main_frame,text="Train Data",bg="orange",fg="white",font=("League_Spartan"))
        train_data.place(x=160,y=2,width=150,height=40)


        #button
        training_button=Button(background_img_data_training_position,command=self.train_classifier,text="Train Data")
        training_button.place(x=200,y=200,width=150,height=40)





    #--------------------------------Function-----------------------------------
    def train_classifier(self):
        data_directory = 'data'
        
        
        path = [os.path.join(data_directory, f) for f in os.listdir(data_directory)]
        faces = []
        ids = []
 
        for image in path:
         # Load the image and convert it to grayscale
            img = Image.open(image).convert('L')
            img_numpy = np.array(img, 'uint8')
         
         # Extract the ID from the filename
            try:
             id = int(os.path.split(image)[1].split('.')[1])
            except (IndexError, ValueError) as e:
                print(f"Error processing file {image}: {e}")
                continue
         
            faces.append(img_numpy)
            ids.append(id)
            cv2.imshow("Training", img_numpy)
            cv2.waitKey(1)==13
     
        ids = np.array(ids)
 
     # Train the classifier
        clf = cv2.face.LBPHFaceRecognizer_create()
        clf.train(faces, ids)
        clf.write('classifier.xml')
 








if __name__ == "__main__":
    root=Tk()
    obj=Data_Training(root)
    root.mainloop()
