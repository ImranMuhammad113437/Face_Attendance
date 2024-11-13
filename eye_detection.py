from tkinter import *
from PIL import Image, ImageTk
import admit_interface
import cv2
import time

class Eye_Detection:
    def __init__(self, root, username):
        self.root = root
        self.username = username
        self.root.geometry("1024x590")
        self.root.title("AttendNow - Eye Detection")
        self.root.resizable(False, False)

        
        background_img_eye_detection = Image.open(r"Image\Background.png")
        background_img_eye_detection = background_img_eye_detection.resize((1024, 590), Image.Resampling.LANCZOS)
        self.photo_background_img_eye_detection = ImageTk.PhotoImage(background_img_eye_detection)
        background_img_eye_detection_position = Label(self.root, image=self.photo_background_img_eye_detection)
        background_img_eye_detection_position.place(x=0, y=0, width=1024, height=590)

        
        left_title = Image.open(r"Image\LogoTitle_Left Top.png")
        self.photoleft_title = ImageTk.PhotoImage(left_title)
        left_title_position = Label(self.root, image=self.photoleft_title)
        left_title_position.place(x=0, y=0, width=163, height=60)

        
        main_frame = Frame(background_img_eye_detection_position, bd=2, bg="orange")
        main_frame.place(x=300, y=5, width=400, height=50)

        
        Label(main_frame, text="Eye Detection", bg="orange", fg="white", font=("New Time Roman", 20, "bold")).place(relx=0.5, rely=0.5, anchor=CENTER)

        
        start_eye_detection_button = Button(background_img_eye_detection_position, command=self.eye_detection, text="Start Eye Detection", bg="orange", fg="white", font=("Arial", 12, "bold"))
        start_eye_detection_button.place(x=80, y=80, width=150, height=40) 

        
        stop_eye_detection_button = Button(background_img_eye_detection_position, command=self.stop_detection, text="Stop Eye Detection", bg="red", fg="white", font=("Arial", 12, "bold"))
        stop_eye_detection_button.place(x=240, y=80, width=150, height=40)

        
        self.video_label = Label(background_img_eye_detection_position)
        self.video_label.place(x=400, y=80, width=600, height=500)

        
        return_button = Button(self.root, text="Back", command=self.return_to_admit_interface, bg="blue", fg="white", font=("Arial", 12, "bold"))
        return_button.place(x=170, y=15, width=80, height=30)

        
        self.username_label = Label(self.root, text=f"Logged in as: {self.username}", bg="orange", fg="white", font=("Arial", 12))
        self.username_label.place(x=820, y=15)

        self.video_cap = None  
        self.eyes_closed_start_time = None  
        self.eyes_closed_duration_threshold = 10  

    def eye_detection(self):
        
        eye_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_eye.xml')
        self.video_cap = cv2.VideoCapture(0)
        self.detect_eyes(eye_cascade)

    def detect_eyes(self, eye_cascade):
        ret, img = self.video_cap.read()
        if not ret:
            self.video_cap.release()
            return

        gray_image = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        eyes = eye_cascade.detectMultiScale(gray_image, scaleFactor=1.1, minNeighbors=10, minSize=(20, 20))

        if len(eyes) == 0:
            
            if self.eyes_closed_start_time is None:
                self.eyes_closed_start_time = time.time()

            
            eyes_closed_duration = time.time() - self.eyes_closed_start_time

            if eyes_closed_duration >= self.eyes_closed_duration_threshold:
                cv2.putText(img, "Asleep/Not Paying Attention", (20, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
            else:
                cv2.putText(img, f"Eyes closed for {int(eyes_closed_duration)} sec", (20, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2)
        else:
            
            cv2.putText(img, "Awake", (20, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            self.eyes_closed_start_time = None  

        for (x, y, w, h) in eyes:
            cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 3)
            cv2.putText(img, "Eye Detected", (x, y - 10), cv2.FONT_HERSHEY_COMPLEX, 0.8, (255, 255, 255), 2)

        
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        img_pil = Image.fromarray(img_rgb)
        imgtk = ImageTk.PhotoImage(image=img_pil)

        
        self.video_label.imgtk = imgtk
        self.video_label.configure(image=imgtk)

        
        self.video_label.after(10, lambda: self.detect_eyes(eye_cascade))

    def stop_detection(self):
        if self.video_cap:
            self.video_cap.release()
        self.video_label.config(image="")  

    def return_to_admit_interface(self):
        self.root.destroy()  
        new_window = Tk()  
        admit_interface.Admit_Interface(new_window, self.username)

if __name__ == "__main__":
    root = Tk()
    obj = Eye_Detection(root, "Guest")  
    root.mainloop()
