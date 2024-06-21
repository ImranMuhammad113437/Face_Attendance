from tkinter import *
from tkinter import ttk 
from PIL  import Image, ImageTk
from tkinter import messagebox
import mysql.connector
import json

with open(r".vscode\settings.json") as file:
    settings = json.load(file)

connection_details = settings["sqltools.connections"][0]

class Student:
    def __init__(self,root):
        self.root=root
        self.root.geometry("1024x590+0+0")
        self.root.title("AttendNow")

    #Variable
        self.var_department=StringVar()
        self.var_course=StringVar()
        self.var_year=StringVar()
        self.var_semester=StringVar()
        self.var_student_id=StringVar()
        self.var_student_name=StringVar()
        self.var_gender=StringVar()
        self.var_date_of_birth=StringVar()
        self.var_email=StringVar()
        self.var_phone_number=StringVar()
        self.var_address=StringVar()
        self.var_teacher=StringVar()
        
        

    #Background Image
        background_img=Image.open(r"Image\Background.png")
        background_img=background_img.resize((1024, 590),Image.Resampling.LANCZOS)
        self.photo_background_img=ImageTk.PhotoImage(background_img)
        background_img_position=Label(self.root,image=self.photo_background_img)
        background_img_position.place(x=0,y=0,width=1024,height=590)




    #LogoTitle Image
        left_title=Image.open(r"Image\LogoTitle_Left Top.png")     
        self.photoleft_title=ImageTk.PhotoImage(left_title)
        left_title_position=Label(self.root,image=self.photoleft_title)
        left_title_position.place(x=0,y=0,width=163,height=60)




    #Navigation Bar
        save_button=Button(text="Student Information",bg="orange",fg="white",font=("League_Spartan"))
        save_button.place(x=200,y=15,width=150,height=40)




    #Frame
        main_frame=Frame(background_img_position,bd=2,bg="orange")
        main_frame.place(x=20,y=70,width=984,height=500)









    #Left Label Frame(Student Information: Current Course,Class Student Information)    
        left_frame=LabelFrame(main_frame,bd=2,relief=RIDGE,text="Student Information")
        left_frame.place(x=10,y=10,width=477,height=470)






    #Current Course Information
        current_course_frame=LabelFrame(left_frame,bd=2,relief=RIDGE,text="Current Course Information")
        current_course_frame.place(x=5,y=5,width=462,height=100)

        #Department Section
        department_label=Label(current_course_frame,text="Department")
        department_label.grid(row=0,column=0,padx=10,sticky=W)

        department_dropdown=ttk.Combobox(current_course_frame,textvariable=self.var_department,state="readonly")
        department_dropdown["values"]=("Select Department","Software Engineer")
        department_dropdown.current(0)
        department_dropdown.grid(row=0,column=1,pady=10,sticky=W)

        #Course Section
        course_label=Label(current_course_frame,text="Course")
        course_label.grid(row=0,column=2,padx=10,sticky=W)

        course_dropdown=ttk.Combobox(current_course_frame,textvariable=self.var_course,state="readonly")
        course_dropdown["values"]=("Select Course","Software")
        course_dropdown.current(0)
        course_dropdown.grid(row=0,column=3,pady=10,sticky=W)

        #Year Section
        year_label=Label(current_course_frame,text="Year")
        year_label.grid(row=1,column=0,padx=10,sticky=W)

        year_dropdown=ttk.Combobox(current_course_frame,textvariable=self.var_year,state="readonly")
        year_dropdown["values"]=("Select Year","2024","2025","2026")
        year_dropdown.current(0)
        year_dropdown.grid(row=1,column=1,pady=10,sticky=W)


        #Semester Section 
        semester_label=Label(current_course_frame,text="Semester")
        semester_label.grid(row=1,column=2,padx=10,sticky=W)

        semester_dropdown=ttk.Combobox(current_course_frame,textvariable=self.var_semester,state="readonly")
        semester_dropdown["values"]=("Select Semester","Semester-1","Semester-2","Semester-3","Semester-4","Semester-5","Semester-6","Semester-7","Semester-8")
        semester_dropdown.current(0)
        semester_dropdown.grid(row=1,column=3,pady=10,sticky=W)




    #Class Student Information Frame
        class_student_frame=LabelFrame(left_frame,bd=2,relief=RIDGE,text="Class Student Information")
        class_student_frame.place(x=5,y=110,width=462,height=300)

        #Student ID  Section
        student_ID_label=Label(class_student_frame,text="Student ID")
        student_ID_label.grid(row=0,column=0,padx=5,sticky=W)

        student_ID_input=ttk.Entry(class_student_frame,textvariable=self.var_student_id)
        student_ID_input.grid(row=0,column=1,pady=10,sticky=W)

        #Student Name
        student_Name_label=Label(class_student_frame,text="Student Name")
        student_Name_label.grid(row=0,column=2,padx=5,sticky=W)

        student_Name_input=ttk.Entry(class_student_frame,textvariable=self.var_student_name)
        student_Name_input.grid(row=0,column=3,pady=10,sticky=W)

        #Gender
        gender_label=Label(class_student_frame,text="Gender")
        gender_label.grid(row=1,column=0,padx=5,sticky=W)

        gender_dropdown=ttk.Combobox(class_student_frame,textvariable=self.var_gender,state="readonly")
        gender_dropdown["values"]=("Select Gender","Male","Female")
        gender_dropdown.current(0)
        gender_dropdown.grid(row=1,column=1,pady=10,sticky=W)

        #Date of Birth
        DOB_label=Label(class_student_frame,text="Date of Birth")
        DOB_label.grid(row=1,column=2,padx=5,sticky=W)

        DOB_input=ttk.Entry(class_student_frame,textvariable=self.var_date_of_birth)
        DOB_input.grid(row=1,column=3,pady=10,sticky=W)
        #Email
        email_label=Label(class_student_frame,text="Email")
        email_label.grid(row=2,column=0,padx=5,sticky=W)

        email_input=ttk.Entry(class_student_frame,textvariable=self.var_email)
        email_input.grid(row=2,column=1,pady=10,sticky=W)

        #Phone No
        phone_num_label=Label(class_student_frame,text="Phone Number")
        phone_num_label.grid(row=2,column=2,padx=5,sticky=W)

        phone_num_input=ttk.Entry(class_student_frame,textvariable=self.var_phone_number)
        phone_num_input.grid(row=2,column=3,pady=10,sticky=W)

        #Address
        address_label=Label(class_student_frame,text="Address")
        address_label.grid(row=3,column=0,padx=5,sticky=W)

        address_input=ttk.Entry(class_student_frame,textvariable=self.var_address)
        address_input.grid(row=3,column=1,pady=10,sticky=W)

        #Teacher Name
        teacher_label=Label(class_student_frame,text="Teacher")
        teacher_label.grid(row=3,column=2,padx=5,sticky=W)

        teacher_input=ttk.Entry(class_student_frame,textvariable=self.var_teacher)
        teacher_input.grid(row=3,column=3,pady=10,sticky=W)

        
        #Selection Button
        self.var_take_photo=StringVar()
        
        take_photo_label=Label(class_student_frame,text="Photo Sample")
        take_photo_label.grid(row=4,column=0,padx=5,sticky=W)
        
        take_photo_dropdown=ttk.Combobox(class_student_frame,text="Take Photo",textvariable=self.var_take_photo,state="readonly")
        take_photo_dropdown["value"]=("Select Option","Yes","No")
        take_photo_dropdown.current(0)
        take_photo_dropdown.grid(row=4,column=1,pady=10)

        
        #Button Upper Frame Section 
        button_upper_frame=Frame(class_student_frame,bd=2,relief=RIDGE,bg="white")
        button_upper_frame.place(x=5,y=210,width=450)
        
         
        #Save Button
        save_button=Button(button_upper_frame,text="Save",command=self.add_data,bg="orange",fg="white",width=14)
        save_button.grid(row=0,column=0)

        #Update Button
        update_button=Button(button_upper_frame,text="Update",command=self.update_data,bg="orange",fg="white",width=15)
        update_button.grid(row=0,column=1)

        #Delete Button
        delete_button=Button(button_upper_frame,text="Delete",command=self.delete_data,bg="orange",fg="white",width=14)
        delete_button.grid(row=0,column=2)

        #Reset Button
        reset_button=Button(button_upper_frame,text="Reset",bg="orange",fg="white",width=15)
        reset_button.grid(row=0,column=3)

       #Button Lower Frame Section
        button_lower_frame=Frame(class_student_frame,bd=2,relief=RIDGE,bg="white")
        button_lower_frame.place(x=5,y=239,width=450)
        

        #Take Photo Sample
        take_photo_button=Button(button_lower_frame,text="Take Photo Sample",bg="orange",fg="white",width=31)
        take_photo_button.grid(row=1,column=0)
 
        #Update Photo Sample
        update_photo_button=Button(button_lower_frame,text="Update Photo Sample",bg="orange",fg="white",width=30)
        update_photo_button.grid(row=1,column=1)











    #Right Label Frame(Search System, Table Information)     
        right_frame=LabelFrame(main_frame,bd=2,relief=RIDGE,text="Student Information")
        right_frame.place(x=497,y=10,width=475,height=470)

    #Search Frame
        search_frame=LabelFrame(right_frame,bd=2,relief=RIDGE,text="Search System")
        search_frame.place(x=5,y=5,width=462,height=50)

    #Search Title
        search_label=Label(search_frame,text="Search By: ")
        search_label.grid(row=0,column=0)
    #Dropdown Menu for Searching
        search_dropdown=ttk.Combobox(search_frame,state="readonly",width=12)
        search_dropdown["values"]=("Select Search","DOD")
        search_dropdown.current(0)
        search_dropdown.grid(row=0,column=1,padx=3,pady=5,sticky=W)

    #Search InputField
        search_input=ttk.Entry(search_frame,width=15)
        search_input.grid(row=0,column=2,padx=3)
    #Search Button
        search_button=Button(search_frame,text="Search",bg="orange",fg="white",width=12)
        search_button.grid(row=0,column=3,padx=3)
    
    #Show All
        show_all_button=Button(search_frame,text="Show All",bg="orange",fg="white",width=10)
        show_all_button.grid(row=0,column=4,padx=3)









    #Database Frame
        database_frame=LabelFrame(right_frame,bd=2,relief=RIDGE)
        database_frame.place(x=5,y=55,width=462,height=390)
     
        scroll_left_right=ttk.Scrollbar(database_frame,orient=HORIZONTAL)
        scroll_up_down=ttk.Scrollbar(database_frame,orient=VERTICAL)
        self.student_database=ttk.Treeview(database_frame,columns=("Department",
                                                                   "Course",
                                                                   "Year",
                                                                   "Semester",
                                                                   "Student ID",
                                                                   "Student Name",
                                                                   "Gender",
                                                                   "Date of Birth",
                                                                   "Email",
                                                                   "Phone Number",
                                                                   "Address",
                                                                   "Teacher", 
                                                                   "Photo"),xscrollcommand=scroll_left_right.set,yscrollcommand=scroll_up_down.set)
        
        scroll_left_right.pack(side=BOTTOM,fill=X)
        scroll_up_down.pack(side=RIGHT,fill=Y)
        
        scroll_left_right.config(command=self.student_database.xview)
        scroll_up_down.config(command=self.student_database.yview)
        

        self.student_database.heading("Department",text="Department")
        self.student_database.heading("Course",text="Course")
        self.student_database.heading("Year",text="Year")
        self.student_database.heading("Semester",text="Semester")
        self.student_database.heading("Student ID",text="Student ID")
        self.student_database.heading("Student Name",text="Student Name")
        self.student_database.heading("Gender",text="Gender")
        self.student_database.heading("Date of Birth",text="Date of Birth")
        self.student_database.heading("Email",text="Email")
        self.student_database.heading("Phone Number",text="Phone Number")
        self.student_database.heading("Address",text="Address")
        self.student_database.heading("Teacher",text="Teacher")
        self.student_database.heading("Photo",text="Photo")
        self.student_database["show"]="headings"

        self.student_database.column("Department",width=100)
        self.student_database.column("Course",width=100)
        self.student_database.column("Year",width=100)
        self.student_database.column("Semester",width=100)
        self.student_database.column("Student ID",width=100)
        self.student_database.column("Student Name",width=100)
        self.student_database.column("Gender",width=100)
        self.student_database.column("Date of Birth",width=100)
        self.student_database.column("Email",width=100)
        self.student_database.column("Phone Number",width=100)
        self.student_database.column("Address",width=100)
        self.student_database.column("Teacher",width=100)
        self.student_database.column("Photo",width=100)
        
        self.student_database.pack(fill=BOTH,expand=1)
        self.student_database.bind("<ButtonRelease>",self.get_cursor)
        self.fetch_data()













    #Function

    #This is to ADD the information to the database.
    def add_data(self):
        if self.var_department.get()=="Select Department" or self.var_course.get()=="Select Course":
            messagebox.showerror("Missing Field","All Field are required to be fill!",parent=self.root)
        else:
            conn = mysql.connector.connect(
            host=connection_details["server"],
            port=connection_details["port"],
            user=connection_details["username"],
            password=connection_details["password"],
            database=connection_details["database"]
            )
            my_cursor=conn.cursor()
            my_cursor.execute("INSERT INTO students VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",
            (
                self.var_department.get(),
                self.var_course.get(),
                self.var_year.get(),
                self.var_semester.get(),
                self.var_student_id.get(),
                self.var_student_name.get(),
                self.var_gender.get(),
                self.var_date_of_birth.get(),
                self.var_email.get(),
                self.var_phone_number.get(),
                self.var_address.get(),
                self.var_teacher.get(),
                self.var_take_photo.get()
))
            conn.commit()
            self.fetch_data()
            conn.close()
            messagebox.showinfo("Successful","Student Added", parent=self.root)
        


    #This is to display the data in the table.
    def fetch_data(self):
        conn = mysql.connector.connect(
            host=connection_details["server"],
            port=connection_details["port"],
            user=connection_details["username"],
            password=connection_details["password"],
            database=connection_details["database"]
            )
        my_cursor=conn.cursor()
        my_cursor.execute("SELECT * FROM students")
        data=my_cursor.fetchall()

        if len(data)!=0:
            self.student_database.delete(*self.student_database.get_children())
            for i in data:
                self.student_database.insert("",END,values=i)
                conn.commit()
        conn.close()







      #Getting the Cursor
    
    def get_cursor(self,event=""):
        cursor_focus=self.student_database.focus()
        content=self.student_database.item(cursor_focus)
        data=content["values"]

        self.var_department.set(data[0]),
        self.var_course.set(data[1]),
        self.var_year.set(data[2]),
        self.var_semester.set(data[3]),
        self.var_student_id.set(data[4]),
        self.var_student_name.set(data[5]),
        self.var_gender.set(data[6]),
        self.var_date_of_birth.set(data[7]),
        self.var_email.set(data[8]),
        self.var_phone_number.set(data[9]),
        self.var_address.set(data[10]),
        self.var_teacher.set(data[11]),
        self.var_take_photo.set(data[12])
  
        


    #Update the information
    def update_data(self):
        if self.var_department.get()=="Select Department" or self.var_course.get()=="Select Course":
            messagebox.showerror("Missing Field","All Field are required to be fill!",parent=self.root)
        
        else:
            conn = mysql.connector.connect(
            host=connection_details["server"],
            port=connection_details["port"],
            user=connection_details["username"],
            password=connection_details["password"],
            database=connection_details["database"]
            )
            my_cursor=conn.cursor()
            my_cursor.execute("UPDATE students SET department=%s,course=%s,year=%s,semester=%s,student_name=%s,gender=%s,date_of_birth=%s,email=%s,phone_number=%s,address=%s,teacher=%s,photo_sample=%s WHERE student_id=%s",
            (
                self.var_department.get(),
                self.var_course.get(),
                self.var_year.get(),
                self.var_semester.get(),
                self.var_student_name.get(),
                self.var_gender.get(),
                self.var_date_of_birth.get(),
                self.var_email.get(),
                self.var_phone_number.get(),
                self.var_address.get(),
                self.var_teacher.get(),
                self.var_take_photo.get(),
                self.var_student_id.get()
            ))
            messagebox.showinfo("Success","Student Updated")
            conn.commit()
            self.fetch_data()
            conn.close()
            


    #Delect Function        
    def delete_data(self):
            conn = mysql.connector.connect(
                host=connection_details["server"],
                port=connection_details["port"],
                user=connection_details["username"],
                password=connection_details["password"],
                database=connection_details["database"]
            )
            my_cursor=conn.cursor()
            sql="DELETE FROM students WHERE student_id=%s"
            val=(self.var_student_id.get(),)
            my_cursor.execute(sql,val)

            conn.commit()
            self.fetch_data()
            conn.close()
            messagebox.showinfo("Deletion","Successfully Deleted")
        

if __name__ == "__main__":
    root=Tk()
    obj=Student(root)
    root.mainloop()