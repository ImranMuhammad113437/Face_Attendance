from tkinter import *
from tkinter import messagebox
import cv2
import mediapipe as mp
import os
import numpy as np
from PIL import Image, ImageTk  # Ensure to import these

class FaceRecognition:
    def __init__(self, root):
        self.root = root
        self.root.geometry("640x480")  # Set the window size
        self.root.title("Face Recognition for Students")

        self.mp_face_detection = mp.solutions.face_detection
        self.face_detection = self.mp_face_detection.FaceDetection(min_detection_confidence=0.5)

        self.data_folder = "data2"
        self.known_faces = {}
        self.load_known_faces()

        # Button to start recognition
        self.recognition_button = Button(self.root, text="Start Recognition", command=self.start_recognition)
        self.recognition_button.pack(pady=20)

        # Video Capture
        self.video_cap = cv2.VideoCapture(0)  # Initialize video capture

        # Start Video
        self.show_video()

    def load_known_faces(self):
        for filename in os.listdir(self.data_folder):
            if filename.endswith(".jpg"):
                student_id = filename.split('.')[1]  # Assuming the format is user.ID.num.jpg
                img_path = os.path.join(self.data_folder, filename)
                image = cv2.imread(img_path)
                rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
                results = self.face_detection.process(rgb_image)

                if results.detections:
                    # Assuming the first detection is the one we want to save
                    self.known_faces[student_id] = rgb_image

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

            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            img = Image.fromarray(img)
            imgtk = ImageTk.PhotoImage(image=img)

            # Display the video feed in Tkinter
            self.video_label = Label(self.root, image=imgtk)
            self.video_label.imgtk = imgtk
            self.video_label.place(x=0, y=0)
            self.video_label.after(10, self.show_video)

    def start_recognition(self):
        recognized = False
        ret, img = self.video_cap.read()
        if ret:
            rgb_image = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            results = self.face_detection.process(rgb_image)

            if results.detections:
                for detection in results.detections:
                    bboxC = detection.location_data.relative_bounding_box
                    ih, iw, _ = img.shape
                    bbox = int(bboxC.xmin * iw), int(bboxC.ymin * ih), int(bboxC.width * iw), int(bboxC.height * ih)

                    # Extract the face from the frame
                    face_image = rgb_image[bbox[1]:bbox[1] + bbox[3], bbox[0]:bbox[0] + bbox[2]]

                    # Compare with known faces
                    for student_id, known_face in self.known_faces.items():
                        # Assuming that the comparison is done by calculating the mean square error (MSE)
                        mse = np.mean((face_image - known_face) ** 2)
                        if mse < 1000:  # Set a threshold for recognizing the face
                            messagebox.showinfo("Recognition Successful", f"Student ID: {student_id}\nStudent Name: {student_id}")
                            recognized = True
                            break

            if not recognized:
                messagebox.showwarning("Recognition Failed", "No matching student found.")

    def __del__(self):
        self.video_cap.release()  # Release video capture when the object is destroyed

if __name__ == "__main__":
    root = Tk()
    app = FaceRecognition(root)
    root.mainloop()
