from tkinter import *
from tkinter import ttk  # For Treeview
from PIL import Image, ImageTk
import mysql.connector
from datetime import datetime
import cv2
import json
import admit_interface
import mediapipe as mp
import os

with open(r".vscode\settings.json") as file:
    settings = json.load(file)
connection_details = settings["sqltools.connections"][0]

class Face_Recognition:
    def __init__(self, root, username):
        self.root = root
        self.username = username 
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
        main_frame.place(x=300, y=5, width=400, height=50)

        # Add the text label in the center of the main_frame
        Label(main_frame, text="Face Recognition", bg="orange", fg="white", font=("New Time Roman", 20, "bold")).place(relx=0.5, rely=0.5, anchor=CENTER)

        # Create a dropdown menu (Combobox)
        self.teacher_input = ttk.Combobox(background_img_face_recognition_position, width=28, state="readonly")
        self.teacher_input['values'] = ["Teacher 1", "Teacher 2", "Teacher 3"]  # Add teacher names here
        self.teacher_input.place(x=80, y=100, width=310)  # Position the dropdown above the Start button

        # Start Face Recognition Button
        face_recognition_button = Button(background_img_face_recognition_position, command=self.face_recog, text="Start Face Recognition")
        face_recognition_button.place(x=80, y=140, width=150, height=40)  # Position below the dropdown

        # Stop Face Recognition Button (next to the Start button)
        stop_button = Button(background_img_face_recognition_position, command=self.stop_recog, text="Stop Face Recognition", bg="red", fg="white")
        stop_button.place(x=240, y=140, width=150, height=40)  # Next to the Start button

        # Video display area on the right of the buttons
        self.video_label = Label(background_img_face_recognition_position)
        self.video_label.place(x=400, y=100, width=600, height=400)  # Position for video display

        # Create a frame for the Treeview and scrollbar
        tree_frame = Frame(self.root)
        tree_frame.place(x=80, y=200, width=310, height=250)

        # Create a table for displaying the student name and ID
        self.tree = ttk.Treeview(tree_frame, columns=("ID", "Name", "Start Time", "End Time"), show='headings', height=8)
        self.tree.heading("ID", text="Student ID")
        self.tree.heading("Name", text="Student Name")
        self.tree.heading("Start Time", text="Start Time")
        self.tree.heading("End Time", text="End Time")
        self.tree.column("ID", anchor=CENTER, width=100)
        self.tree.column("Name", anchor=CENTER, width=200)
        self.tree.column("Start Time", anchor=CENTER, width=100)
        self.tree.column("End Time", anchor=CENTER, width=100)

        # Create a horizontal scrollbar
        scrollbar = ttk.Scrollbar(tree_frame, orient="horizontal", command=self.tree.xview)
        self.tree.configure(xscrollcommand=scrollbar.set)

        self.tree.pack(side=TOP, fill=BOTH, expand=True)  # Adjusted packing
        scrollbar.pack(side=BOTTOM, fill=X)  # Pack scrollbar at the bottom

        self.attendance_records = {}  # To track start times
        self.student_present = set()  # Track recognized students
        self.video_cap = None  # Video capture object
        self.student_data = {}  # Dictionary to hold student info
        self.load_student_data()  # Load student data from the database

        self.username_label = Label(self.root, text=f"Logged in as: {self.username}", bg="orange", fg="white", font=("Arial", 12))
        self.username_label.place(x=820, y=15)
        
        return_button = Button(self.root, text="Back", command=self.return_to_admit_interface, bg="blue", fg="white", font=("Arial", 12, "bold"))
        return_button.place(x=170, y=15, width=80, height=30)

    def return_to_admit_interface(self):
        self.root.destroy()  # Close the student interface
        new_window = Tk()  # Create a new Tk window for the admit interface
        admit_interface.Admit_Interface(new_window, self.username)
    
    def mark_attendance(self, id, student_name, is_end=False):
        now = datetime.now()
        dtString = now.strftime("%H:%M:%S")

        if is_end:
            # Record end time
            if id in self.attendance_records:
                start_time = self.attendance_records[id]
                self.tree.item(id, values=(id, student_name, start_time, dtString))
                del self.attendance_records[id]  # Remove from the record
        else:
            # Record start time
            if id not in self.attendance_records:
                self.attendance_records[id] = dtString
                # Add student info to the table
                self.tree.insert('', 'end', values=(id, student_name, dtString, ""))

    def load_student_data(self):
        # Connect to the database and fetch student data
        try:
            connection = mysql.connector.connect(
                host="localhost",
                user="root",
                password="Nightcore_1134372019!",
                database="attendnow"
            )
            cursor = connection.cursor()
            cursor.execute("SELECT student_id, student_name FROM student")
            for (student_id, student_name) in cursor.fetchall():
                self.student_data[student_id] = student_name  # Store student data in the dictionary
            cursor.close()
            connection.close()
        except mysql.connector.Error as err:
            print(f"Error: {err}")

    def face_recog(self):
        # Initialize MediaPipe Face Detection
        self.mp_face_detection = mp.solutions.face_detection
        self.face_detection = self.mp_face_detection.FaceDetection(min_detection_confidence=0.5)

        self.video_cap = cv2.VideoCapture(0)
        self.recognize()

    def recognize(self):
        ret, img = self.video_cap.read()
        if not ret:
            self.video_cap.release()
            return

        # Convert the image to RGB
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        results = self.face_detection.process(img_rgb)

        # Draw face detection annotations on the image
        if results.detections:
            for detection in results.detections:
                bboxC = detection.location_data.relative_bounding_box
                ih, iw, _ = img.shape
                bbox = int(bboxC.xmin * iw), int(bboxC.ymin * ih), int(bboxC.width * iw), int(bboxC.height * ih)
                cv2.rectangle(img, bbox, (0, 255, 0), 3)

                # Placeholder logic for recognition
                student_id = self.get_student_id(bbox)  # Get student ID based on bounding box
                if student_id in self.student_data:
                    student_name = self.student_data[student_id]
                    confidence = 95  # Placeholder confidence

                    if confidence > 77:
                        cv2.putText(img, f"Name: {student_name}", (bbox[0], bbox[1] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)
                        if student_id not in self.student_present:
                            self.student_present.add(student_id)
                            self.mark_attendance(student_id, student_name)  # Record start time
                    else:
                        cv2.putText(img, "Unknown Student", (bbox[0], bbox[1] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 0, 0), 2)

            # Update the display
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            img = Image.fromarray(img)
            img = img.resize((600, 400), Image.Resampling.LANCZOS)
            self.photo_img = ImageTk.PhotoImage(img)
            self.video_label.configure(image=self.photo_img)
            self.video_label.image = self.photo_img

        self.video_label.after(10, self.recognize)  # Call the recognize method again

    def get_student_id(self, bbox):
        # Placeholder method to get student ID based on bounding box
        # Implement the logic to map the detected face to a student ID
        return "some_id"  # Replace with actual logic

    def stop_recog(self):
        if self.video_cap is not None:
            self.video_cap.release()
        self.mp_face_detection = None  # Cleanup
        self.student_present.clear()  # Clear recognized students
        self.tree.delete(*self.tree.get_children())  # Clear the attendance table

if __name__ == "__main__":
    root = Tk()
    app = Face_Recognition(root, "SampleUsername")  # Use a sample username
    root.mainloop()
