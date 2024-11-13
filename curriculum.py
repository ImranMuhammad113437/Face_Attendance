from tkinter import *
from tkinter import ttk
from PIL import Image, ImageTk
import os
import admit_interface  
import mysql.connector  
from tkinter import messagebox
import sys
import curriculum

class Curriculum_Interface:
    def __init__(self, root, username):
        self.root = root
        self.username = username  
        self.root.geometry("1024x590+0+0")
        self.root.title("AttendNow - Curriculum")

        self.var_department = StringVar()
        self.var_course = StringVar()

        
        self.conn = self.connect_to_db()

        
        background_img_main = Image.open(r"Image\Background.png")
        background_img_main = background_img_main.resize((1024, 590), Image.Resampling.LANCZOS)
        self.photo_background_img_main = ImageTk.PhotoImage(background_img_main)
        background_img_main_position = Label(self.root, image=self.photo_background_img_main)
        background_img_main_position.place(x=0, y=0, width=1024, height=590)

        
        left_title = Image.open(r"Image\LogoTitle_Left Top.png")
        self.photoleft_title = ImageTk.PhotoImage(left_title)
        left_title_position = Label(self.root, image=self.photoleft_title)
        left_title_position.place(x=0, y=0, width=163, height=60)

        
        title_frame = Frame(background_img_main_position, bd=2, bg="orange")
        title_frame.place(x=300, y=5, width=450, height=50)
        title_label = Label(title_frame, text="Curriculum Management Table", bg="orange", fg="white", font=("New Time Roman", 20, "bold"))
        title_label.place(x=2, y=2, width=445, height=40)

        
        back_button = Button(self.root, text="Back", command=self.go_back, bg="red", fg="white", font=("Arial", 12, "bold"))
        back_button.place(x=175, y=15, width=80, height=30)

        
        self.username_label = Label(self.root, text=f"Logged in as: {self.username}", bg="orange", fg="white", font=("Arial", 12))
        self.username_label.place(x=800, y=15)

        
        main_frame = Frame(background_img_main_position, bd=2, bg="orange")
        main_frame.place(x=150, y=100, width=700, height=450)

        
        refresh_button = Button(background_img_main_position, text="Refresh Page", bg="orange", fg="white", width=19, command=lambda: self.refresh_page(username))
        refresh_button.place(x=860, y=530)  


        
        upper_frame = LabelFrame(main_frame, bd=2, relief=RIDGE, text="Curriculum Table", bg="white")
        upper_frame.place(x=5, y=5, width=687, height=185)  

        
        search_frame = LabelFrame(upper_frame, bd=2, relief=RIDGE, text="Search System")
        search_frame.place(x=5, y=5, width=676, height=50)

        
        search_label = Label(search_frame, text="Search By: ")
        search_label.grid(row=0, column=0)

        
        self.search_dropdown = ttk.Combobox(search_frame, state="readonly", width=12)
        self.search_dropdown["values"] = ("Select Search", "Department", "Course")
        self.search_dropdown.current(0)
        self.search_dropdown.grid(row=0, column=1, padx=3, pady=5, sticky=W)

        
        self.search_input_dropdown = ttk.Combobox(search_frame, state="readonly", width=30)
        self.search_input_dropdown.grid(row=0, column=2, padx=3, pady=5, sticky=W)

        
        search_button = Button(search_frame, text="Search", bg="orange", fg="white", width=19, command=self.show_search)
        search_button.grid(row=0, column=3, padx=3)

        
        show_all_button = Button(search_frame, text="Show All", bg="orange", fg="white", width=20, command=self.fetch_data)
        show_all_button.grid(row=0, column=4, padx=3)

        
        
        curriculum_editing_frame = LabelFrame(upper_frame, bd=2, relief=RIDGE, text="Curriculum Editing", bg="white")
        curriculum_editing_frame.place(x=5, y=60, width=676, height=90)  

       
        
        button_width = 22  

        
        department_label = Label(curriculum_editing_frame, text="Department:", bg="white", fg="black", font=("Arial", 10))
        department_label.grid(row=0, column=2, padx=10, pady=3, sticky=W)
        self.department_input = ttk.Entry(curriculum_editing_frame, width=30)
        self.department_input.grid(row=0, column=3, padx=10, pady=3)

        course_label = Label(curriculum_editing_frame, text="Course:", bg="white", fg="black", font=("Arial", 10))
        course_label.grid(row=1, column=2, padx=10, pady=3, sticky=W)
        self.course_input = ttk.Entry(curriculum_editing_frame, width=30)
        self.course_input.grid(row=1, column=3, padx=10, pady=3)

        
        add_button = Button(curriculum_editing_frame, text="Add", bg="orange", fg="white", width=button_width, command=self.add_data)
        add_button.grid(row=0, column=0, padx=3, pady=3)

        delete_button = Button(curriculum_editing_frame, text="Delete", bg="orange", fg="white", width=button_width, command=self.delete_data)
        delete_button.grid(row=0, column=1, padx=3, pady=3)

        reset_button = Button(curriculum_editing_frame, text="Reset", bg="orange", fg="white", width=button_width, command=self.reset_fields)
        reset_button.grid(row=1, column=0, padx=3, pady=3)


        
        lower_frame = LabelFrame(main_frame, bd=2, relief=RIDGE, text="Curriculum Table Management", bg="white")
        lower_frame.place(x=5, y=200, width=687, height=237)  

        
        database_frame = LabelFrame(lower_frame, bd=2, relief=RIDGE)
        database_frame.place(x=5, y=5, width=677, height=210)

        
        scroll_left_right = ttk.Scrollbar(database_frame, orient=HORIZONTAL)
        scroll_up_down = ttk.Scrollbar(database_frame, orient=VERTICAL)

        
        self.student_database = ttk.Treeview(database_frame, columns=("Department", "Course"),
                                              xscrollcommand=scroll_left_right.set, 
                                              yscrollcommand=scroll_up_down.set)

        
        scroll_up_down.pack(side=RIGHT, fill=Y)       
        scroll_up_down.config(command=self.student_database.yview)

        
        self.student_database.heading("Department", text="Department")
        self.student_database.heading("Course", text="Course")

        
        self.student_database["show"] = "headings"

        
        self.student_database.column("Department", width=200)  
        self.student_database.column("Course", width=200)      

        
        self.student_database.pack(fill=BOTH, expand=1)
        self.student_database.bind("<ButtonRelease>", self.get_cursor)
        self.search_dropdown.bind("<<ComboboxSelected>>", self.course_combolist)


        self.fetch_data()  

    def refresh_page(self, username):
        self.root.destroy()  
        new_window = Tk()  
        curriculum.Curriculum_Interface(new_window, username)

    def connect_to_db(self):
        try:
            conn = mysql.connector.connect(
                host="localhost",
                user="root",
                password="Nightcore_1134372019!",
                database="attendnow"
            )
            return conn
        except mysql.connector.Error as err:
            print(f"Error: {err}")
            return None

    def go_back(self):
        self.root.destroy()  
        self.open_admit_interface()  

    def open_admit_interface(self):
        new_window = Tk()  
        admit_interface.Admit_Interface(new_window, self.username)  


    
    def course_combolist(self, event):
        selected_option = self.search_dropdown.get()

        try:
            
            connection = mysql.connector.connect(
                host="localhost",
                user="root",
                password="Nightcore_1134372019!",
                database="attendnow"
            )
            cursor = connection.cursor()

            if selected_option == "Department":
                
                cursor.execute("SELECT DISTINCT department FROM curriculum")
                departments = cursor.fetchall()

                
                department_list = ["Select Department"] + [department[0] for department in departments]
                self.search_input_dropdown["values"] = department_list

            elif selected_option == "Course":
                
                cursor.execute("SELECT DISTINCT course FROM curriculum")
                courses = cursor.fetchall()

                
                course_list = ["Select Course"] + [course[0] for course in courses]
                self.search_input_dropdown["values"] = course_list

            else:
                
                self.search_input_dropdown["values"] = ("Select Option",)

            
            self.search_input_dropdown.current(0)

        except mysql.connector.Error as err:
            
            messagebox.showerror("Database Error", f"Error: {str(err)}")

        finally:
            
            if connection.is_connected():
                cursor.close()
                connection.close()


    def fetch_data(self):
        try:
            
            conn = mysql.connector.connect(
                host="localhost",
                user="root",
                password="Nightcore_1134372019!",
                database="attendnow"
            )

            
            cursor = conn.cursor()
            cursor.execute("SELECT Department, Course FROM curriculum")
            
            
            data = cursor.fetchall()

            
            if len(data) != 0:
                self.student_database.delete(*self.student_database.get_children())  
                for row in data:
                    self.student_database.insert("", "end", values=row)

        except mysql.connector.Error as err:
            print(f"Error: {err}")

        finally:
            
            if conn.is_connected():
                cursor.close()
                conn.close()

    
    def show_search(self):
        if self.conn and self.search_input_dropdown.get():
            cursor = self.conn.cursor()
            
            
            search_column = self.search_dropdown.get()
            search_value = self.search_input_dropdown.get()
            
            
            query = f"SELECT Department, Course FROM curriculum WHERE {search_column} = %s"
            
            
            cursor.execute(query, (search_value,))
            
            
            rows = cursor.fetchall()
            
            
            self.student_database.delete(*self.student_database.get_children())
            
            if rows:
                for row in rows:
                    self.student_database.insert('', 'end', values=row)
                    
            
            cursor.close()


    
    def add_data(self):
        
        if self.department_input.get() == "Select Department" or self.course_input.get() == "Select Course":
            messagebox.showerror("Missing Field", "All fields are required to be filled!", parent=self.root)
        else:
            try:
                
                conn = mysql.connector.connect(
                    host="localhost",
                    user="root",
                    password="Nightcore_1134372019!",
                    database="attendnow"
                )
                cursor = conn.cursor()

                
                query = "INSERT INTO curriculum (Department, Course) VALUES (%s, %s)"
                values = (self.department_input.get(), self.course_input.get())
                cursor.execute(query, values)

                
                conn.commit()
                
                self.fetch_data()

                
                messagebox.showinfo("Successful", "Data added successfully", parent=self.root)
            except mysql.connector.Error as err:
                messagebox.showerror("Error", f"Error: {err}", parent=self.root)
            finally:
                if conn.is_connected():
                    cursor.close()
                    conn.close()

    def delete_data(self):
        
        selected_item = self.student_database.selection()
        if not selected_item:
            print("Please select a record to delete.")
            return

        
        item_values = self.student_database.item(selected_item, 'values')
        if item_values:
            department, course = item_values

            
            confirm = messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete the course '{course}' from the department '{department}'?")
            if confirm:
                
                try:
                    cursor = self.conn.cursor()

                    
                    query = "DELETE FROM curriculum WHERE Department = %s AND Course = %s"
                    values = (department, course)
                    cursor.execute(query, values)

                    
                    self.conn.commit()

                    
                    self.fetch_data()

                    print("Data deleted successfully")
                except mysql.connector.Error as err:
                    print(f"Error: {err}")
                finally:
                    cursor.close()
        else:
            print("No valid selection made.")

    def reset_fields(self):
        
        self.search_dropdown.set("Select Search")

        
        self.search_input_dropdown.set("Select Option")

        
        self.department_input.delete(0, END)

        
        self.course_input.delete(0, END)



    def get_cursor(self, event=""):
        
        cursor_focus = self.student_database.focus()
        
        
        content = self.student_database.item(cursor_focus)
        
        
        data = content["values"]
        
        
        if data:
            self.department_input.delete(0, END)  
            self.department_input.insert(END, data[0])  
            
            self.course_input.delete(0, END)  
            self.course_input.insert(END, data[1])  



if __name__ == "__main__":
    root = Tk()
    app = Curriculum_Interface(root, "TeacherName")  
    root.mainloop()
