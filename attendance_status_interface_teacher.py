from tkinter import *  # Import required tkinter widgets
from tkinter import ttk  # Import ttk for Treeview
from tkinter import messagebox
from tkcalendar import DateEntry  # Import DateEntry for calendar picker
from PIL import Image, ImageTk
import teacher_interface
import mysql.connector

class Attendance_Status_Interface_Teacher:
    def __init__(self, root, username):
        self.root = root
        self.root.geometry("1024x590+0+0")
        self.username = username
        self.root.title("AttendNow")

        # Background Image
        background_img_main = Image.open(r"Image\Background.png")
        background_img_main = background_img_main.resize((1024, 590), Image.Resampling.LANCZOS)
        self.photo_background_img_main = ImageTk.PhotoImage(background_img_main)
        background_img_main_position = Label(self.root, image=self.photo_background_img_main)
        background_img_main_position.place(x=0, y=0, width=1024, height=590)

        # LogoTitle Image
        left_title = Image.open(r"Image\LogoTitle_Left Top.png")
        self.photoleft_title = ImageTk.PhotoImage(left_title)
        left_title_position = Label(self.root, image=self.photoleft_title)
        left_title_position.place(x=0, y=0, width=163, height=60)

        # Display username on the top right corner
        self.username_label = Label(self.root, text=f"Logged in as: {username}", bg="orange", fg="white", font=("Arial", 12))
        self.username_label.place(x=800, y=15)

        # Logout Button (next to the logo)
        back_button = Button(self.root, text="Back", command=self.go_back, bg="blue", fg="white", font=("Arial", 12, "bold"))
        back_button.place(x=175, y=15, width=80, height=30)

        # Main Frame (Orange background) to hold the upper and lower sections
        main_frame = Frame(self.root, bd=2, bg="orange")
        main_frame.place(x=100, y=70, width=800, height=510)
#-----------------------------------------------------------------------------------------------------------
        # Upper Section - Search Section inside a LabelFrame
        upper_frame = LabelFrame(main_frame, text="Search Attendance", bg="white", fg="black")
        upper_frame.place(x=5, y=5, width=785, height=260)
#-----------------------------------------------------------------------------------------------------------

        # Frame for "Search By Student"
        search_student_frame = LabelFrame(upper_frame, text="Search By Student", bg="white", fg="black")
        search_student_frame.place(x=5, y=5, width=450, height=100)

        # Search label for Student ID
        search_label_id = Label(search_student_frame, text="Student ID:", bg="white")
        search_label_id.grid(row=0, column=0, padx=3, pady=2, sticky=W)

        self.search_entry_id = Entry(search_student_frame)
        self.search_entry_id.grid(row=0, column=1, padx=3, pady=2, sticky=W)

        option_label = Label(search_student_frame, text="/--OR--/", bg="white")
        option_label.grid(row=1, column=0, padx=10, pady=2, sticky=W)

        # Search label for Student Name
        search_label_name = Label(search_student_frame, text="Student Name:", bg="white")
        search_label_name.grid(row=2, column=0, padx=3, pady=2, sticky=W)

        self.search_entry_name = Entry(search_student_frame)
        self.search_entry_name.grid(row=2, column=1, padx=3, pady=2, sticky=W)

       

#-------------------------------------------------------------------------------------------------------------------------------
        # Frame for "Search Button"
        search_button_frame = LabelFrame(upper_frame, text="Search Button", bg="white", fg="black")
        search_button_frame.place(x=470, y=5, width=305, height=130)


        # Search Button for Student
        search_student_button = Button(search_button_frame, text="Search By Student", command=self.search_by_student, bg="orange", fg="white", width=20)
        search_student_button.grid(row=0, column=0, padx=10, pady=5, sticky=W)

        # Search Button for All
        search_all_button = Button(search_button_frame, text="Search All", command=self.search_attendance, bg="orange", fg="white", width=20)
        search_all_button.grid(row=1, column=0, padx=10, pady=5, sticky=W)

#-------------------------------------------------------------------------------------------------------------------------------
        # Lower Section - Table Section inside a LabelFrame
        lower_frame = LabelFrame(main_frame, text="Attendance Records", bg="white", fg="black")
        lower_frame.place(x=5, y=270, width=785, height=200)

        # Create a frame for the Treeview
        self.tree_frame = Frame(lower_frame, bd=2, relief=RIDGE)
        self.tree_frame.pack(fill=BOTH, expand=True)  # Use pack to fill the lower_frame

        # Scrollbar for the Treeview
        scroll_x = Scrollbar(self.tree_frame, orient=HORIZONTAL)
        scroll_y = Scrollbar(self.tree_frame, orient=VERTICAL)

        # Create the Treeview with additional columns
        self.attendance_table = ttk.Treeview(self.tree_frame, 
                                            columns=("student_id", "student_name", "start_time", "recorder_timer", "end_time", "attendance_status", "date", "course", "course_hour"),
                                            xscrollcommand=scroll_x.set, yscrollcommand=scroll_y.set)

        # Pack the Scrollbars
        scroll_x.pack(side=BOTTOM, fill=X)
        scroll_y.pack(side=RIGHT, fill=Y)

        # Configure the Scrollbars
        scroll_x.config(command=self.attendance_table.xview)
        scroll_y.config(command=self.attendance_table.yview)

        # Defining column headings
        self.attendance_table.heading("student_id", text="Student ID")
        self.attendance_table.heading("student_name", text="Student Name")
        self.attendance_table.heading("start_time", text="Start Time")
        self.attendance_table.heading("recorder_timer", text="Recorder Timer")
        self.attendance_table.heading("end_time", text="End Time")
        self.attendance_table.heading("attendance_status", text="Attendance Status")
        self.attendance_table.heading("date", text="Date")
        self.attendance_table.heading("course", text="Course")
        self.attendance_table.heading("course_hour", text="Course Hour")

        self.attendance_table["show"] = "headings"  # Show headings only

        # Set fixed column widths
        self.attendance_table.column("student_id", width=100, minwidth=100, stretch=False)
        self.attendance_table.column("student_name", width=150, minwidth=150, stretch=False)
        self.attendance_table.column("start_time", width=100, minwidth=100, stretch=False)
        self.attendance_table.column("recorder_timer", width=120, minwidth=120, stretch=False)
        self.attendance_table.column("end_time", width=100, minwidth=100, stretch=False)
        self.attendance_table.column("attendance_status", width=150, minwidth=150, stretch=False)
        self.attendance_table.column("date", width=100, minwidth=100, stretch=False)
        self.attendance_table.column("course", width=150, minwidth=150, stretch=False)
        self.attendance_table.column("course_hour", width=100, minwidth=100, stretch=False)

        # Pack the Treeview
        self.attendance_table.pack(fill=BOTH, expand=1)

        # Add the Treeview to the scrollbars
        self.attendance_table.configure(yscrollcommand=scroll_y.set, xscrollcommand=scroll_x.set)



        self.search_attendance()
    


        





#-----------------------------------------------------------------------------------------------------------------------------------------------   

    
    # Search by Student function
    def search_by_student(self):
        # Clear previous data in the Treeview
        for item in self.attendance_table.get_children():
            self.attendance_table.delete(item)

        student_id = self.search_entry_id.get().strip()
        student_name = self.search_entry_name.get().strip()
        teacher_name = self.username

        # Check if both fields are empty
        if not student_id and not student_name:
            messagebox.showwarning("Input Required", "Please enter either a Student ID or Student Name to search.")
            return  # Stop the function if both fields are empty
        
        # Check if both fields are filled
        if student_id and student_name:
            messagebox.showwarning("Input Error", "Please fill only one field, either Student ID or Student Name, not both.")
            return  # Stop the function if both fields are filled

        try:
            # Establish the connection to the database
            connection = mysql.connector.connect(
                host='localhost',        # Change if necessary
                user='root',             # Your MySQL username
                password='Nightcore_1134372019!',  # Your MySQL password
                database='attendnow'     # Your database name
            )
            
            cursor = connection.cursor()

            # Prepare the SQL query
            query = """
            SELECT student_id, student_name, start_time, recorder_timer, end_time, 
                attendance_status, date, course, course_hour 
            FROM attendance_status 
            WHERE student_id = %s AND teacher = %s OR student_name = %s AND teacher = %s
            """
            cursor.execute(query, (student_id, teacher_name,student_name, teacher_name))

            # Fetch all the records
            records = cursor.fetchall()

            # Insert records into the Treeview
            for record in records:
                self.attendance_table.insert('', 'end', values=record)

            if not records:
                messagebox.showinfo("No Records", "No attendance records found for the given Student ID or Name.")

        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Error: {err}")
        finally:
            # Close the database connection
            if connection.is_connected():
                cursor.close()
                connection.close()

    
   

    # Search by Student function
    def search_attendance(self):
        # Clear previous data in the Treeview
        for item in self.attendance_table.get_children():
            self.attendance_table.delete(item)

        try:
            # Establish the connection to the database
            connection = mysql.connector.connect(
                host='localhost',        # Change if necessary
                user='root',             # Your MySQL username
                password='Nightcore_1134372019!',  # Your MySQL password
                database='attendnow'     # Your database name
            )
            
            cursor = connection.cursor()

            # Define the SQL query to fetch data for the specific teacher
            query = """
                SELECT student_id, student_name, start_time, recorder_timer, end_time, attendance_status, date, course, course_hour
                FROM attendance_status
                WHERE teacher = %s
            """
            
            # Execute the query with the teacher name (self.username)
            cursor.execute(query, (self.username,))

            # Fetch all the records
            records = cursor.fetchall()

            # Insert records into the Treeview
            for record in records:
                self.attendance_table.insert('', 'end', values=record)

        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Error: {err}")
        finally:
            # Close the database connection
            if connection.is_connected():
                cursor.close()
                connection.close()


    # Go back function
    def go_back(self):
        self.root.destroy()
        new_window = Tk()
        teacher_interface.Teacher_Interface(new_window, self.username)


if __name__ == "__main__":
    root = Tk()
    root.resizable(False, False)
    obj = Attendance_Status_Interface_Teacher(root, "Jackie Chan")
    root.mainloop()
