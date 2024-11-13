from tkinter import *  
from tkinter import ttk  
from tkinter import messagebox
from tkcalendar import DateEntry  
from PIL import Image, ImageTk
import admit_interface
import mysql.connector

class Attendance_Status_Interface:
    def __init__(self, root, username):
        self.root = root
        self.root.geometry("1024x590+0+0")
        self.username = username
        self.root.title("AttendNow")

        
        background_img_main = Image.open(r"Image\Background.png")
        background_img_main = background_img_main.resize((1024, 590), Image.Resampling.LANCZOS)
        self.photo_background_img_main = ImageTk.PhotoImage(background_img_main)
        background_img_main_position = Label(self.root, image=self.photo_background_img_main)
        background_img_main_position.place(x=0, y=0, width=1024, height=590)

        
        left_title = Image.open(r"Image\LogoTitle_Left Top.png")
        self.photoleft_title = ImageTk.PhotoImage(left_title)
        left_title_position = Label(self.root, image=self.photoleft_title)
        left_title_position.place(x=0, y=0, width=163, height=60)

        
        back_button = Button(self.root, text="Back", command=self.go_back, bg="blue", fg="white", font=("Arial", 12, "bold"))
        back_button.place(x=175, y=15, width=80, height=30)

        
        main_frame = Frame(self.root, bd=2, bg="orange")
        main_frame.place(x=100, y=70, width=800, height=510)

        
        upper_frame = LabelFrame(main_frame, text="Search Attendance", bg="white", fg="black")
        upper_frame.place(x=5, y=5, width=785, height=260)

        
        search_teacher_frame = LabelFrame(upper_frame, text="Search By Teacher", bg="white", fg="black")
        search_teacher_frame.place(x=5, y=5, width=450, height=100)

       
        teacher_label = Label(search_teacher_frame, text="Teacher Name:", bg="white")
        teacher_label.grid(row=0, column=0, padx=3, pady=3, sticky=W)
        self.teacher_combobox = ttk.Combobox(search_teacher_frame, values=["John Doe", "Jane Smith"])
        self.teacher_combobox.grid(row=0, column=1, padx=3, pady=3, sticky=W)

        
        course_label = Label(search_teacher_frame, text="Course:", bg="white")
        course_label.grid(row=0, column=2, padx=3, pady=3, sticky=W)
        self.course_combobox = ttk.Combobox(search_teacher_frame)
        self.course_combobox['values'] = ("Select Course",)
        self.course_combobox.current(0)
        self.course_combobox.grid(row=0, column=3, padx=3, pady=3, sticky=W)

        
        date_label = Label(search_teacher_frame, text="Date:", bg="white")
        date_label.grid(row=1, column=2, padx=3, pady=3, sticky=W)
        self.date_entry = DateEntry(search_teacher_frame, width=20, background='darkblue', foreground='white', borderwidth=2)
        self.date_entry.grid(row=1, column=3, padx=3, pady=3, sticky=W)

        
        course_hour_label = Label(search_teacher_frame, text="Course Hour:", bg="white")
        course_hour_label.grid(row=1, column=0, padx=3, pady=3, sticky=W)
        self.course_hour_combobox = ttk.Combobox(search_teacher_frame, values=["8:00 AM - 9:00 AM", "9:00 AM - 10:00 AM", "10:00 AM - 11:00 AM"])
        self.course_hour_combobox['values'] = ("Select Course Hour",)
        self.course_hour_combobox.current(0)
        self.course_hour_combobox.grid(row=1, column=1, padx=3, pady=3, sticky=W)

        

        
        search_student_frame = LabelFrame(upper_frame, text="Search By Student", bg="white", fg="black")
        search_student_frame.place(x=5, y=110, width=450, height=120)

        
        search_label_id = Label(search_student_frame, text="Student ID:", bg="white")
        search_label_id.grid(row=0, column=0, padx=3, pady=2, sticky=W)

        self.search_entry_id = Entry(search_student_frame)
        self.search_entry_id.grid(row=0, column=1, padx=3, pady=2, sticky=W)

        option_label = Label(search_student_frame, text="/--OR--/", bg="white")
        option_label.grid(row=1, column=0, padx=10, pady=2, sticky=W)

        
        search_label_name = Label(search_student_frame, text="Student Name:", bg="white")
        search_label_name.grid(row=2, column=0, padx=3, pady=2, sticky=W)

        self.search_entry_name = Entry(search_student_frame)
        self.search_entry_name.grid(row=2, column=1, padx=3, pady=2, sticky=W)

       


        
        search_button_frame = LabelFrame(upper_frame, text="Search Button", bg="white", fg="black")
        search_button_frame.place(x=470, y=5, width=305, height=130)

        
        search_teacher_button = Button(search_button_frame, text="Search By Teacher", command=self.search_by_teacher, bg="orange", fg="white",width=20)
        search_teacher_button.grid(row=0, column=0, padx=10, pady=5, sticky=W)

        
        search_student_button = Button(search_button_frame, text="Search By Student", command=self.search_by_student, bg="orange", fg="white", width=20)
        search_student_button.grid(row=1, column=0, padx=10, pady=5, sticky=W)

        
        search_all_button = Button(search_button_frame, text="Search All", command=self.search_attendance, bg="orange", fg="white", width=20)
        search_all_button.grid(row=2, column=0, padx=10, pady=5, sticky=W)


        
        lower_frame = LabelFrame(main_frame, text="Attendance Records", bg="white", fg="black")
        lower_frame.place(x=5, y=270, width=785, height=200)

        
        self.tree_frame = Frame(lower_frame, bd=2, relief=RIDGE)
        self.tree_frame.pack(fill=BOTH, expand=True)  

        
        scroll_x = Scrollbar(self.tree_frame, orient=HORIZONTAL)
        scroll_y = Scrollbar(self.tree_frame, orient=VERTICAL)

        
        self.attendance_table = ttk.Treeview(self.tree_frame, 
                                            columns=("student_id", "student_name", "start_time", "recorder_timer", "end_time", "attendance_status", "date", "teacher", "course", "course_hour"),
                                            xscrollcommand=scroll_x.set, yscrollcommand=scroll_y.set)

        
        scroll_x.pack(side=BOTTOM, fill=X)
        scroll_y.pack(side=RIGHT, fill=Y)

        
        scroll_x.config(command=self.attendance_table.xview)
        scroll_y.config(command=self.attendance_table.yview)

        
        self.attendance_table.heading("student_id", text="Student ID")
        self.attendance_table.heading("student_name", text="Student Name")
        self.attendance_table.heading("start_time", text="Start Time")
        self.attendance_table.heading("recorder_timer", text="Recorder Timer")
        self.attendance_table.heading("end_time", text="End Time")
        self.attendance_table.heading("attendance_status", text="Attendance Status")
        self.attendance_table.heading("date", text="Date")
        self.attendance_table.heading("teacher", text="Teacher")
        self.attendance_table.heading("course", text="Course")
        self.attendance_table.heading("course_hour", text="Course Hour")

        self.attendance_table["show"] = "headings"  

        
        self.attendance_table.column("student_id", width=100, minwidth=100, stretch=False)
        self.attendance_table.column("student_name", width=150, minwidth=150, stretch=False)
        self.attendance_table.column("start_time", width=100, minwidth=100, stretch=False)
        self.attendance_table.column("recorder_timer", width=120, minwidth=120, stretch=False)
        self.attendance_table.column("end_time", width=100, minwidth=100, stretch=False)
        self.attendance_table.column("attendance_status", width=150, minwidth=150, stretch=False)
        self.attendance_table.column("date", width=100, minwidth=100, stretch=False)
        self.attendance_table.column("teacher", width=150, minwidth=150, stretch=False)
        self.attendance_table.column("course", width=150, minwidth=150, stretch=False)
        self.attendance_table.column("course_hour", width=100, minwidth=100, stretch=False)

        
        self.attendance_table.pack(fill=BOTH, expand=1)

        
        self.attendance_table.configure(yscrollcommand=scroll_y.set, xscrollcommand=scroll_x.set)



        self.search_attendance()
        self.populate_teacher_combobox()
        self.teacher_combobox.bind("<<ComboboxSelected>>", self.populate_course_combobox) 
        self.course_combobox.bind("<<ComboboxSelected>>", self.populate_timing_dropdown)


        






    def populate_timing_dropdown(self, event):
        selected_course = self.course_combobox.get()

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
                self.course_hour_combobox['values'] = ["Select Timing"] + timings
            else:
                messagebox.showinfo("No Timings Found", "No timings available for the selected course.")
                self.course_hour_combobox['values'] = ("Select Timing",)

            
            self.course_hour_combobox.current(0)

        except mysql.connector.Error as error:
            messagebox.showerror("Database Error", f"Error: {error}")
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()


    
    def populate_course_combobox(self, event):
        
        selected_teacher = self.teacher_combobox.get()
        
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
        self.course_combobox['values'] = course_list
        
        
        self.course_combobox.current(0)
        
        
        connection.close()

    
    def populate_teacher_combobox(self):
        try:
            
            connection = mysql.connector.connect(
                host='localhost',        
                user='root',             
                password='Nightcore_1134372019!',  
                database='attendnow'     
            )
            
            cursor = connection.cursor()

            
            query = "SELECT DISTINCT teacher_name FROM timetable"
            cursor.execute(query)

            
            teachers = cursor.fetchall()

            
            teacher_list = [teacher[0] for teacher in teachers]

            
            self.teacher_combobox['values'] = teacher_list

            
            self.teacher_combobox.set("Select Teacher")

        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Error: {err}")
        finally:
            
            if connection.is_connected():
                cursor.close()
                connection.close()

    
    
    def search_by_student(self):
        
        for item in self.attendance_table.get_children():
            self.attendance_table.delete(item)

        student_id = self.search_entry_id.get().strip()
        student_name = self.search_entry_name.get().strip()

        
        if not student_id and not student_name:
            messagebox.showwarning("Input Required", "Please enter either a Student ID or Student Name to search.")
            return  
        
        
        if student_id and student_name:
            messagebox.showwarning("Input Error", "Please fill only one field, either Student ID or Student Name, not both.")
            return  

        try:
            
            connection = mysql.connector.connect(
                host='localhost',        
                user='root',             
                password='Nightcore_1134372019!',  
                database='attendnow'     
            )
            
            cursor = connection.cursor()

            
            query = 
            cursor.execute(query, (student_id, student_name))

            
            records = cursor.fetchall()

            
            for record in records:
                self.attendance_table.insert('', 'end', values=record)

            if not records:
                messagebox.showinfo("No Records", "No attendance records found for the given Student ID or Name.")

        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Error: {err}")
        finally:
            
            if connection.is_connected():
                cursor.close()
                connection.close()

    
    
    def search_by_teacher(self):
        teacher_name = self.teacher_combobox.get()
        course = self.course_combobox.get()
        date = self.date_entry.get()

        if not teacher_name or not course or not date:
            messagebox.showwarning("Input Error", "Please fill all fields to search.")
            return
        
        print(f"Searching for teacher: {teacher_name}, course: {course}, date: {date}")

        
        for row in self.tree.get_children():
            self.tree.delete(row)

        
        data = [
            ("S001", "John Doe", "09:00 AM", "1h", "10:00 AM", "Present"),
            ("S002", "Jane Smith", "09:10 AM", "50m", "10:00 AM", "Present")
        ]

        
        for record in data:
            self.tree.insert("", END, values=record)

    
    def search_attendance(self):
        
        for item in self.attendance_table.get_children():
            self.attendance_table.delete(item)

        try:
            
            connection = mysql.connector.connect(
                host='localhost',        
                user='root',             
                password='Nightcore_1134372019!',  
                database='attendnow'     
            )
            
            cursor = connection.cursor()

            
            query = "SELECT  student_id, student_name, start_time, recorder_timer, end_time, attendance_status, date ,teacher, course,course_hour FROM attendance_status"
            cursor.execute(query)

            
            records = cursor.fetchall()

            
            for record in records:
                self.attendance_table.insert('', 'end', values=record)

        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Error: {err}")
        finally:
            
            if connection.is_connected():
                cursor.close()
                connection.close()

    
    def go_back(self):
        self.root.destroy()
        new_window = Tk()
        admit_interface.Admit_Interface(new_window, self.username)


if __name__ == "__main__":
    root = Tk()
    root.resizable(False, False)
    obj = Attendance_Status_Interface(root, "Guest")
    root.mainloop()
