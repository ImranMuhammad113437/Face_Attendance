from tkinter import *
from tkinter import ttk  
from PIL import Image, ImageTk
import mysql.connector
from datetime import datetime
from tkinter import messagebox
import cv2
from datetime import datetime, timedelta
import csv
import json
import admit_interface 

with open(r".vscode\settings.json") as file:
    settings = json.load(file)
connection_details = settings["sqltools.connections"][0]

class Face_Recognition:
    def __init__(self, root, username):
        self.root = root
        self.username = username 
        self.root.geometry("1024x590")
        self.root.title("AttendNow")

        

        
        background_img_face_recognition = Image.open(r"Image\Background.png")
        background_img_face_recognition = background_img_face_recognition.resize((1024, 590), Image.Resampling.LANCZOS)
        self.photo_background_img_face_recognition = ImageTk.PhotoImage(background_img_face_recognition)
        background_img_face_recognition_position = Label(self.root, image=self.photo_background_img_face_recognition)
        background_img_face_recognition_position.place(x=0, y=0, width=1024, height=590)

        
        left_title = Image.open(r"Image\LogoTitle_Left Top.png")
        self.photoleft_title = ImageTk.PhotoImage(left_title)
        left_title_position = Label(self.root, image=self.photoleft_title)
        left_title_position.place(x=0, y=0, width=163, height=60)

        main_frame = Frame(background_img_face_recognition_position, bd=2, bg="orange")
        main_frame.place(x=300, y=5, width=400, height=50)

        
        Label(main_frame, text="Face Recognition", bg="orange", fg="white", font=("New Time Roman", 20, "bold")).place(relx=0.5, rely=0.5, anchor=CENTER)

        
        self.teacher_input = ttk.Combobox(background_img_face_recognition_position, width=28, state="readonly")
        self.teacher_input.place(x=80, y=100, width=310)  

        
        self.teacher_course_input = ttk.Combobox(background_img_face_recognition_position, width=28, state="readonly")
        self.teacher_course_input['values'] = ("Select Course",)
        self.teacher_course_input.current(0)
        self.teacher_course_input.place(x=80, y=130, width=310)  

        
        self.timing_input = ttk.Combobox(background_img_face_recognition_position, width=28, state="readonly")
        self.timing_input['values'] = ("Select Timing",)
        self.timing_input.current(0)
        self.timing_input.place(x=80, y=160, width=310)  


        
        face_recognition_button = Button(background_img_face_recognition_position, command=self.face_recog, text="Start Class")
        face_recognition_button.place(x=80, y=190, width=150, height=40)  

        
        stop_button = Button(background_img_face_recognition_position, command=self.stop_recog, text="Stop Class", bg="red", fg="white")
        stop_button.place(x=240, y=190, width=150, height=40)  

        
        self.video_label = Label(background_img_face_recognition_position)
        self.video_label.place(x=400, y=100, width=600, height=400)  

        
        tree_frame = Frame(self.root)
        tree_frame.place(x=80, y=250, width=310, height=250)

    


         
        self.tree = ttk.Treeview(tree_frame, columns=("ID", "Name", "Start Time", "Recording Timer", "End Time", "Attendance"), show='headings', height=8)
        self.tree.heading("ID", text="Student ID")
        self.tree.heading("Name", text="Student Name")
        self.tree.heading("Start Time", text="Start Time")
        self.tree.heading("Recording Timer", text="Recording Timer")  
        self.tree.heading("End Time", text="End Time")
        self.tree.heading("Attendance", text="Attendance")  
        self.tree.column("ID", anchor=CENTER, width=100)
        self.tree.column("Name", anchor=CENTER, width=200)
        self.tree.column("Start Time", anchor=CENTER, width=100)
        self.tree.column("Recording Timer", anchor=CENTER, width=100)  
        self.tree.column("End Time", anchor=CENTER, width=100)
        self.tree.column("Attendance", anchor=CENTER, width=100)  

        
        scrollbar = ttk.Scrollbar(tree_frame, orient="horizontal", command=self.tree.xview)
        self.tree.configure(xscrollcommand=scrollbar.set)

        self.tree.pack(side=TOP, fill=BOTH, expand=True)  
        scrollbar.pack(side=BOTTOM, fill=X)  

        self.attendance_records = {}  
        self.student_present = set()  
        self.student_start_times = {}  
        self.video_cap = None  
        
        self.username_label = Label(self.root, text=f"Logged in as: {self.username}", bg="orange", fg="white", font=("Arial", 12))
        self.username_label.place(x=820, y=15)
        
        return_button = Button(self.root, text="Back", command=self.return_to_admit_interface, bg="blue", fg="white", font=("Arial", 12, "bold"))
        return_button.place(x=170, y=15, width=80, height=30)

        self.populate_teacher_dropdown()
        self.teacher_input.bind("<<ComboboxSelected>>", self.populate_course_dropdown)
        self.teacher_course_input.bind("<<ComboboxSelected>>", self.populate_timing_dropdown)


    
    
    def populate_timing_dropdown(self, event):
        selected_course = self.teacher_course_input.get()

        if selected_course == "Select Course":
            messagebox.showwarning("Selection Error", "Please select a valid course.")
            return

        try:
            
            connection = mysql.connector.connect(
                host="localhost",
                user="root",
                password="Nightcore_1134372019!",  
                database="attendnow"
            )

            cursor = connection.cursor()

            
            query = "SELECT timing FROM timetable WHERE course = %s"
            cursor.execute(query, (selected_course,))

            
            timings = [timing[0] for timing in cursor.fetchall()]

            
            if timings:
                self.timing_input['values'] = ["Select Timing"] + timings
            else:
                messagebox.showinfo("No Timings Found", "No timings available for the selected course.")
                self.timing_input['values'] = ("Select Timing",)

            
            self.timing_input.current(0)

        except mysql.connector.Error as error:
            messagebox.showerror("Database Error", f"Error: {error}")
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()

    
    def populate_course_dropdown(self, event):
        
        selected_teacher = self.teacher_input.get()
        
        if selected_teacher == "Select Teacher":
            return
        
        
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

        
        course_list = ["Select Course"] + [course[0] for course in courses]
        self.teacher_course_input['values'] = course_list
        
        
        self.teacher_course_input.current(0)
        
        
        connection.close()

    
    def populate_teacher_dropdown(self):
        
        connection = mysql.connector.connect(
            host="localhost",  
            user="root",
            password="Nightcore_1134372019!",
            database="attendnow"
        )
        
        cursor = connection.cursor()

        
        query = "SELECT DISTINCT teacher_name FROM timetable"
        cursor.execute(query)
        results = cursor.fetchall()

        
        connection.close()

        
        teacher_names = [row[0] for row in results]

        
        self.teacher_input['values'] = teacher_names

        self.teacher_input.set("Select Teacher:")


    def return_to_admit_interface(self):
        self.root.destroy()  
        new_window = Tk()  
        admit_interface.Admit_Interface(new_window, self.username)
    
    def mark_attendance(self, id, student_name):
        now = datetime.now()
        dtString = now.strftime("%H:%M:%S")  

        
        if id not in self.attendance_records:
            self.attendance_records[id] = {"student_name": student_name, "start_time": dtString, "end_time": ""}

        try:
            
            connection = mysql.connector.connect(
                host="localhost",
                user="root",
                password="Nightcore_1134372019!",
                database="attendnow"
            )
            cursor = connection.cursor()

            
            if id not in self.student_present:
                self.student_present.add(id)
                self.attendance_records[id]["start_time"] = dtString  

            connection.commit()

        except mysql.connector.Error as error:
            print(f"Database Error: {error}")
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()


       

    def face_recog(self):
        selected_course = self.teacher_course_input.get()
        selected_time = self.timing_input.get()  
        selected_teacher = self.teacher_input.get()

        
        if selected_course == "Select Course" or selected_time == "Select Timing" or selected_teacher == "Select Teacher":
            messagebox.showwarning("Selection Required", "Please select a valid course, timing, and teacher.")
            return

        try:
            
            connection = mysql.connector.connect(
                host="localhost",
                user="root",
                password="Nightcore_1134372019!",  
                database="attendnow"
            )
            cursor = connection.cursor()

            
            query = "SELECT student_name, student_id FROM students WHERE course = %s"
            cursor.execute(query, (selected_course,))

            
            students = cursor.fetchall()

            
            for row in self.tree.get_children():
                self.tree.delete(row)

            if students:
                
                for student_name, student_id in students:
                    self.tree.insert("", "end", values=(student_id, student_name, "", ""))  

            
            connection.commit()

        except mysql.connector.Error as error:
            messagebox.showerror("Database Error", f"Error: {error}")
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()

        
        faceCascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

        
        clf = cv2.face.LBPHFaceRecognizer_create()
        clf.read("classifier.xml")

        
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

            
            my_cursor.execute("SELECT student_name, student_id FROM students WHERE course=%s AND student_id=%s", (selected_course, id))
            result = my_cursor.fetchone()
            student_name = result[0] if result else "Unknown"
            student_id = result[1] if result else "Unknown"

            conn.close()

            
            if confidence > 70:
                cv2.putText(img, f"Name: {student_name}", (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)
                cv2.putText(img, f"ID: {student_id}", (x, y + h + 30), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)

                now = datetime.now().strftime("%H:%M:%S")  

                
                if id not in self.student_present:
                    self.student_present.add(id)
                    self.mark_attendance(id, student_name)  
                    self.student_start_times[id] = datetime.now()  

                    
                    for row in self.tree.get_children():
                        row_data = self.tree.item(row, "values")
                        if str(student_id) == row_data[0]:  
                            self.tree.item(row, values=(student_id, student_name, now, "", ""))  

                
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
                        values_to_update = (student_id, student_name, start_time_str, timer, now, attendance_status)
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

                        
                        current_date = datetime.now().strftime("%Y-%m-%d")  

                        
                        check_query = 

                        
                        my_cursor.execute(check_query, (student_id, selected_course, selected_time, current_date))
                        record = my_cursor.fetchone()  

                        if record:
                            
                            update_query = 

                            
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
                            
                            insert_query = 

                            
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


            else:
                pass

        
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        img_pil = Image.fromarray(img_rgb)
        imgtk = ImageTk.PhotoImage(image=img_pil)

        
        self.video_label.imgtk = imgtk
        self.video_label.configure(image=imgtk)

        
        self.video_label.after(10, lambda: self.recognize(faceCascade, clf, selected_course))


    def stop_recog(self):
        
        if self.video_cap:
            self.video_cap.release()
        self.video_label.config(image="")


if __name__ == "__main__":
    root = Tk()
    obj = Face_Recognition(root, "Face")
    root.mainloop()
    root.resizable(False, False)
