from tkinter import *
from PIL import Image, ImageTk
import mysql.connector
from datetime import datetime
import cv2
import csv
import json

with open(r".vscode\settings.json") as file:
    settings = json.load(file)
connection_details = settings["sqltools.connections"][0]

class Face_Recognition:
    def __init__(self, root):
        self.root = root
        self.root.geometry("1024x590")
        self.root.title("AttendNow")

        # Background Image
        background_img_face_recognition = Image.open(r"Image\Background.png")
        background_img_face_recognition = background_img_face_recognition.resize((1024, 590), Image.Resampling.LANCZOS)
        self.photo_background_img_face_recognition = ImageTk.PhotoImage(background_img_face_recognition)
        background_img_face_recognition_position = Label(self.root, image=self.photo_background_img_face_recognition)
        background_img_face_recognition_position.place(x=0, y=0, width=1024, height=590)

        # LogoTitle Image
        left_title = Image.open(r"Image\LogoTitle_Left Top.png")
        self.photoleft_title = ImageTk.PhotoImage(left_title)
        left_title_position = Label(self.root, image=self.photoleft_title)
        left_title_position.place(x=0, y=0, width=163, height=60)

        main_frame = Frame(background_img_face_recognition_position, bd=2, bg="orange")
        main_frame.place(x=200, y=5, width=700, height=50)

        save_button = Label(main_frame, text="Face Recognition", bg="orange", fg="white", font=("New Time Roman", 20, "bold"))
        save_button.place(x=5, y=2, width=600, height=40)

        # Start Face Recognition Button
        face_recognition_button = Button(background_img_face_recognition_position, command=self.face_recog, text="Start Face Recognition")
        face_recognition_button.place(x=200, y=200, width=150, height=40)

        # Stop Face Recognition Button (below the Start button)
        stop_button = Button(background_img_face_recognition_position, command=self.stop_recog, text="Stop Face Recognition", bg="red", fg="white")
        stop_button.place(x=200, y=250, width=150, height=40)

        # Video display area on the right of the buttons
        self.video_label = Label(background_img_face_recognition_position)
        self.video_label.place(x=400, y=100, width=600, height=400)

        self.attendance_records = {}  # To track start times
        self.student_present = set()  # Track recognized students
        self.video_cap = None  # Video capture object

    def mark_attendance(self, id, student_name, is_end=False):
        with open(r"Attendance.csv", "a+", newline="\n") as f:
            writer = csv.writer(f)
            if f.tell() == 0:  # If the file is empty, write the header
                writer.writerow(["Student's Name", "Start", "End"])

            now = datetime.now()
            dtString = now.strftime("%H:%M:%S")

            if is_end:
                # Record end time
                if id in self.attendance_records:
                    start_time = self.attendance_records[id]
                    writer.writerow([student_name, start_time, dtString])
                    del self.attendance_records[id]  # Remove from the record
            else:
                # Record start time
                if id not in self.attendance_records:
                    self.attendance_records[id] = dtString

    def face_recog(self):
        faceCascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

        clf = cv2.face.LBPHFaceRecognizer_create()
        clf.read("classifier.xml")

        self.video_cap = cv2.VideoCapture(0)
        self.recognize(faceCascade, clf)

    def recognize(self, faceCascade, clf):
        ret, img = self.video_cap.read()
        if not ret:
            self.video_cap.release()
            return

        gray_image = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        features = faceCascade.detectMultiScale(gray_image, scaleFactor=1.1, minNeighbors=10)

        for (x, y, w, h) in features:
            cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 3)
            id, predict = clf.predict(gray_image[y:y + h, x:x + w])
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
            student_name = result[0] if result else "Unknown"

            conn.close()

            if confidence > 77:
                cv2.putText(img, f"Name: {student_name}", (x, y - 55), cv2.FONT_HERSHEY_COMPLEX, 0.8, (255, 255, 255), 3)
                cv2.putText(img, f"SAPID: {id}", (x, y - 30), cv2.FONT_HERSHEY_COMPLEX, 0.8, (255, 255, 255), 3)
                if id not in self.student_present:
                    self.student_present.add(id)
                    self.mark_attendance(id, student_name)  # Record start time
            else:
                cv2.putText(img, "Unknown Student", (x, y - 55), cv2.FONT_HERSHEY_COMPLEX, 0.8, (255, 255, 255), 3)

        # Convert OpenCV image to ImageTk format for Tkinter display
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        img_pil = Image.fromarray(img_rgb)
        imgtk = ImageTk.PhotoImage(image=img_pil)

        # Update video feed in the Tkinter interface
        self.video_label.imgtk = imgtk
        self.video_label.configure(image=imgtk)

        # Continuously update the video feed
        self.video_label.after(10, lambda: self.recognize(faceCascade, clf))

    def stop_recog(self):
        if self.video_cap:
            self.video_cap.release()
        self.video_label.config(image="")  # Clear the video feed from the label

if __name__ == "__main__":
    root = Tk()
    obj = Face_Recognition(root)
    root.mainloop()
    root.resizable(False, False)
