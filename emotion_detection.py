from tkinter import *
from tkinter import ttk  # Import ttk for Treeview
from PIL import Image, ImageTk
import mysql.connector
from datetime import datetime
import cv2
from collections import defaultdict
import admit_interface
from fer import FER
from tkinter.ttk import Combobox  # Import FER for emotion detection

class Emotion_Detection:
    def __init__(self, root,username):
        self.root = root
        self.root.geometry("1024x590")
        self.root.title("AttendNow")


        self.username = username

        self.fetch_teacher_names()

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

        

        save_button = Label(background_img_face_recognition_position, text="Emotion Detection (Admin)", bg="orange", fg="white", font=("New Time Roman", 20, "bold"))
        save_button.place(x=300, y=5, width=400, height=50)


        # Teacher Dropdown Menu (Combobox on the left side)
        self.teacher_var = StringVar()
        self.teacher_combobox = Combobox(root, textvariable=self.teacher_var)
        self.teacher_combobox['values'] = self.teacher_names  # Populate with unique teacher names
        self.teacher_combobox.place(x=80, y=100, width=150, height=30)
        self.teacher_combobox.set("Select Teacher")  # Default text
        self.teacher_combobox.bind("<<ComboboxSelected>>", self.update_course_list)  # Bind selection event

        # Course Dropdown Menu (Combobox)
        self.course_var = StringVar()
        self.course_combobox = Combobox(root, textvariable=self.course_var)
        self.course_combobox.place(x=240, y=100, width=150, height=30)
        self.course_combobox.set("Select Course")  # Default text
        self.course_combobox.bind("<<ComboboxSelected>>", self.enable_face_recognition_button)  # Enable button on selection
        

        # Start Face Recognition Button (Initially Disabled)
        self.face_recognition_button = Button(background_img_face_recognition_position, command=self.face_recog, text="Start", state="disabled")
        self.face_recognition_button.place(x=80, y=140, width=150, height=40)

        # Stop Face Recognition Button (Initially Disabled)
        self.stop_button = Button(background_img_face_recognition_position, command=self.stop_recog, text="Stop", bg="red", fg="white", state="disabled")
        self.stop_button.place(x=240, y=140, width=150, height=40)

        # Video display area on the right of the buttons
        self.video_label = Label(background_img_face_recognition_position)
        self.video_label.place(x=400, y=100, width=600, height=400)

        # Initialize attendance and emotion tracking
        self.attendance_records = {}
        self.student_present = set()
        self.video_cap = None
        self.emotion_detector = FER()
        self.total_frames = defaultdict(int)  # Track total frames per student

        # Treeview to display the attendance and emotion details
        self.tree_frame = Frame(self.root, bd=2, relief=RIDGE)
        self.tree_frame.place(x=80, y=200, width=300, height=250)

        # Scrollbar for the Treeview
        scroll_x = Scrollbar(self.tree_frame, orient=HORIZONTAL)
        scroll_y = Scrollbar(self.tree_frame, orient=VERTICAL)
        self.attendance_table = ttk.Treeview(self.tree_frame, columns=("date", "student_name", "student_id", "start_time", "end_time", "neutral", "happy", "sad", "angry", "fear", "surprise"),
                                             xscrollcommand=scroll_x.set, yscrollcommand=scroll_y.set)
        scroll_x.pack(side=BOTTOM, fill=X)
        scroll_y.pack(side=RIGHT, fill=Y)
        scroll_x.config(command=self.attendance_table.xview)
        scroll_y.config(command=self.attendance_table.yview)

        # Defining column headings
        self.attendance_table.heading("date", text="Date")  # New Date column
        self.attendance_table.heading("student_name", text="Student Name")
        self.attendance_table.heading("student_id", text="Student ID")
        self.attendance_table.heading("start_time", text="Start Time")
        self.attendance_table.heading("end_time", text="End Time")
        self.attendance_table.heading("neutral", text="Neutral (%)")
        self.attendance_table.heading("happy", text="Happy (%)")
        self.attendance_table.heading("sad", text="Sad (%)")
        self.attendance_table.heading("angry", text="Angry (%)")
        self.attendance_table.heading("fear", text="Fear (%)")
        self.attendance_table.heading("surprise", text="Surprise (%)")

        self.attendance_table["show"] = "headings"

        # Set column widths
        self.attendance_table.column("date", width=100)  # Set width for the Date column
        self.attendance_table.column("student_name", width=150)
        self.attendance_table.column("student_id", width=100)
        self.attendance_table.column("start_time", width=120)
        self.attendance_table.column("end_time", width=120)
        self.attendance_table.column("neutral", width=80)
        self.attendance_table.column("happy", width=80)
        self.attendance_table.column("sad", width=80)
        self.attendance_table.column("angry", width=80)
        self.attendance_table.column("fear", width=80)
        self.attendance_table.column("surprise", width=80)

        self.attendance_table.pack(fill=BOTH, expand=1)

        # Store attendance data
        self.student_attendance = {}

        # Save Record Button below the Treeview
        save_record_button = Button(self.root, text="Save Record", command=self.save_record,bg="green", fg="white", font=("Arial", 12, "bold"))
        save_record_button.place(x=150, y=470, width=150, height=40)  # Adjust coordinates to place it below the Treeview

        # Display username on the top right corner
        self.username_label = Label(self.root, text=f"Logged in as: {self.username}", bg="orange", fg="white", font=("Arial", 12))
        self.username_label.place(x=800, y=15)

        # Back Button
        back_button = Button(self.root, text="Back", command=self.go_back, bg="red", fg="white", font=("Arial", 12, "bold"))
        back_button.place(x=175, y=15, width=80, height=30)


#------------------------------------------------------------------------------------------------------------------------------------
    def enable_face_recognition_button(self, event):
        # Enable the "Start Face Recognition" button if a course is selected
        if self.course_var.get() != "Select Course":
            self.face_recognition_button.config(state="normal")
            self.stop_button.config(state="normal")

    def update_course_list(self, event):
            # Get the selected teacher name
            selected_teacher = self.teacher_var.get()

            # Connect to the database and fetch courses based on the selected teacher
            try:
                connection = mysql.connector.connect(
                    host="localhost",
                    user="root",
                    password="Nightcore_1134372019!",  # replace with your actual password
                    database="attendnow"
                )

                cursor = connection.cursor()
                # Fetch courses associated with the selected teacher
                query = "SELECT DISTINCT course FROM timetable WHERE teacher_name = %s"
                cursor.execute(query, (selected_teacher,))
                courses = [row[0] for row in cursor.fetchall()]  # Extract courses into a list

                # Update the course_combobox with the fetched courses
                self.course_combobox['values'] = courses
                self.course_combobox.set("Select Course")  # Reset the default text

            except mysql.connector.Error as err:
                print(f"Error: {err}")
                self.course_combobox['values'] = []  # Empty list if there's an error

            finally:
                if connection.is_connected():
                    cursor.close()
                    connection.close()
    
    
    def fetch_teacher_names(self):
        # Connect to the database and fetch unique teacher names
        try:
            connection = mysql.connector.connect(
                host="localhost",
                user="root",
                password="Nightcore_1134372019!",  # replace with your actual password
                database="attendnow"
            )

            cursor = connection.cursor()
            cursor.execute("SELECT DISTINCT teacher_name FROM timetable")  # Fetch unique teacher names
            self.teacher_names = [row[0] for row in cursor.fetchall()]  # Extract teacher names into a list

        except mysql.connector.Error as err:
            print(f"Error: {err}")
            self.teacher_names = []  # Empty list if there's an error

        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()

    def check_selections(self, event):
        # Enable buttons if both a course and teacher are selected
        if self.course_var.get() != "Select Course" and self.teacher_var.get() != "Select Teacher":
            self.face_recognition_button.config(state="normal")
            self.stop_button.config(state="normal")
        else:
            self.face_recognition_button.config(state="disabled")
            self.stop_button.config(state="disabled")
    
    def face_recog(self):
        faceCascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        clf = cv2.face.LBPHFaceRecognizer_create()
        clf.read("classifier.xml")
        self.video_cap = cv2.VideoCapture(0)
        self.recognize(faceCascade, clf)


    def go_back(self):
        self.root.destroy() 
        new_window =Tk()
        admit_interface.Admit_Interface(new_window, self.username)

    def save_record(self):
        selected_course = self.course_var.get()

        self.stop_recog()
        try:
            # Connect to the MySQL database
            conn = mysql.connector.connect(
                host="localhost",
                user="root",
                password="Nightcore_1134372019!",
                database="attendnow"
            )
            my_cursor = conn.cursor()

            # Iterate through the Treeview to save or update each row's data into the database
            for row in self.attendance_table.get_children():
                row_values = self.attendance_table.item(row)["values"]
                
                # Extract the values
                date = row_values[0]
                student_name = row_values[1]
                student_id = row_values[2]
                neutral = row_values[5].replace("%", "")
                happy = row_values[6].replace("%", "")
                sad = row_values[7].replace("%", "")
                angry = row_values[8].replace("%", "")
                fear = row_values[9].replace("%", "")
                surprise = row_values[10].replace("%", "")

                # Check if the student record already exists in the database
                check_query = """
                    SELECT * FROM student_emotion 
                    WHERE student_name = %s AND student_id = %s AND date = %s
                """
                my_cursor.execute(check_query, (student_name, student_id, date))
                record_exists = my_cursor.fetchone()

                if record_exists:
                    # Update the existing record if found
                    update_query = """
                        UPDATE student_emotion 
                        SET neutral = %s, happy = %s, sad = %s, angry = %s, fear = %s, surprise = %s, course = %s
                        WHERE student_name = %s AND student_id = %s AND date = %s
                    """
                    update_values = (neutral, happy, sad, angry, fear, surprise, selected_course ,student_name, student_id, date)
                    my_cursor.execute(update_query, update_values)
                else:
                    # Insert a new record if no existing record is found
                    insert_query = """
                        INSERT INTO student_emotion (date, student_name, student_id, neutral, happy, sad, angry, fear, surprise, course)
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                    """
                    insert_values = (date, student_name, student_id, neutral, happy, sad, angry, fear, surprise, selected_course)
                    my_cursor.execute(insert_query, insert_values)

            # Commit the transaction
            conn.commit()
            print("Records saved or updated successfully!")
            
        except mysql.connector.Error as err:
            print(f"Error: {err}")
        finally:
            # Close the database connection
            if conn.is_connected():
                my_cursor.close()
                conn.close()



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
                host="localhost",
                user="root",
                password="Nightcore_1134372019!",
                database="attendnow"
            )
            my_cursor = conn.cursor()
            my_cursor.execute("SELECT student_name FROM students WHERE student_id=%s", (id,))
            result = my_cursor.fetchone()
            student_name = result[0] if result else "Unknown"
            conn.close()

            if confidence > 77:
                face_img = img[y:y + h, x:x + w]
                emotion = self.detect_emotion(face_img)

                cv2.putText(img, f"Name: {student_name}", (x, y - 75), cv2.FONT_HERSHEY_COMPLEX, 0.8, (255, 255, 255), 3)
                cv2.putText(img, f"SAPID: {id}", (x, y - 50), cv2.FONT_HERSHEY_COMPLEX, 0.8, (255, 255, 255), 3)
                cv2.putText(img, f"Emotion: {emotion}", (x, y - 25), cv2.FONT_HERSHEY_COMPLEX, 0.8, (255, 255, 255), 3)

                if id not in self.student_present:
                    self.student_present.add(id)
                    start_time = datetime.now().strftime("%H:%M:%S")
                    current_date = datetime.now().strftime("%Y-%m-%d")  # Get the current date
                    self.student_attendance[id] = {"student_name": student_name, "start_time": start_time, "end_time": "", "emotions": defaultdict(int)}
                    self.add_to_table(id, current_date)  # Pass current date to add_to_table
                else:
                    self.update_table(id)

                # Update emotion counts for the student and the total frames for that student
                self.student_attendance[id]["emotions"][emotion] += 1
                self.total_frames[id] += 1  # Track total frames for each student

            else:
                cv2.putText(img, "Unknown Student", (x, y - 55), cv2.FONT_HERSHEY_COMPLEX, 0.8, (255, 255, 255), 3)

        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        img_pil = Image.fromarray(img_rgb)
        imgtk = ImageTk.PhotoImage(image=img_pil)
        self.video_label.imgtk = imgtk
        self.video_label.configure(image=imgtk)
        self.video_label.after(10, lambda: self.recognize(faceCascade, clf))

    def detect_emotion(self, face_img):
        emotions = self.emotion_detector.detect_emotions(face_img)
        if emotions:
            max_emotion = max(emotions[0]["emotions"], key=emotions[0]["emotions"].get)  # Get the emotion with the highest score
            return max_emotion
        return "unknown"

    def add_to_table(self, student_id, date):
        student_data = self.student_attendance[student_id]
        emotions = student_data["emotions"]

        # Calculate the total frames for percentage calculation
        total_frames = self.total_frames[student_id]

        # Calculate percentage for each emotion
        if total_frames > 0:
            neutral_percent = (emotions["neutral"] / total_frames) * 100
            happy_percent = (emotions["happy"] / total_frames) * 100
            sad_percent = (emotions["sad"] / total_frames) * 100
            angry_percent = (emotions["angry"] / total_frames) * 100
            fear_percent = (emotions["fear"] / total_frames) * 100
            surprise_percent = (emotions["surprise"] / total_frames) * 100
        else:
            neutral_percent = happy_percent = sad_percent = angry_percent = fear_percent = surprise_percent = 0.0

        # Add the row to the Treeview
        self.attendance_table.insert("", "end", values=(date, student_data["student_name"], student_id, student_data["start_time"], student_data["end_time"],
                                                         f"{neutral_percent:.2f}%", f"{happy_percent:.2f}%", f"{sad_percent:.2f}%", 
                                                         f"{angry_percent:.2f}%", f"{fear_percent:.2f}%", f"{surprise_percent:.2f}%"))

    def update_table(self, student_id):
        student_data = self.student_attendance[student_id]
        emotions = student_data["emotions"]

        # Calculate the total frames for percentage calculation
        total_frames = self.total_frames[student_id]

        # Calculate percentage for each emotion
        if total_frames > 0:
            neutral_percent = (emotions["neutral"] / total_frames) * 100
            happy_percent = (emotions["happy"] / total_frames) * 100
            sad_percent = (emotions["sad"] / total_frames) * 100
            angry_percent = (emotions["angry"] / total_frames) * 100
            fear_percent = (emotions["fear"] / total_frames) * 100
            surprise_percent = (emotions["surprise"] / total_frames) * 100
        else:
            neutral_percent = happy_percent = sad_percent = angry_percent = fear_percent = surprise_percent = 0.0

        # Update the row in the Treeview
        for item in self.attendance_table.get_children():
            if self.attendance_table.item(item)["values"][1] == student_data["student_name"] and self.attendance_table.item(item)["values"][2] == student_id:
                # Update end time if the student is present
                student_data["end_time"] = datetime.now().strftime("%H:%M:%S")
                self.attendance_table.item(item, values=(self.attendance_table.item(item)["values"][0], student_data["student_name"], student_id, 
                                                         student_data["start_time"], student_data["end_time"], 
                                                         f"{neutral_percent:.2f}%", f"{happy_percent:.2f}%", 
                                                         f"{sad_percent:.2f}%", f"{angry_percent:.2f}%", 
                                                         f"{fear_percent:.2f}%", f"{surprise_percent:.2f}%"))
                break

    def stop_recog(self):
        # Release the video capture if it's active
        if self.video_cap is not None:
            self.video_cap.release()
        
        # Clear the video label's image
        self.video_label.config(image="")

        # Deactivate both buttons
        self.face_recognition_button.config(state="disabled")
        self.stop_button.config(state="disabled")

if __name__ == "__main__":
    root = Tk()
    app = Emotion_Detection(root, username="Guest")
    root.mainloop()
