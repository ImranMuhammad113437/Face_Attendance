from tkinter import *
from tkinter import ttk  # For Treeview
from PIL import Image, ImageTk
import mysql.connector
from datetime import datetime
from tkinter import messagebox
import cv2
from datetime import datetime, timedelta
import csv
import json
from collections import defaultdict
import teacher_interface 
from fer import FER

with open(r".vscode\settings.json") as file:
    settings = json.load(file)
connection_details = settings["sqltools.connections"][0]

class Start_Class_Interface_Teacher:
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
        Label(main_frame, text="Start Class", bg="orange", fg="white", font=("New Time Roman", 20, "bold")).place(relx=0.5, rely=0.5, anchor=CENTER)

        # Assuming this code is inside a class and you call the method to populate the dropdown
        self.teacher_input = ttk.Combobox(background_img_face_recognition_position, width=28, state="readonly")
        self.teacher_input.place(x=80, y=100, width=310)  

        # Course dropdown (new dropdown to select the teacher's course)
        self.teacher_course_input = ttk.Combobox(background_img_face_recognition_position, width=28, state="readonly")
        self.teacher_course_input['values'] = ("Select Course",)
        self.teacher_course_input.current(0)
        self.teacher_course_input.place(x=80, y=130, width=310)  # Position below teacher dropdown and above buttons

        # Timing dropdown (new dropdown to select the timing)
        self.timing_input = ttk.Combobox(background_img_face_recognition_position, width=28, state="readonly")
        self.timing_input['values'] = ("Select Timing",)
        self.timing_input.current(0)
        self.timing_input.place(x=80, y=160, width=310)  


        # Start Face Recognition Button
        face_recognition_button = Button(background_img_face_recognition_position, command=self.face_recog, text="Start Class")
        face_recognition_button.place(x=80, y=190, width=150, height=40)  # Position below the dropdown

        # Stop Face Recognition Button (next to the Start button)
        stop_button = Button(background_img_face_recognition_position, command=self.stop_recog, text="Stop Class", bg="red", fg="white")
        stop_button.place(x=240, y=190, width=150, height=40)  # Next to the Start button

        # Video display area on the right of the buttons
        self.video_label = Label(background_img_face_recognition_position)
        self.video_label.place(x=400, y=100, width=600, height=400)  # Position for video display
    
        # Create a frame for the Treeview and scrollbar
        tree_frame = Frame(self.root)
        tree_frame.place(x=80, y=250, width=310, height=250)

    


        columns = ("ID", "Name", "Start Time", "Recording Timer", "End Time", "Attendance", "Neutral", "Happy", "Sad", "Fear", "Surprise", "Angry")
        self.tree = ttk.Treeview(tree_frame, columns=columns, show='headings', height=8)

        self.tree.heading("ID", text="Student ID")
        self.tree.heading("Name", text="Student Name")
        self.tree.heading("Start Time", text="Start Time")
        self.tree.heading("Recording Timer", text="Recording Timer")
        self.tree.heading("End Time", text="End Time")
        self.tree.heading("Attendance", text="Attendance")
        self.tree.heading("Neutral", text="Neutral (%)")
        self.tree.heading("Happy", text="Happy (%)")
        self.tree.heading("Sad", text="Sad (%)")
        self.tree.heading("Fear", text="Fear (%)")
        self.tree.heading("Surprise", text="Surprise (%)")
        self.tree.heading("Angry", text="Angry (%)")

        self.tree.column("ID", anchor=CENTER, width=100)
        self.tree.column("Name", anchor=CENTER, width=200)
        self.tree.column("Start Time", anchor=CENTER, width=100)
        self.tree.column("Recording Timer", anchor=CENTER, width=100)
        self.tree.column("End Time", anchor=CENTER, width=100)
        self.tree.column("Attendance", anchor=CENTER, width=100)
        self.tree.column("Neutral", anchor=CENTER, width=100)
        self.tree.column("Happy", anchor=CENTER, width=100)
        self.tree.column("Sad", anchor=CENTER, width=100)
        self.tree.column("Fear", anchor=CENTER, width=100)
        self.tree.column("Surprise", anchor=CENTER, width=100)
        self.tree.column("Angry", anchor=CENTER, width=100)

        # Create a horizontal scrollbar
        scrollbar = ttk.Scrollbar(tree_frame, orient="horizontal", command=self.tree.xview)
        self.tree.configure(xscrollcommand=scrollbar.set)

        self.tree.pack(side=TOP, fill=BOTH, expand=True)  # Adjusted packing
        scrollbar.pack(side=BOTTOM, fill=X)  # Pack scrollbar at the bottom

        self.emotion_detector = FER()
        self.total_frames = defaultdict(int)
        self.attendance_records = {}  # To track start times
        self.student_present = set()  # Track recognized students
        self.student_start_times = {}  # To store start time for each student
        self.cumulative_emotions = {}
        self.video_cap = None  # Video capture object
        
        self.username_label = Label(self.root, text=f"Logged in as: {self.username}", bg="orange", fg="white", font=("Arial", 12))
        self.username_label.place(x=820, y=15)
        
        return_button = Button(self.root, text="Back", command=self.return_to_admit_interface, bg="blue", fg="white", font=("Arial", 12, "bold"))
        return_button.place(x=170, y=15, width=80, height=30)

        self.populate_teacher_dropdown()
        self.teacher_input.bind("<<ComboboxSelected>>", self.populate_course_dropdown)
        self.teacher_course_input.bind("<<ComboboxSelected>>", self.populate_timing_dropdown)

#--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    
    
    def populate_timing_dropdown(self, event):
        selected_course = self.teacher_course_input.get()

        if selected_course == "Select Course":
            messagebox.showwarning("Selection Error", "Please select a valid course.")
            return

        try:
            # Connect to the MySQL database 'attendnow'
            connection = mysql.connector.connect(
                host="localhost",
                user="root",
                password="Nightcore_1134372019!",  # Replace with your actual password
                database="attendnow"
            )

            cursor = connection.cursor()

            # SQL query to get the timing based on the selected course
            query = "SELECT timing FROM timetable WHERE course = %s"
            cursor.execute(query, (selected_course,))

            # Fetch all the timings for the selected course
            timings = [timing[0] for timing in cursor.fetchall()]

            # Always show "Select Timing" as the default option
            if timings:
                self.timing_input['values'] = ["Select Timing"] + timings
            else:
                messagebox.showinfo("No Timings Found", "No timings available for the selected course.")
                self.timing_input['values'] = ("Select Timing",)

            # Set the default selection to "Select Timing"
            self.timing_input.current(0)

        except mysql.connector.Error as error:
            messagebox.showerror("Database Error", f"Error: {error}")
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()

    
    def populate_course_dropdown(self, event):
        # Get the selected teacher name
        selected_teacher = self.teacher_input.get()
        
        if selected_teacher == "Select Teacher":
            return
        
        # Connect to the MySQL database
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="Nightcore_1134372019!",
            database="attendnow"
        )
        
        cursor = connection.cursor()
        query = "SELECT DISTINCT course FROM timetable WHERE teacher_name = %s"
        cursor.execute(query, (selected_teacher,))
        courses = cursor.fetchall()

        # Set the courses in the dropdown, including the default "Select Course"
        course_list = ["Select Course"] + [course[0] for course in courses]
        self.teacher_course_input['values'] = course_list
        
        # Automatically select the default option ("Select Course")
        self.teacher_course_input.current(0)
        
        # Close the database connection
        connection.close()

    
    def populate_teacher_dropdown(self):
        # Connect to the MySQL database
        connection = mysql.connector.connect(
            host="localhost",  # Replace with your host if different
            user="root",
            password="Nightcore_1134372019!",
            database="attendnow"
        )
        
        cursor = connection.cursor()

        # SQL query to fetch distinct teacher names
        query = "SELECT DISTINCT teacher_name FROM timetable"
        cursor.execute(query)
        results = cursor.fetchall()

        # Close the database connection
        connection.close()

        # Extract the teacher names from the results
        teacher_names = [row[0] for row in results]

        # Populate the dropdown (Combobox) with unique teacher names
        self.teacher_input['values'] = teacher_names

        self.teacher_input.set("Select Teacher:")


    def return_to_admit_interface(self):
        self.root.destroy()  # Close the student interface
        new_window = Tk()  # Create a new Tk window for the admit interface
        teacher_interface.Teacher_Interface(new_window, self.username)
    
    def mark_attendance(self, id, student_name):
        now = datetime.now()
        dtString = now.strftime("%H:%M:%S")  # Start time for when the student first arrives

        # Store start time for student if not already present
        if id not in self.attendance_records:
            self.attendance_records[id] = {"student_name": student_name, "start_time": dtString, "end_time": ""}

        try:
            # Connect to the MySQL database 'attendnow'
            connection = mysql.connector.connect(
                host="localhost",
                user="root",
                password="Nightcore_1134372019!",
                database="attendnow"
            )
            cursor = connection.cursor()

            # Insert attendance record without duplicating start time
            if id not in self.student_present:
                self.student_present.add(id)
                self.attendance_records[id]["start_time"] = dtString  # Add the start time when student first seen

            connection.commit()

        except mysql.connector.Error as error:
            print(f"Database Error: {error}")
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()


       

    def face_recog(self):
        selected_course = self.teacher_course_input.get()
        selected_time = self.timing_input.get()  # Get the selected timing
        selected_teacher = self.teacher_input.get()

        # Validate that all required fields are selected
        if selected_course == "Select Course" or selected_time == "Select Timing" or selected_teacher == "Select Teacher":
            messagebox.showwarning("Selection Required", "Please select a valid course, timing, and teacher.")
            return

        try:
            # Connect to the MySQL database 'attendnow'
            connection = mysql.connector.connect(
                host="localhost",
                user="root",
                password="Nightcore_1134372019!",  # Replace with your actual password
                database="attendnow"
            )
            cursor = connection.cursor()

            # SQL query to retrieve student names and IDs where course matches the selected course
            query = "SELECT student_name, student_id FROM students WHERE course = %s"
            cursor.execute(query, (selected_course,))

            # Fetch all the students for the selected course
            students = cursor.fetchall()

            # Clear the Treeview before inserting new data
            for row in self.tree.get_children():
                self.tree.delete(row)

            if students:
                # Populate Treeview with student name and ID
                for student_name, student_id in students:
                    self.tree.insert("", "end", values=(student_id, student_name, "", ""))  # Empty columns for Start Time and End Time

            # Commit the transaction
            connection.commit()

        except mysql.connector.Error as error:
            messagebox.showerror("Database Error", f"Error: {error}")
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()

        # Load the face detection classifier
        faceCascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

        # Load the face recognition model
        clf = cv2.face.LBPHFaceRecognizer_create()
        clf.read("classifier.xml")

        # Start video capture for face recognition
        self.video_cap = cv2.VideoCapture(0)
        self.recognize(faceCascade, clf, selected_course)

    
    def recognize(self, faceCascade, clf, selected_course):
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

            my_cursor.execute("SELECT student_name, student_id FROM students WHERE course=%s AND student_id=%s", (selected_course, id))
            result = my_cursor.fetchone()
            student_name = result[0] if result else "Unknown"
            student_id = result[1] if result else "Unknown"

            conn.close()

            if confidence > 77:
                face_img = img[y:y + h, x:x + w]
                detected_emotions = self.detect_emotion(face_img)  # Get detected emotion values

                # Get the live emotion with the highest value
                live_emotion = max(detected_emotions, key=detected_emotions.get)
                live_emotion_value = detected_emotions[live_emotion]

                # Initialize or update cumulative emotion values
                if student_id not in self.cumulative_emotions:
                    self.cumulative_emotions[student_id] = {
                        "neutral": 0, "happy": 0, "sad": 0, "fear": 0, "surprise": 0, "angry": 0, "disgust": 0
                    }

                cumulative_emotions = self.cumulative_emotions[student_id]

                for emotion, value in detected_emotions.items():
                    cumulative_emotions[emotion] += value

                # Track total frames for each student
                if student_id not in self.total_frames:
                    self.total_frames[student_id] = 0
                self.total_frames[student_id] += 1

                # Calculate the percentage for each emotion
                total_frames = self.total_frames[student_id]
                if total_frames > 0:
                    neutral_percent = (cumulative_emotions["neutral"] / total_frames) * 100
                    happy_percent = (cumulative_emotions["happy"] / total_frames) * 100
                    sad_percent = (cumulative_emotions["sad"] / total_frames) * 100
                    angry_percent = (cumulative_emotions["angry"] / total_frames) * 100
                    fear_percent = (cumulative_emotions["fear"] / total_frames) * 100
                    surprise_percent = (cumulative_emotions["surprise"] / total_frames) * 100
                else:
                    neutral_percent = happy_percent = sad_percent = angry_percent = fear_percent = surprise_percent = 0.0

                # Display the live emotion on the video frame
                cv2.putText(img, f"Name: {student_name}", (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)
                cv2.putText(img, f"ID: {student_id}", (x, y + h + 30), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)
                cv2.putText(img, f"Emotion: {live_emotion.capitalize()}", (x, y - 35), cv2.FONT_HERSHEY_COMPLEX, 0.8, (255, 255, 255), 2)

                now = datetime.now().strftime("%H:%M:%S")

                if id not in self.student_present:
                    self.student_present.add(id)
                    self.mark_attendance(id, student_name)
                    self.student_start_times[id] = datetime.now()

                    for row in self.tree.get_children():
                        row_data = self.tree.item(row, "values")
                        if str(student_id) == row_data[0]:
                            self.tree.item(row, values=(student_id, student_name, now, "", "", "", 
                                                        f"{neutral_percent:.2f}%", f"{happy_percent:.2f}%", f"{sad_percent:.2f}%", 
                                                        f"{angry_percent:.2f}%", f"{fear_percent:.2f}%", f"{surprise_percent:.2f}%"))

                start_time = self.student_start_times.get(id)
                elapsed_time = datetime.now() - start_time
                timer = str(elapsed_time).split(".")[0]

                for row in self.tree.get_children():
                    row_data = self.tree.item(row, "values")
                    if str(student_id) == row_data[0]:
                        start_time_str = row_data[2]
                        start_time = datetime.strptime(start_time_str, "%H:%M:%S")

                        current_time = datetime.now()
                        total_time = current_time - start_time
                        total_time_seconds = total_time.total_seconds()
                        timer_seconds = elapsed_time.total_seconds()

                        if timer_seconds > 8:
                            attendance_status = "Present"
                        elif 5 < timer_seconds <= 8:
                            attendance_status = "Half-Absent"
                        else:
                            attendance_status = "Absent"

                        now = current_time.strftime("%H:%M:%S")
                        values_to_update = (student_id, student_name, start_time_str, timer, now, attendance_status, 
                                            f"{neutral_percent:.2f}%", f"{happy_percent:.2f}%", f"{sad_percent:.2f}%", f"{angry_percent:.2f}%", 
                                            f"{fear_percent:.2f}%", f"{surprise_percent:.2f}%")
                        self.tree.item(row, values=values_to_update)

                        selected_course = self.teacher_course_input.get()
                        selected_time = self.timing_input.get()
                        selected_teacher = self.teacher_input.get()

                        current_date = datetime.now().strftime("%Y-%m-%d")

                        conn = mysql.connector.connect(
                            host="localhost",
                            user="root",
                            password="Nightcore_1134372019!",
                            database="attendnow"
                        )
                        my_cursor = conn.cursor()

                        check_query = """
                        SELECT * FROM attendance_status 
                        WHERE student_id = %s AND course = %s AND course_hour = %s AND date = %s;
                        """
                        my_cursor.execute(check_query, (student_id, selected_course, selected_time, current_date))
                        record = my_cursor.fetchone()

                        if record:
                            update_query = """
                            UPDATE attendance_status
                            SET attendance_status = %s,
                                start_time = %s,
                                recorder_timer = %s,
                                end_time = %s
                            WHERE student_id = %s AND course = %s AND course_hour = %s AND date = %s;
                            """
                            my_cursor.execute(update_query, (
                                attendance_status,
                                start_time_str,
                                timer,
                                now,
                                student_id,
                                selected_course,
                                selected_time,
                                current_date
                            ))
                        else:
                            insert_query = """
                            INSERT INTO attendance_status (student_name, student_id, attendance_status, start_time, recorder_timer, end_time, date, course, teacher, course_hour)
                            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
                            """
                            my_cursor.execute(insert_query, (
                                student_name,
                                student_id,
                                attendance_status,
                                start_time_str,
                                timer,
                                now,
                                current_date,
                                selected_course,
                                selected_teacher,
                                selected_time
                            ))

                        conn.commit()
                        conn.close()

                        # Update or insert emotion data into "student_emotion" table
                        conn = mysql.connector.connect(
                            host="localhost",
                            user="root",
                            password="Nightcore_1134372019!",
                            database="attendnow"
                        )
                        my_cursor = conn.cursor()

                        check_emotion_query = """
                        SELECT * FROM student_emotion
                        WHERE student_id = %s AND date = %s AND course = %s;
                        """
                        my_cursor.execute(check_emotion_query, (student_id, current_date, selected_course))
                        emotion_record = my_cursor.fetchone()

                        if emotion_record:
                            update_emotion_query = """
                            UPDATE student_emotion
                            SET neutral = %s, happy = %s, sad = %s, fear = %s, surprise = %s, angry = %s
                            WHERE student_id = %s AND date = %s AND course = %s;
                            """
                            my_cursor.execute(update_emotion_query, (
                                neutral_percent, happy_percent, sad_percent, fear_percent, 
                                surprise_percent, angry_percent,
                                student_id, current_date, selected_course
                            ))
                        else:
                            insert_emotion_query = """
                            INSERT INTO student_emotion (student_name, student_id, date, course, neutral, happy, sad, fear, surprise, angry)
                            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
                            """
                            my_cursor.execute(insert_emotion_query, (
                                student_name, student_id, current_date, selected_course,
                                neutral_percent, happy_percent, sad_percent, fear_percent, 
                                surprise_percent, angry_percent
                            ))

                        conn.commit()
                        conn.close()

            else:
                pass

        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        img_pil = Image.fromarray(img_rgb)
        imgtk = ImageTk.PhotoImage(image=img_pil)

        self.video_label.imgtk = imgtk
        self.video_label.configure(image=imgtk)
        self.video_label.after(10, lambda: self.recognize(faceCascade, clf, selected_course))

    def detect_emotion(self, face_img):
        emotions = self.emotion_detector.detect_emotions(face_img)
        if emotions:
            # Round each emotion value to 2 decimal places and cap at 99.99
            return {emotion: min(round(value, 2), 99.99) for emotion, value in emotions[0]["emotions"].items()}
        return {"neutral": 0, "happy": 0, "sad": 0, "fear": 0, "surprise": 0, "angry": 0}





    def stop_recog(self):
        # Step 1: Stop the video capture
        if self.video_cap:
            self.video_cap.release()
        self.video_label.config(image="")


if __name__ == "__main__":
    root = Tk()
    obj = Start_Class_Interface_Teacher(root, "Face")
    root.mainloop()
    root.resizable(False, False)
