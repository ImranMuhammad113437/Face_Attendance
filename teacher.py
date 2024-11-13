from tkinter import *
from tkinter import ttk
from PIL import Image, ImageTk
import os
import admit_interface  
import mysql.connector  
from tkinter import messagebox


class Teacher_Interface:
    def __init__(self, root, username):
        self.root = root
        self.username = username  
        self.root.geometry("1024x590")  
        self.root.title("AttendNow - Curriculum")

        self.var_full_name = StringVar()
        self.var_email = StringVar()
        self.var_password = StringVar()
        self.var_phone_number = StringVar()
        self.var_username = StringVar()


       

        
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
        title_label = Label(title_frame, text="Teacher Management Table", bg="orange", fg="white", font=("New Time Roman", 20, "bold"))
        title_label.place(x=2, y=2, width=445, height=40)

        
        back_button = Button(self.root, text="Back", command=self.go_back, bg="red", fg="white", font=("Arial", 12, "bold"))
        back_button.place(x=175, y=15, width=80, height=30)

        
        self.username_label = Label(self.root, text=f"Logged in as: {self.username}", bg="orange", fg="white", font=("Arial", 12))
        self.username_label.place(x=800, y=15)

        
        main_frame = Frame(self.root, bd=2, bg="orange")
        main_frame.place(x=20,y=70,width=984,height=500)

        
       
        
        left_frame = LabelFrame(main_frame, bd=2, relief=RIDGE, text="Teacher Registration Form", bg="white")
        left_frame.place(x=10, y=10, width=477, height=470)  

        
        upper_frame = LabelFrame(left_frame, bg="white", relief=RIDGE, text="Teacher Information")
        upper_frame.place(x=5, y=0, width=465, height=260)

        
        middle_frame = LabelFrame(left_frame, bg="white", relief=RIDGE, text="Search & Filter")
        middle_frame.place(x=5, y=270, width=465, height=70)

        
        lower_frame = LabelFrame(left_frame, bg="white", relief=RIDGE, text="Actions")
        lower_frame.place(x=5, y=350, width=465, height=100)

        
        full_name_label = Label(upper_frame, text="Full Name:", bg="white", fg="black" )
        full_name_label.grid(row=0, column=0, padx=10, pady=10, sticky=W)
        self.full_name_input = ttk.Entry(upper_frame, width=40, textvariable=self.var_full_name)
        self.full_name_input.grid(row=0, column=1, padx=10, pady=10)

    
        email_label = Label(upper_frame, text="Email Address:", bg="white", fg="black" )
        email_label.grid(row=2, column=0, padx=10, pady=10, sticky=W)
        self.email_input = ttk.Entry(upper_frame, width=40,textvariable=self.var_email)
        self.email_input.grid(row=2, column=1, padx=10, pady=10)

        password_label = Label(upper_frame, text="Password:", bg="white", fg="black" )
        password_label.grid(row=3, column=0, padx=10, pady=10, sticky=W)
        self.password_input = ttk.Entry(upper_frame, show="*", width=40,textvariable=self.var_password)  
        self.password_input.grid(row=3, column=1, padx=10, pady=10)

        phone_number_label = Label(upper_frame, text="Phone Number:", bg="white", fg="black", )
        phone_number_label.grid(row=4, column=0, padx=10, pady=10, sticky=W)
        self.phone_number_input = ttk.Entry(upper_frame, width=40, textvariable=self.var_phone_number)
        self.phone_number_input.grid(row=4, column=1, padx=10, pady=10)

        
        username_label = Label(upper_frame, text="Username:", bg="white", fg="black")
        username_label.grid(row=5, column=0, padx=10, pady=10, sticky=W)
        self.username_input = ttk.Entry(upper_frame, width=40, textvariable=self.var_username)
        self.username_input.grid(row=5, column=1, padx=10, pady=10)

        
        search_label_1 = Label(middle_frame, text="Search By:", bg="white", fg="black")
        search_label_1.grid(row=0, column=0, padx=3, pady=5, sticky=W)
        
        
        self.search_dropdown_1 = ttk.Combobox(middle_frame, width=12, state="readonly")
        self.search_dropdown_1['values'] = ("Select Option", "Full Name", "Email Address", "Password", "Phone Number", "Username")
        self.search_dropdown_1.grid(row=0, column=1, padx=3, pady=5)

        
        self.search_dropdown_1.current(0)  


        self.search_dropdown_2 = ttk.Combobox(middle_frame, width=15, state="readonly")
        self.search_dropdown_2.grid(row=0, column=2, padx=3, pady=5)

        search_button = Button(middle_frame, text="Search", bg="orange", fg="white", width=10,command=self.search_database)
        search_button.grid(row=0, column=4, padx=3, pady=5)

        show_all_button = Button(middle_frame, text="Show All", bg="orange", fg="white", width=10,command=self.fetch_data)
        show_all_button.grid(row=0, column=5, padx=3, pady=5)

        
        button_width = 28
        add_button = Button(lower_frame, text="Add", bg="orange", command=self.add_data,fg="white", width=button_width)
        add_button.grid(row=0, column=0, padx=3, pady=5)

        delete_button = Button(lower_frame, text="Delete", bg="orange",command=self.delete_data, fg="white", width=button_width)
        delete_button.grid(row=0, column=1, padx=3, pady=5)

        update_button = Button(lower_frame, text="Update", bg="orange",command=self.update_data ,fg="white", width=button_width)
        update_button.grid(row=1, column=0, padx=3, pady=5)

        reset_button = Button(lower_frame, text="Reset", bg="orange", command=self.reset_fields ,fg="white", width=button_width)
        reset_button.grid(row=1, column=1, padx=3, pady=5)


        
        right_frame = LabelFrame(main_frame, bd=2, relief=RIDGE, text="Curriculum Table Management", bg="white")
        right_frame.place(x=497,y=10,width=475,height=470)  

                
        database_frame = LabelFrame(right_frame, bd=2, relief=RIDGE)
        database_frame.place(x=5, y=5, width=460, height=400)

        
        scroll_left_right = ttk.Scrollbar(database_frame, orient=HORIZONTAL)
        scroll_up_down = ttk.Scrollbar(database_frame, orient=VERTICAL)

        
        self.teacher_database = ttk.Treeview(database_frame, columns=( "Full Name", "Email", "Password", "Phone Number", "Username"),
                                            xscrollcommand=scroll_left_right.set,
                                            yscrollcommand=scroll_up_down.set)

        
        scroll_up_down.pack(side=RIGHT, fill=Y)
        scroll_up_down.config(command=self.teacher_database.yview)

        scroll_left_right.pack(side=BOTTOM, fill=X)
        scroll_left_right.config(command=self.teacher_database.xview)

        
        self.teacher_database.heading("Full Name", text="Full Name")
        self.teacher_database.heading("Email", text="Email Address")
        self.teacher_database.heading("Password", text="Password")
        self.teacher_database.heading("Phone Number", text="Phone Number")
        self.teacher_database.heading("Username", text="Username")
        
        self.teacher_database["show"] = "headings"

        
        self.teacher_database.column("Full Name", width=200)
        self.teacher_database.column("Email", width=250)
        self.teacher_database.column("Password", width=100)  
        self.teacher_database.column("Phone Number", width=100)
        self.teacher_database.column("Username", width=200)  

        
        self.teacher_database.pack(fill=BOTH, expand=1)
        self.teacher_database.bind("<ButtonRelease>", self.get_cursor)
        self.fetch_data()  
        
        self.search_dropdown_1.bind("<<ComboboxSelected>>", self.search_specific)


    
    def search_specific(self, event):
        selected_option = self.search_dropdown_1.get()

        
        column_mapping = {
            "Full Name": "full_name",
            "Email Address": "email",
            "Password": "password",
            "Phone Number": "phone_number",
            "Username": "user_name"
        }

        
        column_name = column_mapping.get(selected_option)

        if column_name:
            
            try:
                
                connection = mysql.connector.connect(
                    host="localhost",  
                    user="root",
                    password="Nightcore_1134372019!",
                    database="attendnow"
                )
                cursor = connection.cursor()

                
                query = f"SELECT DISTINCT {column_name} FROM teacher_user"
                cursor.execute(query)
                results = cursor.fetchall()

                
                values = [row[0] for row in results]  
                self.search_dropdown_2['values'] = values  

                
                if values:
                    self.search_dropdown_2.current(0)
                else:
                    self.search_dropdown_2.set("No data available")

            except mysql.connector.Error as e:
                print(f"Database error: {e}")
                self.search_dropdown_2.set("Error")

            finally:
                
                if connection.is_connected():
                    cursor.close()
                    connection.close()

    

    def go_back(self):
        self.root.destroy()  
        self.open_admit_interface()  


    def open_admit_interface(self):
        new_window = Tk()  
        admit_interface.Admit_Interface(new_window, self.username)  

    def fetch_data(self):
        try:
            
            conn = mysql.connector.connect(
                host="localhost",  
                user="root",
                password="Nightcore_1134372019!",  
                database="attendnow"
            )
            my_cursor = conn.cursor()

            
            my_cursor.execute("SELECT * FROM teacher_user")
            rows = my_cursor.fetchall()  

            
            if len(rows) != 0:
                self.teacher_database.delete(*self.teacher_database.get_children())  
                for row in rows:
                    self.teacher_database.insert("", END, values=row)  

            conn.close()  

        except Exception as e:
            
            messagebox.showerror("Error", f"Error due to: {str(e)}", parent=self.root)


    
    def search_database(self):
        selected_option = self.search_dropdown_1.get()
        search_value = self.search_dropdown_2.get()

        
        column_mapping = {
            "Full Name": "Full_name",
            "Email Address": "email",
            "Password": "password",
            "Phone Number": "phone_number",
            "Username": "user_name"
        }

        
        column_name = column_mapping.get(selected_option)

        
        if column_name and search_value:
            try:
                
                conn = mysql.connector.connect(
                    host="localhost",
                    user="root",
                    password="Nightcore_1134372019!",
                    database="attendnow"
                )
                my_cursor = conn.cursor()

                
                query = f"SELECT * FROM teacher_user WHERE {column_name} = %s"
                my_cursor.execute(query, (search_value,))  

                
                rows = my_cursor.fetchall()

                
                self.teacher_database.delete(*self.teacher_database.get_children())

                
                if rows:
                    for row in rows:
                        self.teacher_database.insert("", "end", values=row)
                else:
                    messagebox.showinfo("No Results", "No matching records found.", parent=self.root)

                conn.close()  

            except mysql.connector.Error as e:
                messagebox.showerror("Database Error", f"Error: {str(e)}", parent=self.root)
        else:
            messagebox.showwarning("Invalid Search", "Please select a valid search criterion and value.", parent=self.root)


    def add_data(self):
    
        full_name = self.var_full_name.get()
        email = self.var_email.get()
        password = self.var_password.get()
        phone_number = self.var_phone_number.get()
        user_name = self.var_username.get()

        
        if full_name == "" or email == "" or password == "" or phone_number == "" or user_name == "":
            messagebox.showerror("Error", "All fields are required")
        else:
            try:
                
                connection = mysql.connector.connect(
                    host="localhost",
                    user="root",
                    password="Nightcore_1134372019!",
                    database="attendnow"
                )

                cursor = connection.cursor()

                
                insert_query = 
                values = (full_name, email, password, phone_number, user_name)

                cursor.execute(insert_query, values)
                connection.commit()  

                
                messagebox.showinfo("Success", "Teacher added successfully")

                
                self.reset_fields()

            except mysql.connector.Error as err:
                
                messagebox.showerror("Database Error", f"Error: {str(err)}")
            finally:
                
                if connection.is_connected():
                    cursor.close()
                    connection.close()
        self.fetch_data()

    def delete_data(self):
        full_name = self.var_full_name.get()
        email = self.var_email.get()
        password = self.var_password.get()
        phone_number = self.var_phone_number.get()
        user_name = self.var_username.get()

        if email == "":
            messagebox.showerror("Error", "Email is required to delete the record")
        else:
            try:
                
                conn = mysql.connector.connect(
                    host="localhost",
                    user="root",
                    password="Nightcore_1134372019!",
                    database="attendnow"
                )
                my_cursor = conn.cursor()

                
                sql = "DELETE FROM teacher_user WHERE full_name=%s and email=%s and password=%s and phone_number=%s and user_name=%s"
                val = (full_name, email, password, phone_number,user_name)
                my_cursor.execute(sql, val)

                conn.commit()
                self.fetch_data()
                conn.close()

                
                self.fetch_data()
                messagebox.showinfo("Deletion", "Successfully Deleted")

            except Exception as e:
                messagebox.showerror("Error", f"Error due to: {str(e)}")
        
    def update_data(self):
        
        full_name = self.var_full_name.get()
        email = self.var_email.get()
        password = self.var_password.get()
        phone_number = self.var_phone_number.get()
        user_name = self.var_username.get()  

        
        if user_name == "":
            messagebox.showerror("Error", "Username is required to update the record")
            return

        
        if full_name == "" or email == "" or password == "" or phone_number == "":
            messagebox.showerror("Error", "All fields are required to update the record")
            return

        try:
            
            connection = mysql.connector.connect(
                host="localhost",
                user="root",
                password="Nightcore_1134372019!",
                database="attendnow"
            )
            cursor = connection.cursor()

            
            update_query = 
            values = (full_name, email, password, phone_number, user_name)

            
            cursor.execute(update_query, values)
            connection.commit()  

            
            if cursor.rowcount > 0:
                messagebox.showinfo("Success", "Teacher record updated successfully")
            else:
                messagebox.showwarning("Not Found", "No record found with the given Username")

            
            self.fetch_data()

        except mysql.connector.Error as err:
            
            messagebox.showerror("Database Error", f"Error: {str(err)}")
        finally:
            
            if connection.is_connected():
                cursor.close()
                connection.close()


    def reset_fields(self):
        self.var_full_name.set("")
        self.var_email.set("")
        self.var_password.set("")
        self.var_phone_number.set("")
        self.var_username.set("")
        

    def get_cursor(self, event=""):
        cursor_focus=self.teacher_database.focus()
        content=self.teacher_database.item(cursor_focus)
        data=content["values"]
        self.var_full_name.set(data[0]),
        self.var_email.set(data[1]),
        self.var_password.set(data[2]),
        self.var_phone_number.set(data[3])
        self.var_username.set(data[4])
        


if __name__ == "__main__":
    root = Tk()
    app = Teacher_Interface(root, username="Username123")
    root.mainloop()
