from tkinter import Tk, Label, Button, Entry, Frame, LabelFrame, StringVar
from tkinter import ttk
from tkinter import *
from PIL import Image, ImageTk
import mysql.connector
import tkinter.messagebox as messagebox 
import re 
import admit_interface
import admin_register

class Admin_Register:
    def __init__(self, root, username):
        self.root = root
        self.root.title("Admin Register")
        self.root.geometry("1024x590")
        self.username = username

        
        self.conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="Nightcore_1134372019!",
            database="attendnow"
        )
        self.cursor = self.conn.cursor()

        
        background_img_main = Image.open(r"Image\Background.png")   
        background_img_main = background_img_main.resize((1024, 590), Image.Resampling.LANCZOS)
        self.photo_background_img_main = ImageTk.PhotoImage(background_img_main)
        background_img_main_position = Label(self.root, image=self.photo_background_img_main)
        background_img_main_position.place(x=0, y=0, width=1024, height=590)

        
        left_title = Image.open(r"Image\LogoTitle_Left Top.png")
        self.photoleft_title = ImageTk.PhotoImage(left_title)
        left_title_position = Label(self.root, image=self.photoleft_title)
        left_title_position.place(x=0, y=0, width=163, height=60)

        
        back_button = Button(self.root, text="Back", command=self.back_to_main, bg="blue", fg="white", font=("Arial", 12, "bold"))
        back_button.place(x=175, y=15, width=80, height=30)
        
        
        self.username_label = Label(self.root, text=f"Logged in as: {username}", bg="orange", fg="white", font=("Arial", 12))
        self.username_label.place(x=800, y=15)

        
        main_title = Label(background_img_main_position, text="Admin Registration", bg="orange", fg="white", font=("Arial", 20, "bold"))
        main_title.place(x=300, y=2, width=400, height=40)

        
        middle_frame = Frame(self.root, bg="orange")
        middle_frame.place(x=50, y=100, width=900, height=400)

        
        form_frame = LabelFrame(middle_frame, text="Admin Registration Form", bg="white", fg="black")
        form_frame.place(x=20, y=20, width=400, height=190)

        
        self.first_name_entry = Entry(form_frame)
        self.last_name_entry = Entry(form_frame)
        self.username_entry = Entry(form_frame)
        self.password_entry = Entry(form_frame)
        self.email_entry = Entry(form_frame)
        
        
        Label(form_frame, text="First Name:", bg="white", fg="black").grid(row=0, column=0, padx=10, pady=5, sticky="w")
        self.first_name_entry.grid(row=0, column=1, padx=10, pady=5)
        Label(form_frame, text="Last Name:", bg="white", fg="black").grid(row=1, column=0, padx=10, pady=5, sticky="w")
        self.last_name_entry.grid(row=1, column=1, padx=10, pady=5)
        Label(form_frame, text="Username:", bg="white", fg="black").grid(row=2, column=0, padx=10, pady=5, sticky="w")
        self.username_entry.grid(row=2, column=1, padx=10, pady=5)
        Label(form_frame, text="Password:", bg="white", fg="black").grid(row=3, column=0, padx=10, pady=5, sticky="w")
        self.password_entry.grid(row=3, column=1, padx=10, pady=5)
        Label(form_frame, text="Email:", bg="white", fg="black").grid(row=4, column=0, padx=10, pady=5, sticky="w")
        self.email_entry.grid(row=4, column=1, padx=10, pady=5)

       
        button_frame = LabelFrame(middle_frame, text="Actions", bg="white", fg="black")
        button_frame.place(x=20, y=220, width=400, height=60)

        
        button_frame.grid_columnconfigure(0, weight=1)
        button_frame.grid_columnconfigure(1, weight=1)
        button_frame.grid_columnconfigure(2, weight=1)
        button_frame.grid_columnconfigure(3, weight=1)

        
        Button(button_frame, text="Add", bg="orange", fg="white", command=self.add_record).grid(row=0, column=0, padx=5, pady=5, sticky="nsew")
        Button(button_frame, text="Delete", bg="orange", fg="white", command=self.delete_record).grid(row=0, column=1, padx=5, pady=5, sticky="nsew")
        Button(button_frame, text="Update", bg="orange", fg="white", command=self.update_record).grid(row=0, column=2, padx=5, pady=5, sticky="nsew")
        Button(button_frame, text="Reset", bg="orange", fg="white", command=self.reset_form).grid(row=0, column=3, padx=5, pady=5, sticky="nsew")

        
        search_frame = LabelFrame(middle_frame, text="Search Table", bg="white", fg="black")
        search_frame.place(x=20, y=290, width=400, height=90)

        
        search_label = Label(search_frame, text="Search:", bg="white", fg="black")
        search_label.grid(row=0, column=0, padx=5, pady=5, sticky="w")

        
        search_options = ["First Name", "Last Name", "Username", "Email"]
        self.search_by = StringVar()
        self.search_by_combobox = ttk.Combobox(search_frame, textvariable=self.search_by, values=search_options, state="readonly")
        self.search_by_combobox.grid(row=0, column=1, padx=5, pady=5)
        self.search_by_combobox.set("Select Option")

        
        self.search_entry_combobox = ttk.Combobox(search_frame, state="readonly")
        self.search_entry_combobox.grid(row=0, column=2, padx=5, pady=5)

        
        Button(search_frame, text="Search", bg="orange", fg="white", width=10, command=self.search_record).grid(row=1, column=0, padx=5, pady=5)
        Button(search_frame, text="Show All", bg="orange", fg="white", width=15, command=self.show_all_records).grid(row=1, column=1, padx=5, pady=5)
        Button(search_frame, text="Refresh Page", bg="orange", fg="white", width=10, command=lambda: self.refresh_page(username)).grid(row=1, column=2, padx=5, pady=5)



        
        table_frame = Frame(middle_frame, bg="orange")
        table_frame.place(x=450, y=20, width=420, height=360)
        columns = ("First Name", "Last Name", "Username", "Password", "Email")
        self.admin_table = ttk.Treeview(table_frame, columns=columns, show="headings")
        for col in columns:
            self.admin_table.heading(col, text=col)
            self.admin_table.column(col, anchor="center", width=80)
        self.admin_table.pack(fill="both", expand=True)
        
        self.admin_table.bind("<ButtonRelease-1>", self.on_admin_selected)
        
        self.search_by_combobox.bind("<<ComboboxSelected>>", self.update_search_dropdown)
        self.show_all_records()

    
    def search_record(self):
        
        search_option = self.search_by_combobox.get()
        search_value = self.search_entry_combobox.get()
        
        if not search_value:
            messagebox.showwarning("Input Error", "Please select a search value.")
            return
        
        
        column_mapping = {
            "First Name": "first_name",
            "Last Name": "last_name",
            "Username": "user_name",
            "Email": "email"
        }
        
        
        if search_option not in column_mapping:
            messagebox.showwarning("Input Error", "Please select a valid search option.")
            return
        
        
        column_name = column_mapping[search_option]
        
        
        try:
            connection = mysql.connector.connect(
                host="localhost",   
                user="root",        
                password="Nightcore_1134372019!",  
                database="attendnow"
            )
            cursor = connection.cursor()

            
            query = f"SELECT first_name, last_name, user_name, user_password, email FROM admin_user WHERE {column_name} = %s"
            
            
            cursor.execute(query, (search_value,))
            
            
            records = cursor.fetchall()
            
            
            for row in self.admin_table.get_children():
                self.admin_table.delete(row)
            
            
            for row in records:
                self.admin_table.insert("", "end", values=row)
            
            
            cursor.close()
            connection.close()

        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Error: {err}")
    
    
    def update_search_dropdown(self, event=None):
        search_values = self.fetch_search_values()  
        self.search_entry_combobox['values'] = search_values  
        if search_values:
            self.search_entry_combobox.set(search_values[0])  

    
    def fetch_search_values(self):
        search_option = self.search_by_combobox.get()  
        if search_option == "First Name":
            column = "first_name"
        elif search_option == "Last Name":
            column = "last_name"
        elif search_option == "Username":
            column = "user_name"
        elif search_option == "Email":
            column = "email"
        else:
            return []  

        
        try:
            connection = mysql.connector.connect(
                host="localhost",   
                user="root",        
                password="Nightcore_1134372019!",  
                database="attendnow"
            )
            cursor = connection.cursor()

            
            query = f"SELECT DISTINCT {column} FROM admin_user"
            cursor.execute(query)

            
            search_values = [row[0] for row in cursor.fetchall()]

            
            cursor.close()
            connection.close()

            return search_values

        except mysql.connector.Error as err:
            print(f"Error: {err}")
            return []

    
    def refresh_page(self, username):
        self.root.destroy()  
        new_window = Tk()  
        admin_register.Admin_Register(new_window, username)
    
    def show_all_records(self):
        
        for row in self.admin_table.get_children():
            self.admin_table.delete(row)
        
        
        query = "SELECT first_name, last_name, user_name, user_password, email FROM admin_user"
        self.cursor.execute(query)
        rows = self.cursor.fetchall()
        
        
        for row in rows:
            self.admin_table.insert("", "end", values=row)

    
    
    def on_admin_selected(self, event):
        
        selected_item = self.admin_table.focus()
        
        
        values = self.admin_table.item(selected_item, 'values')
        
        if values:
            
            self.first_name_entry.delete(0, END)
            self.first_name_entry.insert(0, values[0])

            self.last_name_entry.delete(0, END)
            self.last_name_entry.insert(0, values[1])

            self.username_entry.delete(0, END)
            self.username_entry.insert(0, values[2])

            self.password_entry.delete(0, END)
            self.password_entry.insert(0, values[3])

            self.email_entry.delete(0, END)
            self.email_entry.insert(0, values[4])
    
    def add_record(self):
        
        first_name = self.first_name_entry.get().strip()
        last_name = self.last_name_entry.get().strip()
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()
        email = self.email_entry.get().strip()

        
        if not first_name or not last_name or not username or not password or not email:
            messagebox.showwarning("Input Error", "All fields are required")
            return

        
        if not re.match(r"^[A-Za-z]+$", first_name):
            messagebox.showwarning("Input Error", "First name can only contain alphabets.")
            return
        if not re.match(r"^[A-Za-z]+$", last_name):
            messagebox.showwarning("Input Error", "Last name can only contain alphabets.")
            return

        
        if not re.match(r"^[A-Za-z0-9]+$", username):
            messagebox.showwarning("Input Error", "Username can only contain letters and numbers, no special characters.")
            return

        
        if not (8 <= len(password) <= 20):
            messagebox.showwarning("Input Error", "Password must be between 8 and 20 characters.")
            return

        
        if not re.match(r"^[\w\.-]+@[\w\.-]+\.(com)$", email):
            messagebox.showwarning("Input Error", "Invalid email format. Must contain '@' and end with '.com'.")
            return

        
        try:
            self.cursor.execute("SELECT COUNT(*) FROM admin_user WHERE user_name = %s", (username,))
            result = self.cursor.fetchone()
            
            if result[0] > 0:  
                messagebox.showerror("Username Error", "Username is not acceptable, it already exists.")
                return

            
            insert_query = 
            self.cursor.execute(insert_query, (first_name, last_name, username, password, email))
            self.conn.commit()  

            
            messagebox.showinfo("Success", "Record added successfully")

            
            self.reset_form()
            self.show_all_records()  

        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Error: {err}")
    
    def delete_record(self):
        
        selected_username = self.username_entry.get().strip()

        if not selected_username:
            messagebox.showerror("Error", "Username is required to delete the record")
            return

        
        confirmation = messagebox.askyesno("Confirm Deletion", f"Are you sure you want to delete the record for {selected_username}?")

        if confirmation:  
            try:
                
                connection = mysql.connector.connect(
                    host='localhost',
                    user='root',
                    password='Nightcore_1134372019!',
                    database='attendnow'
                )

                cursor = connection.cursor()

                
                sql = "DELETE FROM admin_user WHERE user_name = %s"
                val = (selected_username,)
                cursor.execute(sql, val)

                
                connection.commit()
                self.show_all_records()  

                
                messagebox.showinfo("Deletion", "Record deleted successfully")

            except mysql.connector.Error as err:
                messagebox.showerror("Database Error", f"Error due to: {str(err)}")

            finally:
                if connection.is_connected():
                    cursor.close()
                    connection.close()

        else:
            messagebox.showinfo("Deletion Cancelled", "No record was deleted.")


    def update_record(self):
        
        first_name = self.first_name_entry.get().strip()
        last_name = self.last_name_entry.get().strip()
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()
        email = self.email_entry.get().strip()

        
        if not first_name or not last_name or not username or not password or not email:
            messagebox.showwarning("Input Error", "All fields are required")
            return

        
        if not re.match(r"^[A-Za-z]+(?: [A-Za-z]+)*$", first_name):
            messagebox.showwarning("Input Error", "First name can only contain alphabets and may have a single space between words.")
            return
        if not re.match(r"^[A-Za-z]+(?: [A-Za-z]+)*$", last_name):
            messagebox.showwarning("Input Error", "Last name can only contain alphabets and may have a single space between words.")
            return

        
        if not (8 <= len(password) <= 20):
            messagebox.showwarning("Input Error", "Password must be between 8 and 20 characters.")
            return

        
        if not re.match(r"^[\w\.-]+@[\w\.-]+\.(com)$", email):
            messagebox.showwarning("Input Error", "Invalid email format. Must contain '@' and end with '.com'.")
            return

        
        try:
            
            self.cursor.execute("SELECT COUNT(*) FROM admin_user WHERE user_name = %s", (username,))
            result = self.cursor.fetchone()
            
            if result[0] == 0:  
                messagebox.showerror("Update Error", "Username does not exist.")
                return

            
            update_query = 
            self.cursor.execute(update_query, (first_name, last_name, password, email, username))
            self.conn.commit()  

            
            messagebox.showinfo("Success", "Record updated successfully")

            
            self.reset_form()
            self.show_all_records()  

        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Error: {err}")



    def reset_form(self):
        self.first_name_entry.delete(0, 'end')
        self.last_name_entry.delete(0, 'end')
        self.username_entry.delete(0, 'end')
        self.password_entry.delete(0, 'end')
        self.email_entry.delete(0, 'end')
 

    def back_to_main(self):
        self.root.destroy()  
        new_window = Tk()  
        admit_interface.Admit_Interface(new_window, self.username)


if __name__ == "__main__":
    root = Tk()
    app = Admin_Register(root, "Admin")
    root.mainloop()
