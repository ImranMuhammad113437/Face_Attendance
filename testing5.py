import tkinter as tk
from tkinter import Label, Button
import cv2
import mediapipe as mp
from PIL import Image, ImageTk

class EmotionDetection:
    def __init__(self, root):
        self.root = root
        self.root.geometry("1024x590")
        self.root.title("Emotion Detection")

        # MediaPipe Face Detection
        self.mp_face_mesh = mp.solutions.face_mesh
        self.face_mesh = self.mp_face_mesh.FaceMesh(min_detection_confidence=0.5)

        # Video Capture
        self.video_cap = cv2.VideoCapture(0)

        # Video Display Area
        self.video_label = Label(root)
        self.video_label.place(x=400, y=100, width=600, height=400)

        # Start/Stop Button
        self.start_button = Button(root, text="Start Emotion Detection", command=self.start_detection)
        self.start_button.place(x=80, y=100, width=200, height=40)

        self.stop_button = Button(root, text="Stop Emotion Detection", command=self.stop_detection)
        self.stop_button.place(x=80, y=160, width=200, height=40)

        # Emotion result label
        self.emotion_label = Label(root, text="Detected Emotion: ", font=("Arial", 14))
        self.emotion_label.place(x=80, y=220, width=200, height=40)

        # Emotion percentage labels
        self.sad_label = Label(root, text="Sad: 0%", font=("Arial", 12))
        self.sad_label.place(x=80, y=260, width=200, height=30)
        
        self.happy_label = Label(root, text="Happy: 0%", font=("Arial", 12))
        self.happy_label.place(x=80, y=290, width=200, height=30)
        
        self.neutral_label = Label(root, text="Neutral: 0%", font=("Arial", 12))
        self.neutral_label.place(x=80, y=320, width=200, height=30)
        
        self.fear_label = Label(root, text="Fear: 0%", font=("Arial", 12))
        self.fear_label.place(x=80, y=350, width=200, height=30)
        
        self.surprise_label = Label(root, text="Surprise: 0%", font=("Arial", 12))
        self.surprise_label.place(x=80, y=380, width=200, height=30)
        
        self.angry_label = Label(root, text="Angry: 0%", font=("Arial", 12))
        self.angry_label.place(x=80, y=410, width=200, height=30)

        self.running = False

    def start_detection(self):
        self.running = True
        self.detect_emotion()

    def stop_detection(self):
        self.running = False
        self.video_cap.release()
        self.video_label.config(image='')
        self.emotion_label.config(text="Detected Emotion: ")  # Reset emotion label
        # Reset emotion percentages
        self.reset_emotion_percentages()

    def reset_emotion_percentages(self):
        self.sad_label.config(text="Sad: 0%")
        self.happy_label.config(text="Happy: 0%")
        self.neutral_label.config(text="Neutral: 0%")
        self.fear_label.config(text="Fear: 0%")
        self.surprise_label.config(text="Surprise: 0%")
        self.angry_label.config(text="Angry: 0%")

    def detect_emotion(self):
        if not self.running:
            return

        ret, frame = self.video_cap.read()
        if not ret:
            return

        # Convert the image to RGB
        img_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Process the frame with MediaPipe
        results = self.face_mesh.process(img_rgb)

        # Draw the face mesh on the image
        if results.multi_face_landmarks:
            for face_landmarks in results.multi_face_landmarks:
                for landmark in face_landmarks.landmark:
                    ih, iw, _ = img_rgb.shape
                    x = int(landmark.x * iw)
                    y = int(landmark.y * ih)
                    cv2.circle(img_rgb, (x, y), 1, (255, 0, 0), -1)

        # Here you can replace this with your actual emotion detection logic
        # For now, using fixed emotion percentages for demonstration
        detected_emotion = "Happy"  # Placeholder for detected emotion
        self.emotion_label.config(text=f"Detected Emotion: {detected_emotion}")

        # Fixed percentages for demonstration
        percentages = {
            "Sad": 10,
            "Happy": 70,
            "Neutral": 10,
            "Fear": 5,
            "Surprise": 3,
            "Angry": 2
        }

        # Update emotion percentage labels
        self.sad_label.config(text=f"Sad: {percentages['Sad']}%")
        self.happy_label.config(text=f"Happy: {percentages['Happy']}%")
        self.neutral_label.config(text=f"Neutral: {percentages['Neutral']}%")
        self.fear_label.config(text=f"Fear: {percentages['Fear']}%")
        self.surprise_label.config(text=f"Surprise: {percentages['Surprise']}%")
        self.angry_label.config(text=f"Angry: {percentages['Angry']}%")

        # Convert the image to ImageTk format for Tkinter display
        img_rgb = cv2.cvtColor(img_rgb, cv2.COLOR_RGB2BGR)
        img_pil = Image.fromarray(img_rgb)
        imgtk = ImageTk.PhotoImage(image=img_pil)

        # Update video feed in the Tkinter interface
        self.video_label.imgtk = imgtk
        self.video_label.configure(image=imgtk)

        # Continuously update the video feed
        self.video_label.after(10, self.detect_emotion)

if __name__ == "__main__":
    root = tk.Tk()
    app = EmotionDetection(root)
    root.mainloop()
