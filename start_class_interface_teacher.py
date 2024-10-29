from tkinter import *  # Ensure you import Tk, Button, Frame, Toplevel, etc.
from PIL import Image, ImageTk
import os
import cv2  # Make sure to import OpenCV for video capture
import mysql.connector
from fer import FER
import login_page  # Import the login_page module for logout functionality
import teacher_interface
from tkinter import ttk

class Start_Class_Interface_Teacher:  # Changed class name to Teacher_Interface
    def __init__(self, root, username):
        self.root = root
        self.username = username
        self.root.geometry("1024x590+0+0")
        self.root.title("AttendNow - Teacher Interface")  # Updated title

        # ------------------------------------- Background Image-------------------------------------------------------
        background_img_main = Image.open(r"Image\Background.png")
        background_img_main = background_img_main.resize((1024, 590), Image.Resampling.LANCZOS)
        self.photo_background_img_main = ImageTk.PhotoImage(background_img_main)
        background_img_main_position = Label(self.root, image=self.photo_background_img_main)
        background_img_main_position.place(x=0, y=0, width=1024, height=590)
        # -------------------------------------------------------------------------------------------------------------

        # ------------------------------------- LogoTitle Image
        left_title = Image.open(r"Image\LogoTitle_Left Top.png")
        self.photoleft_title = ImageTk.PhotoImage(left_title)
        left_title_position = Label(self.root, image=self.photoleft_title)
        left_title_position.place(x=0, y=0, width=163, height=60)

        # Back Button (next to the logo)
        back_button = Button(self.root, text="Back", command=self.back_to_interface, bg="blue", fg="white", font=("Arial", 12, "bold"))
        back_button.place(x=175, y=15, width=80, height=30)

        # Main Frame for Teacher Interface
        main_frame = Frame(background_img_main_position, bd=2, bg="orange")
        main_frame.place(x=20, y=70, width=984, height=450)  # Adjusted dimensions for two frames

        # Create left frame for input fields
        self.input_frame = Frame(main_frame, bg="lightgray")
        self.input_frame.pack(side=LEFT, padx=(0, 10), fill=BOTH, expand=True)  # Right padding for gap

        # Create right frame for video display with fixed width and height
        self.video_frame = Frame(main_frame, bg="darkgray")
        self.video_frame.place(x=574, y=0, width=400, height=450)  # Adjusted to fix width and height


        

        # Frame for dropdown label and combobox in one row
        dropdown_frame = Frame(self.input_frame, bg="lightgray")
        dropdown_frame.pack(pady=5)

        # Dropdown menu (Combobox) for selecting an option in one row
        dropdown_label = Label(dropdown_frame, text="Select Course:", bg="lightgray", fg="black", font=("Arial", 12))
        dropdown_label.pack(side=LEFT, padx=5)

        self.course_combobox = ttk.Combobox(dropdown_frame, values=["Math", "Physics", "Computer Science", "English"], state="readonly")
        self.course_combobox.pack(side=LEFT, padx=5)
        self.course_combobox.set("Select a course")  # Set default text



        # "Start" Button to start face recognition
        start_button = Button(self.input_frame, text="Start", bg="green", fg="white", font=("Arial", 12, "bold"), command=self.face_recog)
        start_button.pack(pady=10)

        # "End" Button to stop face recognition
        end_button = Button(self.input_frame, text="End", bg="red", fg="white", font=("Arial", 12, "bold"))
        end_button.pack(pady=10)

        # Display username on the top right corner
        self.username_label = Label(self.root, text=f"Logged in as: {username}", bg="orange", fg="white", font=("Arial", 12))
        self.username_label.place(x=800, y=15)

        # Video Label inside video_frame
        self.video_label = Label(self.video_frame, bg="darkgray")
        self.video_label.pack(fill=BOTH, expand=True)  # Fill the video frame with the video label

    # Face recognition function
    def face_recog(self):
        # Load the face detection classifier
        faceCascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

        # Load the face recognition model
        clf = cv2.face.LBPHFaceRecognizer_create()
        clf.read("classifier.xml")

        # Initialize the emotion detector
        emotion_detector = FER()

        # Start video capture for face recognition
        self.video_cap = cv2.VideoCapture(0)
        self.recognize(faceCascade, clf, emotion_detector)

    # Recognition process
    def recognize(self, faceCascade, clf, emotion_detector):
        ret, img = self.video_cap.read()
        if not ret:
            self.video_cap.release()
            return

        gray_image = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        features = faceCascade.detectMultiScale(gray_image, scaleFactor=1.1, minNeighbors=10)

        for (x, y, w, h) in features:
            cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 3)  # Draw rectangle around face
            id, predict = clf.predict(gray_image[y:y + h, x:x + w])
            confidence = int((100 * (1 - predict / 300)))

            conn = mysql.connector.connect(
                host="localhost",
                user="root",
                password="Nightcore_1134372019!",
                database="attendnow"
            )
            my_cursor = conn.cursor()

            # Retrieve student name and ID based on student ID
            my_cursor.execute("SELECT student_name, student_id FROM students WHERE student_id=%s", (id,))
            result = my_cursor.fetchone()
            student_name = result[0] if result else "Unknown"
            student_id = result[1] if result else "Unknown"

            conn.close()

            # Emotion detection on the cropped face
            face_img = img[y:y + h, x:x + w]
            emotions = emotion_detector.detect_emotions(face_img)

            if emotions:
                dominant_emotion = max(emotions[0]['emotions'], key=emotions[0]['emotions'].get)
            else:
                dominant_emotion = "No emotion detected"

            # Add text overlay on video frame for face recognition and emotion detection
            if confidence > 70:
                cv2.putText(img, f"Name: {student_name}", (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)
                cv2.putText(img, f"ID: {student_id}", (x, y + h + 30), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)
                cv2.putText(img, f"Emotion: {dominant_emotion}", (x, y + h + 60), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255, 0, 0), 2)
            else:
                cv2.putText(img, "Unknown", (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 0, 255), 2)

        # Convert OpenCV image to ImageTk format for Tkinter display
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        img_pil = Image.fromarray(img_rgb)
        imgtk = ImageTk.PhotoImage(image=img_pil)

        # Update video feed in the Tkinter interface (inside video_frame)
        self.video_label.imgtk = imgtk
        self.video_label.configure(image=imgtk)

        # Continuously update the video feed
        self.video_label.after(10, lambda: self.recognize(faceCascade, clf, emotion_detector))

    def back_to_interface(self):
        self.root.destroy()
        new_window = Tk()  # Create a new Tk window
        teacher_interface.Teacher_Interface(new_window, self.username)


if __name__ == "__main__":
    root = Tk()
    root.resizable(False, False)
    obj = Start_Class_Interface_Teacher(root, "Jackie Chan")  # Replace "Jackie Chan" with the actual username
    root.mainloop()
