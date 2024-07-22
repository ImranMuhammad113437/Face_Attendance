from tkinter import *
from tkinter import ttk
from PIL import Image, ImageTk
from tkinter import messagebox
import mysql.connector
from time import strftime
from datetime import datetime
import cv2
import csv
import os
import numpy as np
import json


with open(r".vscode\settings.json") as file:
    settings = json.load(file)
connection_details = settings["sqltools.connections"][0]


class Face_Recognition:
    def __init__(self,root):
        self.root=root
        self.root.geometry("1024x590")
        self.root.title("AttendNow")
        
        #Background Image
        background_img_face_recognition=Image.open(r"Image\Background.png")
        background_img_face_recognition=background_img_face_recognition.resize((1024, 590),Image.Resampling.LANCZOS)
        self.photo_background_img_face_recognition=ImageTk.PhotoImage(background_img_face_recognition)
        background_img_face_recognition_position=Label(self.root,image=self.photo_background_img_face_recognition)
        background_img_face_recognition_position.place(x=0,y=0,width=1024,height=590)

        #LogoTitle Image
        left_title=Image.open(r"Image\LogoTitle_Left Top.png")     
        self.photoleft_title=ImageTk.PhotoImage(left_title)
        left_title_position=Label(self.root,image=self.photoleft_title)
        left_title_position.place(x=0,y=0,width=163,height=60)

        main_frame=Frame(background_img_face_recognition_position,bd=2,bg="orange")
        main_frame.place(x=200,y=5,width=700,height=50)

        save_button=Label(main_frame,text="Face Recognition",bg="orange",fg="white",font=("New Time Roman", 20, "bold"))
        save_button.place(x=5,y=2 ,width=600,height=40)


        face_recogntion_button=Button(background_img_face_recognition_position,command=self.face_recog,text="Start Face Recognition")
        face_recogntion_button.place(x=200,y=200,width=150,height=40)


    def mark_attendance(self, id, student_name):
        with open(r"Attendance.csv", "a+", newline="\n") as f:
            f.seek(0)  # Move the cursor to the start of the file
            myDataList = f.readlines()
            name_list = []
            for line in myDataList:
                entry = line.strip().split(",")
                name_list.append(entry[0])
            if id not in name_list and student_name:
                now = datetime.now()
                d1 = now.strftime("%d/%m/%Y")
                dtString = now.strftime("%H:%M:%S")
                f.write(f"{id},{student_name},{dtString},{d1},Present\n")             
        


    def face_recog(self):

        def draw_boundary(img, classifier, scaleFactor, minNeighbors, color, text, clf):
            gray_image = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            features = classifier.detectMultiScale(gray_image, scaleFactor, minNeighbors)

            coord = []

            for (x, y, w, h) in features:
                cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 3)
                id, predict = clf.predict(gray_image[y:y+h, x:x+w])
                confidence = int((100 * (1 - predict / 300)))

                conn = mysql.connector.connect(
                    host=connection_details["server"],
                    port=connection_details["port"],
                    user=connection_details["username"],
                    password=connection_details["password"],
                    database=connection_details["database"]
                )
                my_cursor = conn.cursor()

                my_cursor.execute("SELECT student_name FROM students WHERE student_id=%s", (id,))
                result = my_cursor.fetchone()
                if result:
                    student_name = result[0]
                else:
                    student_name = "Unknown"

                my_cursor.execute("SELECT department FROM students WHERE student_id=%s", (id,))
                result = my_cursor.fetchone()
                if result:
                    department = result[0]
                else:
                    department = "Unknown"

                conn.close()

                if confidence > 77:
                    cv2.putText(img, f"Name: {student_name}", (x, y - 55), cv2.FONT_HERSHEY_COMPLEX, 0.8, (255, 255, 255), 3)
                    cv2.putText(img, f"SAPID: {id}", (x, y - 30), cv2.FONT_HERSHEY_COMPLEX, 0.8, (255, 255, 255), 3)
                    self.mark_attendance(id,student_name)
                else:
                    cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 3)
                    cv2.putText(img, "Unknown Student", (x, y - 55), cv2.FONT_HERSHEY_COMPLEX, 0.8, (255, 255, 255), 3)

                coord = [x, y, w, h]

            return coord

        def recognize(img, clf, faceCascade):
            coord = draw_boundary(img, faceCascade, 1.1, 10, (255, 25, 255), "Face", clf)
            return img

        faceCascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

        clf = cv2.face.LBPHFaceRecognizer_create()
        clf.read("classifier.xml")

        video_cap = cv2.VideoCapture(0)

        while True:
            ret, img = video_cap.read()
            if not ret:
                break
            img = recognize(img, clf, faceCascade)
            cv2.imshow("Face Recognition", img)
                           
            if cv2.waitKey(1) == 13:  # Press 'Enter' key to break                                                                                                                                                                                  
                break

        video_cap.release()
        cv2.destroyAllWindows()

    # Assume connection_details is a dictionary with necessary database connection information                                            
    connection_details =settings["sqltools.connections"][0]

    # Example usage
    # face_recog(None)  # Replace `None` with appropriate argument if needed


            

                    









if __name__ == "__main__":
        root=Tk()
        obj=Face_Recognition(root)
        root.mainloop()
        root.resizable(False,False)
