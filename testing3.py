from tkinter import *
from PIL import Image, ImageTk
import cv2
import time
from collections import defaultdict
from fer import FER  # For facial emotion recognition
import threading

class Eye_Detection:
    def __init__(self, root, username):
        self.root = root
        self.username = username
        self.root.geometry("1200x590")  # Increased width for two video frames
        self.root.title("AttendNow - Eye Detection and Emotion Tracking")
        self.root.resizable(False, False)

        # Background Image
        background_img_eye_detection = Image.open(r"Image\Background.png")
        background_img_eye_detection = background_img_eye_detection.resize((1200, 590), Image.Resampling.LANCZOS)
        self.photo_background_img_eye_detection = ImageTk.PhotoImage(background_img_eye_detection)
        background_img_eye_detection_position = Label(self.root, image=self.photo_background_img_eye_detection)
        background_img_eye_detection_position.place(x=0, y=0, width=1200, height=590)

        # LogoTitle Image
        left_title = Image.open(r"Image\LogoTitle_Left Top.png")
        self.photoleft_title = ImageTk.PhotoImage(left_title)
        left_title_position = Label(self.root, image=self.photoleft_title)
        left_title_position.place(x=0, y=0, width=163, height=60)

        # Main Frame Title
        main_frame = Frame(background_img_eye_detection_position, bd=2, bg="orange")
        main_frame.place(x=300, y=5, width=400, height=50)

        # Title Label for Eye Detection
        Label(main_frame, text="Eye Detection & Emotion Tracking", bg="orange", fg="white", font=("New Time Roman", 20, "bold")).place(relx=0.5, rely=0.5, anchor=CENTER)

        # Start Eye Detection Button
        start_eye_detection_button = Button(background_img_eye_detection_position, command=self.start_eye_detection_thread, text="Start Eye Detection", bg="orange", fg="white", font=("Arial", 12, "bold"))
        start_eye_detection_button.place(x=80, y=80, width=150, height=40)

        # Stop Eye Detection Button
        stop_eye_detection_button = Button(background_img_eye_detection_position, command=self.stop_detection, text="Stop Eye Detection", bg="red", fg="white", font=("Arial", 12, "bold"))
        stop_eye_detection_button.place(x=240, y=80, width=150, height=40)

        # Video display area for eye detection feed
        self.eye_video_label = Label(background_img_eye_detection_position)
        self.eye_video_label.place(x=400, y=80, width=400, height=500)

        # Video display area for emotion detection feed
        self.emotion_video_label = Label(background_img_eye_detection_position)
        self.emotion_video_label.place(x=800, y=80, width=400, height=500)

        # Statistics display area for emotion tracking
        self.stats_label = Label(background_img_eye_detection_position, text="Emotion detection results will be displayed here", justify="left", bg="orange", fg="white", font=("Arial", 12))
        self.stats_label.place(x=400, y=590 - 100, width=800, height=100)

        # Back button to return to the admit interface
        return_button = Button(self.root, text="Back", command=self.return_to_admit_interface, bg="blue", fg="white", font=("Arial", 12, "bold"))
        return_button.place(x=170, y=15, width=80, height=30)

        # Display username on the top right corner
        self.username_label = Label(self.root, text=f"Logged in as: {self.username}", bg="orange", fg="white", font=("Arial", 12))
        self.username_label.place(x=1030, y=15)

        self.video_cap = None  # Video capture object
        self.is_running = False  # Flag to track if detection is running
        self.emotion_counts = defaultdict(int)  # Store emotion counts
        self.total_frames = 0  # Track the number of frames processed
        self.face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        self.emotion_detector = FER()  # Initialize FER model for emotion detection

    def start_eye_detection_thread(self):
        if not self.is_running:
            self.is_running = True
            self.video_cap = cv2.VideoCapture(0)
            threading.Thread(target=self.detect_eyes).start()
            threading.Thread(target=self.detect_emotions).start()  # Start emotion detection in a separate thread

    def detect_eyes(self):
        eye_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_eye.xml')

        while self.is_running:
            ret, img = self.video_cap.read()
            if not ret:
                break

            # Process every second frame to reduce load
            gray_image = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            eyes = eye_cascade.detectMultiScale(gray_image, scaleFactor=1.1, minNeighbors=10, minSize=(20, 20))

            if len(eyes) == 0:
                # Eyes closed
                cv2.putText(img, "Asleep/Not Paying Attention", (20, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
            else:
                # Eyes are open -> Awake
                cv2.putText(img, "Awake", (20, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

            for (x, y, w, h) in eyes:
                cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 3)
                cv2.putText(img, "Eye Detected", (x, y - 10), cv2.FONT_HERSHEY_COMPLEX, 0.8, (255, 255, 255), 2)

            # Convert OpenCV image to ImageTk format for Tkinter display
            img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            img_pil = Image.fromarray(img_rgb)
            imgtk = ImageTk.PhotoImage(image=img_pil)

            # Update video feed for eye detection in the Tkinter interface
            self.eye_video_label.imgtk = imgtk
            self.eye_video_label.configure(image=imgtk)

            # Introduce a slight delay to control the frame rate
            time.sleep(0.03)  # Adjust this value for desired frame rate

        self.video_cap.release()  # Release video capture when done

    def detect_emotions(self):
        while self.is_running:
            ret, img = self.video_cap.read()
            if not ret:
                break

            # Detect emotions in the same image
            self.track_emotions(img)

            # Convert OpenCV image to ImageTk format for Tkinter display
            img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            img_pil = Image.fromarray(img_rgb)
            imgtk = ImageTk.PhotoImage(image=img_pil)

            # Update video feed for emotion detection in the Tkinter interface
            self.emotion_video_label.imgtk = imgtk
            self.emotion_video_label.configure(image=imgtk)

            # Introduce a slight delay to control the frame rate
            time.sleep(0.03)  # Adjust this value for desired frame rate

    def track_emotions(self, img):
        gray_image = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = self.face_cascade.detectMultiScale(gray_image, scaleFactor=1.1, minNeighbors=10)

        for (x, y, w, h) in faces:
            # Detect emotion for the detected face
            face_img = img[y:y + h, x:x + w]  # Crop the face from the image
            emotion = self.detect_emotion(face_img)

            # Update emotion counts
            self.emotion_counts[emotion] += 1
            self.total_frames += 1

            # Draw the bounding box around the face
            cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)

            # Display the emotion text on the left side of the video frame
            emotion_text = f"Emotion: {emotion}"
            cv2.putText(img, emotion_text, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255, 255, 255), 2)

        # Update the statistics display
        self.update_statistics_display()

    def detect_emotion(self, img):
        # Detect emotion from the image using FER
        emotion_analysis = self.emotion_detector.detect_emotions(img)
        if emotion_analysis:
            # Extract the dominant emotion
            dominant_emotion = max(emotion_analysis[0]['emotions'], key=emotion_analysis[0]['emotions'].get)
            return dominant_emotion
        else:
            return "Neutral"  # Default to neutral if no face is detected

    def update_statistics_display(self):
        stats_text = "Emotion Counts:\n"
        for emotion, count in self.emotion_counts.items():
            stats_text += f"{emotion}: {count}\n"
        stats_text += f"Total Frames: {self.total_frames}"
        self.stats_label.config(text=stats_text)

    def stop_detection(self):
        self.is_running = False

    def return_to_admit_interface(self):
        self.root.destroy()  # Close the current window

# Example usage (ensure to initialize your Tkinter root window and create an instance of Eye_Detection)
if __name__ == "__main__":
    root = Tk()
    username = "User"  # Replace with actual username logic
    app = Eye_Detection(root, username)
    root.mainloop()
