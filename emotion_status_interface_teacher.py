from tkinter import *
from tkinter import ttk
from tkinter import Frame
from PIL import Image, ImageTk
import calendar
import os
import teacher_interface
import mysql.connector  
from tkinter import messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


class Emotion_Status_Interface_Teacher:
    def __init__(self, root, username):
        self.root = root
        self.username = username  
        self.root.geometry("1024x590")  
        self.root.title("AttendNow - Emotion Status")

        
        self.var_teacher_course = StringVar()
        self.var_teacher = StringVar()
        

        
        background_img_main = Image.open(r"Image\Background.png")
        background_img_main = background_img_main.resize((1200, 600), Image.Resampling.LANCZOS)
        self.photo_background_img_main = ImageTk.PhotoImage(background_img_main)
        background_img_main_position = Label(self.root, image=self.photo_background_img_main)
        background_img_main_position.place(x=0, y=0, width=1200, height=600)

        
        left_title = Image.open(r"Image\LogoTitle_Left Top.png")
        self.photoleft_title = ImageTk.PhotoImage(left_title)
        left_title_position = Label(self.root, image=self.photoleft_title)
        left_title_position.place(x=0, y=0, width=163, height=60)

        
        title_frame = Frame(background_img_main_position, bd=2, bg="orange")
        title_frame.place(x=300, y=5, width=450, height=50)
        title_label = Label(title_frame, text="Emotion Status Management", bg="orange", fg="white", font=("New Time Roman", 20, "bold"))
        title_label.place(x=2, y=2, width=445, height=40)

        
        back_button = Button(self.root, text="Back", command=self.go_back, bg="red", fg="white", font=("Arial", 12, "bold"))
        back_button.place(x=175, y=15, width=80, height=30)

        
        self.username_label = Label(self.root, text=f"Logged in as: {self.username}", bg="orange", fg="white", font=("Arial", 12))
        self.username_label.place(x=800, y=15)

        
        self.main_frame = Frame(self.root, bd=2, bg="orange")
        self.main_frame.place(x=490, y=70, width=500, height=400)


        
        course_label = Label(background_img_main_position, text="Course:", bg="white")
        course_label.place(x=160, y=120, width=70, height=30)

        
        self.var_teacher_course = StringVar()  
        self.var_teacher_course.set("Select Teacher's Course")  

        self.course_combobox = ttk.Combobox(background_img_main_position, textvariable=self.var_teacher_course, state="readonly")
        self.course_combobox['values'] = []  
        self.course_combobox.place(x=250, y=120, width=200, height=30)


        

       
        search_button = Button(background_img_main_position, text="Search Student", command=self.search_student, bg="green", fg="white")
        search_button.place(x=160, y=160, width=290, height=40)

       
        columns = ('student_id', 'student_name')

        
        self.student_table = ttk.Treeview(background_img_main_position, columns=columns, show='headings', yscrollcommand=lambda f, l: self.scrollbar.set(f, l))

        
        self.student_table.heading('student_id', text='Student ID')
        self.student_table.heading('student_name', text='Student Name')

        
        self.student_table.column('student_id', width=145, anchor='center')
        self.student_table.column('student_name', width=145, anchor='center')

        
        self.student_table.place(x=160, y=210, width=290, height=150)

        
        self.scrollbar = Scrollbar(background_img_main_position, orient="vertical", command=self.student_table.yview)
        self.scrollbar.place(x=450, y=210, height=150)  

        
        self.student_table.bind("<<TreeviewSelect>>", self.on_student_select)

        
        selected_student_label = Label(background_img_main_position, text="Selected Student:", bg="white")
        selected_student_label.place(x=160, y=370, width=110, height=30)

        
        self.selected_student_input = Entry(background_img_main_position, state='readonly')
        self.selected_student_input.place(x=290, y=370, width=160, height=30)

        
        student_id_label = Label(background_img_main_position, text="Student ID:", bg="white")
        student_id_label.place(x=160, y=410, width=110, height=30)

        
        self.student_id_input = Entry(background_img_main_position, state='readonly')
        self.student_id_input.place(x=290, y=410, width=160, height=30)

       
        month_label = Label(background_img_main_position, text="Month:", bg="white")
        month_label.place(x=160, y=450, width=110, height=30)

        
        self.month_input = ttk.Combobox(background_img_main_position, values=[
            "January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"
        ], state='readonly')
        self.month_input.place(x=290, y=450, width=160, height=30)

        
        self.month_input.set("Select Month")

       
        year_label = Label(self.root, text="Year:", bg="white")
        year_label.place(x=160, y=490, width=110, height=30)

        
        self.year_input = ttk.Combobox(self.root, state='readonly')
        self.year_input.place(x=290, y=490, width=160, height=30)

        
        self.year_input.set("Select Year")

        
        self.fetch_years()

        
        self.get_emotion_status_button = Button(background_img_main_position, text="Get Emotion Status", command=self.get_emotion_status)
        self.get_emotion_status_button.place(x=160, y=530, width=290, height=30)


        
        self.clear_chart_button = Button(self.root, text="Clear Chart", command=self.clear_chart_function)
        self.clear_chart_button.place(x=490, y=480, width=100, height=30)

        
        self.type_labelframe = LabelFrame(self.root, text="Type", bg="orange", fg="white", bd=0, highlightthickness=0)
        self.type_labelframe.place(x=490, y=520, width=500, height=60)  

        
        self.emotion_status_detail_button = Button(self.type_labelframe, text="Emotion Status (Detail)", state="disabled",command=self.get_emotion_status)
        self.emotion_status_detail_button.place(x=10, y=5, width=150, height=30)

        self.emotion_status_overall_button = Button(self.type_labelframe, text="Emotion Status (Overall)", state="disabled", command=self.emotion_status_overall)
        self.emotion_status_overall_button.place(x=163, y=5, width=150, height=30)  

        self.emotion_status_table_button = Button(self.type_labelframe, text="Emotion Status (Table Value)", state="disabled", command=self.emotion_status_table)
        self.emotion_status_table_button.place(x=316, y=5, width=170, height=30)  



       
        self.fetch_courses(self.username)
        
        
        
        
       
        



    def emotion_status_table(self): 
        
        for widget in self.main_frame.winfo_children():
            widget.destroy()

        student_name = self.selected_student_input.get()
        student_id = self.student_id_input.get()
        month_value = self.display_selected_month()
        month_name = calendar.month_name[int(month_value)]
        selected_year = self.year_input.get()  

        if not student_name or not student_id:
            messagebox.showwarning("Warning", "Please select a student.")
            return

        if selected_year == "Select Year":  
            messagebox.showwarning("Warning", "Please select a year.")
            return

        
        connection = mysql.connector.connect(
            host="localhost",  
            user="root",
            password="Nightcore_1134372019!",
            database="attendnow"
        )

        cursor = connection.cursor()

        
        query = 

        cursor.execute(query, (student_name, student_id, month_value, selected_year))
        results = cursor.fetchall()

        
        connection.close()

        if not results:
            messagebox.showinfo("Info", f"No emotion data found for the selected student in {month_name}, {selected_year}.")
            return

        
        self.tree_frame = ttk.Frame(self.main_frame)
        self.tree_frame.pack(fill="both", expand=True)

        
        columns = ["Date", "Neutral", "Happy", "Sad", "Fear", "Surprise", "Angry", "Overall Emotion"]
        
        
        self.attendance_table = ttk.Treeview(self.tree_frame, columns=columns, show='headings')

        
        column_widths = [80, 50, 50, 50, 50, 50, 50, 120]  

        for column, width in zip(columns, column_widths):
            self.attendance_table.heading(column, text=column)
            
            self.attendance_table.column(column, anchor='center', width=width, stretch=False)

        
        scroll_y = ttk.Scrollbar(self.tree_frame, orient='vertical', command=self.attendance_table.yview)

        
        self.attendance_table.configure(yscrollcommand=scroll_y.set)

        
        for row in results:
            date_str = str(row[0])  
            overall_emotion = max(('Neutral', row[1]), ('Happy', row[2]), ('Sad', row[3]), 
                                ('Fear', row[4]), ('Surprise', row[5]), ('Angry', row[6]), 
                                key=lambda x: x[1])[0]  

            
            self.attendance_table.insert('', 'end', values=(date_str, row[1], row[2], row[3], row[4], row[5], row[6], overall_emotion))

        
        self.attendance_table.pack(side="left", fill="both", expand=True)
        scroll_y.pack(side="right", fill="y")

        
        self.emotion_status_detail_button.config(state="normal")
        self.emotion_status_overall_button.config(state="normal")
        self.emotion_status_table_button.config(state="normal")
        self.get_emotion_status_button.config(state="disabled")

    
    def emotion_status_overall(self):
        
        for widget in self.main_frame.winfo_children():
            widget.destroy()

        student_name = self.selected_student_input.get()
        student_id = self.student_id_input.get()
        month_value = self.display_selected_month()
        month_name = calendar.month_name[int(month_value)]
        selected_year = self.year_input.get()  

        if not student_name or not student_id:
            messagebox.showwarning("Warning", "Please select a student.")
            return

        if selected_year == "Select Year":  
            messagebox.showwarning("Warning", "Please select a year.")
            return

        
        connection = mysql.connector.connect(
            host="localhost",  
            user="root",
            password="Nightcore_1134372019!",
            database="attendnow"
        )
        
        cursor = connection.cursor()

        
        query = 
        
        cursor.execute(query, (student_name, student_id, month_value, selected_year))
        results = cursor.fetchall()
        
        
        connection.close()

        if not results:
            messagebox.showinfo("Info", f"No emotion data found for the selected student in {month_name}, {selected_year}.")
            return

        
        days = []  
        max_emotion_values = []
        max_emotion_labels = []

        
        emotion_colors = {
            'Neutral': 'green',
            'Happy': 'yellow',
            'Sad': 'blue',
            'Fear': 'purple',
            'Surprise': 'orange',
            'Angry': 'red'
        }

        for row in results:
            
            date_str = str(row[0])  
            day = date_str.split('-')[2]  
            
            days.append(day)  
            
            
            emotion_values = [row[1], row[2], row[3], row[4], row[5], row[6]]
            max_value = max(emotion_values)
            max_index = emotion_values.index(max_value)

            max_emotion_values.append(max_value)
            
            
            emotions = ['Neutral', 'Happy', 'Sad', 'Fear', 'Surprise', 'Angry']
            max_emotion_labels.append(emotions[max_index])

        
        figure, ax = plt.subplots(figsize=(5, 4))  

        
        colors = [emotion_colors[label] for label in max_emotion_labels]

        bars = ax.bar(days, max_emotion_values, color=colors)  

        
        ax.set_xlabel('Day (DD)')
        ax.set_ylabel('Emotion Value')
        ax.set_title(f'Max Emotion Status for {student_name} ({month_name}, {selected_year})')

        
        ax.set_xticks(range(len(days)))
        ax.set_xticklabels(days, rotation=90)  

        
        handles = [plt.Rectangle((0, 0), 1, 1, color=color) for color in emotion_colors.values()]
        ax.legend(handles, emotion_colors.keys(), title="Emotions")

        
        canvas = FigureCanvasTkAgg(figure, master=self.main_frame)
        canvas.draw()

        
        canvas.get_tk_widget().config(width=500, height=300)  

        
        canvas.get_tk_widget().pack(fill="both", expand=True)

        
        self.emotion_status_detail_button.config(state="normal")
        self.emotion_status_overall_button.config(state="normal")
        self.emotion_status_table_button.config(state="normal")
        self.get_emotion_status_button.config(state="disabled")


    
    def fetch_years(self):
        try:
            
            conn = mysql.connector.connect(
                host="localhost",
                user="root",
                password="Nightcore_1134372019!",  
                database="attendnow"
            )
            cursor = conn.cursor()

            
            query = "SELECT DISTINCT YEAR(date) FROM student_emotion ORDER BY YEAR(date) ASC"
            cursor.execute(query)

            
            years = [str(row[0]) for row in cursor.fetchall()]

            
            cursor.close()
            conn.close()

            
            self.year_input['values'] = years

        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Error: {err}")
    
    
    def clear_chart_function(self):
        
        for widget in self.main_frame.winfo_children():
            widget.destroy()
        
        self.emotion_status_detail_button.config(state="disabled")
        self.emotion_status_overall_button.config(state="disabled")
        self.emotion_status_table_button.config(state="disabled")
        self.get_emotion_status_button.config(state="normal")


        
    
    def display_selected_month(self):
        month_mapping = {
            "January": "01",
            "February": "02",
            "March": "03",
            "April": "04",
            "May": "05",
            "June": "06",
            "July": "07",
            "August": "08",
            "September": "09",
            "October": "10",
            "November": "11",
            "December": "12"
        }
        
        selected_month = self.month_input.get()  
        
        if selected_month in month_mapping:  
            numerical_value = month_mapping[selected_month]
            
            return numerical_value
        else:
        
            return None

    
    
    def get_emotion_status(self):
        
        for widget in self.main_frame.winfo_children():
            widget.destroy()

        student_name = self.selected_student_input.get()
        student_id = self.student_id_input.get()
        month_value = self.display_selected_month()
        month_name = calendar.month_name[int(month_value)]
        selected_year = self.year_input.get()  

        if not student_name or not student_id:
            messagebox.showwarning("Warning", "Please select a student.")
            return

        if selected_year == "Select Year":  
            messagebox.showwarning("Warning", "Please select a year.")
            return

        
        connection = mysql.connector.connect(
            host="localhost",  
            user="root",
            password="Nightcore_1134372019!",
            database="attendnow"
        )
        
        cursor = connection.cursor()

        
        query = 
        
        cursor.execute(query, (student_name, student_id, month_value, selected_year))
        results = cursor.fetchall()
        
        
        connection.close()

        if not results:
            messagebox.showinfo("Info", f"No emotion data found for the selected student in {month_name}, {selected_year}.")
            return

        
        days = []  
        neutral = []
        happy = []
        sad = []
        fear = []
        surprise = []
        angry = []
        
        for row in results:
            
            date_str = str(row[0])  
            day = date_str.split('-')[2]  
            
            days.append(day)  
            neutral.append(row[1])
            happy.append(row[2])
            sad.append(row[3])
            fear.append(row[4])
            surprise.append(row[5])
            angry.append(row[6])

        
        figure, ax = plt.subplots(figsize=(6, 4))

        
        ax.bar(days, neutral, label='Neutral', color='green')
        ax.bar(days, happy, bottom=neutral, label='Happy', color='yellow')
        ax.bar(days, sad, bottom=[i + j for i, j in zip(neutral, happy)], label='Sad', color='blue')
        ax.bar(days, fear, bottom=[i + j + k for i, j, k in zip(neutral, happy, sad)], label='Fear', color='purple')
        ax.bar(days, surprise, bottom=[i + j + k + l for i, j, k, l in zip(neutral, happy, sad, fear)], label='Surprise', color='orange')
        ax.bar(days, angry, bottom=[i + j + k + l + m for i, j, k, l, m in zip(neutral, happy, sad, fear, surprise)], label='Angry', color='red')

        
        ax.set_xticks(range(len(days)))
        ax.set_xticklabels(days, rotation=90)

        
        ax.set_xlabel('Day (DD)')
        ax.set_ylabel('Emotion')
        ax.set_title(f'Emotion Status for {student_name} ({month_name}, {selected_year})')
        ax.legend()

        
        canvas = FigureCanvasTkAgg(figure, master=self.main_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)

        
        self.emotion_status_detail_button.config(state="normal")
        self.emotion_status_overall_button.config(state="normal")
        self.emotion_status_table_button.config(state="normal")
        self.get_emotion_status_button.config(state="disabled")

       

    def go_back(self):
        self.root.destroy() 
        new_window =Tk()
        teacher_interface.Teacher_Interface(new_window, self.username)
        


    
        
    def search_student(self):
        selected_course = self.var_teacher_course.get()  
        if not selected_course or selected_course == "Select Teacher's Course":
            messagebox.showerror("Error", "Please select a course.")
            return

        try:
            
            conn = mysql.connector.connect(
                host="localhost",
                user="root",
                password="Nightcore_1134372019!",
                database="attendnow"
            )
            cursor = conn.cursor()

            
            query = "SELECT student_id, student_name FROM students WHERE course = %s"
            cursor.execute(query, (selected_course,))  
            rows = cursor.fetchall()

            
            for row in self.student_table.get_children():
                self.student_table.delete(row)

            
            for row in rows:
                self.student_table.insert("", "end", values=row)

            conn.close()  

        except Exception as e:
            messagebox.showerror("Error", f"Error due to: {str(e)}")



    
    def on_student_select(self, event):  
        
        selected_item = self.student_table.selection()

        if selected_item:
            
            student_id, student_name = self.student_table.item(selected_item, 'values')

            
            self.selected_student_input.config(state='normal')  
            self.selected_student_input.delete(0, 'end')  
            self.selected_student_input.insert(0, student_name)  
            self.selected_student_input.config(state='readonly')  

            self.student_id_input.config(state='normal')  
            self.student_id_input.delete(0, 'end')  
            self.student_id_input.insert(0, student_id)  
            self.student_id_input.config(state='readonly')  


    

    def fetch_courses(self, teacher_name):
        try:
            
            conn = mysql.connector.connect(
                host="localhost",  
                user="root",  
                password="Nightcore_1134372019!",  
                database="attendnow"  
            )
            cursor = conn.cursor()

            
            query = "SELECT course FROM timetable WHERE teacher_name = %s"
            cursor.execute(query, (teacher_name,))  
            rows = cursor.fetchall()

            
            course_set = {row[0] for row in rows}
            course_list = list(course_set)  
            self.course_combobox['values'] = course_list  

            conn.close()  

        except Exception as e:
            messagebox.showerror("Error", f"Error due to: {str(e)}")


   



if __name__ == "__main__":
    root = Tk()
    app = Emotion_Status_Interface_Teacher(root, username="Jackie Chan")
    root.mainloop()
