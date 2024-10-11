from tkinter import *
from tkinter import messagebox
import cv2
import mediapipe as mp
import os
from PIL import Image, ImageTk  # Importing Image and ImageTk

class FaceCapture:
    def __init__(self, root):
        self.root = root
        self.root.geometry("400x300")
        self.root.title("Face Capture for Students")

        self.mp_face_detection = mp.solutions.face_detection
        self.face_detection = self.mp_face_detection.FaceDetection(min_detection_confidence=0.5)
        
        # Create folder for saving images if it doesn't exist
        self.data_folder = "data2"
        if not os.path.exists(self.data_folder):
            os.makedirs(self.data_folder)

        # Name Input
        Label(self.root, text="Student Name:").pack(pady=10)
        self.name_entry = Entry(self.root)
        self.name_entry.pack(pady=5)

        # ID Input
        Label(self.root, text="Student ID:").pack(pady=10)
        self.id_entry = Entry(self.root)
        self.id_entry.pack(pady=5)

        # Capture Button
        self.capture_button = Button(self.root, text="Capture Face", command=self.capture_face)
        self.capture_button.pack(pady=20)

        # Video Capture
        self.video_cap = cv2.VideoCapture(0)

        # Start Video
        self.show_video()

    def show_video(self):
        ret, img = self.video_cap.read()
        if ret:
            img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            results = self.face_detection.process(img_rgb)

            if results.detections:
                for detection in results.detections:
                    bboxC = detection.location_data.relative_bounding_box
                    ih, iw, _ = img.shape
                    bbox = int(bboxC.xmin * iw), int(bboxC.ymin * ih), int(bboxC.width * iw), int(bboxC.height * ih)
                    cv2.rectangle(img, bbox, (0, 255, 0), 3)

            # Convert image to a format suitable for Tkinter
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            img_pil = Image.fromarray(img)
            imgtk = ImageTk.PhotoImage(image=img_pil)

            # Display the video feed in Tkinter
            self.video_label = Label(self.root, image=imgtk)
            self.video_label.imgtk = imgtk
            self.video_label.place(x=0, y=0)
            self.video_label.after(10, self.show_video)

    def capture_face(self):
        name = self.name_entry.get()
        student_id = self.id_entry.get()

        if not name or not student_id:
            messagebox.showerror("Input Error", "Please enter both name and ID.")
            return

        ret, img = self.video_cap.read()
        if ret:
            file_name = f"{self.data_folder}/user.{student_id}.1.jpg"  # You can change the number based on your logic
            cv2.imwrite(file_name, img)
            messagebox.showinfo("Success", f"Face captured and saved as {file_name}.")
            self.name_entry.delete(0, END)
            self.id_entry.delete(0, END)

    def __del__(self):
        self.video_cap.release()

if __name__ == "__main__":
    root = Tk()
    app = FaceCapture(root)
    root.mainloop()
