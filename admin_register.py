from tkinter import Tk, Label, Button, Entry, Frame, LabelFrame, StringVar
from tkinter import ttk
from PIL import Image, ImageTk
import mysql.connector
import tkinter.messagebox as messagebox 
import re 

class Admin_Register:
    def __init__(self, root, username):
        self.root = root
        self.root.title("Admin Register")
        self.root.geometry("1024x590")

        # Database Connection
        self.conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="Nightcore_1134372019!",
            database="attendnow"
        )
        self.cursor = self.conn.cursor()

        # Background Image
        background_img_main = Image.open(r"Image\Background.png")   
        background_img_main = background_img_main.resize((1024, 590), Image.Resampling.LANCZOS)
        self.photo_background_img_main = ImageTk.PhotoImage(background_img_main)
        background_img_main_position = Label(self.root, image=self.photo_background_img_main)
        background_img_main_position.place(x=0, y=0, width=1024, height=590)

        # Left Title Image
        left_title = Image.open(r"Image\LogoTitle_Left Top.png")
        self.photoleft_title = ImageTk.PhotoImage(left_title)
        left_title_position = Label(self.root, image=self.photoleft_title)
        left_title_position.place(x=0, y=0, width=163, height=60)

        # Back Button
        back_button = Button(self.root, text="Back", command=self.back_to_main, bg="blue", fg="white", font=("Arial", 12, "bold"))
        back_button.place(x=175, y=15, width=80, height=30)
        
        # Display Username
        self.username_label = Label(self.root, text=f"Logged in as: {username}", bg="orange", fg="white", font=("Arial", 12))
        self.username_label.place(x=800, y=15)

        # Main Title
        main_title = Label(background_img_main_position, text="Admin Registration", bg="orange", fg="white", font=("Arial", 20, "bold"))
        main_title.place(x=300, y=2, width=400, height=40)

        # Middle Orange Frame
        middle_frame = Frame(self.root, bg="orange")
        middle_frame.place(x=50, y=100, width=900, height=400)

        # Left Side: Form for Admin Input
        form_frame = LabelFrame(middle_frame, text="Admin Registration Form", bg="white", fg="black")
        form_frame.place(x=20, y=20, width=400, height=190)

        # Form Fields
        self.first_name_entry = Entry(form_frame)
        self.last_name_entry = Entry(form_frame)
        self.username_entry = Entry(form_frame)
        self.password_entry = Entry(form_frame)
        self.email_entry = Entry(form_frame)
        
        # Placing Labels and Entries
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

        # Button Frame and Buttons
        button_frame = LabelFrame(middle_frame, text="Actions", bg="white", fg="black")
        button_frame.place(x=20, y=220, width=400, height=60)
        Button(button_frame, text="Add", bg="orange", fg="white", width=8, command=self.add_record).grid(row=0, column=0, padx=10, pady=5)
        Button(button_frame, text="Delete", bg="orange", fg="white", width=8, command=self.delete_record).grid(row=0, column=1, padx=10, pady=5)
        Button(button_frame, text="Update", bg="orange", fg="white", width=8, command=self.update_record).grid(row=0, column=2, padx=10, pady=5)
        Button(button_frame, text="Reset", bg="orange", fg="white", width=8, command=self.reset_form).grid(row=0, column=3, padx=10, pady=5)

        # Search Frame
        search_frame = LabelFrame(middle_frame, text="Search Table", bg="white", fg="black")
        search_frame.place(x=20, y=290, width=400, height=90)
        search_label = Label(search_frame, text="Search:", bg="white", fg="black")
        search_label.grid(row=0, column=0, padx=5, pady=5, sticky="w")

        # Search Options
        search_options = ["First Name", "Last Name", "Username", "Email"]
        self.search_by = StringVar()
        self.search_by_combobox = ttk.Combobox(search_frame, textvariable=self.search_by, values=search_options, state="readonly")
        self.search_by_combobox.grid(row=0, column=1, padx=10, pady=5)
        self.search_by_combobox.set("Select")
        self.search_entry = Entry(search_frame)
        self.search_entry.grid(row=0, column=2, padx=10, pady=5)
        Button(search_frame, text="Search", bg="orange", fg="white", width=8, command=self.search_record).grid(row=1, column=0, padx=10, pady=5)
        Button(search_frame, text="Show All", bg="orange", fg="white", width=8, command=self.show_all_records).grid(row=1, column=1, padx=10, pady=5)

        # Treeview for Admin List
        table_frame = Frame(middle_frame, bg="orange")
        table_frame.place(x=450, y=20, width=420, height=360)
        columns = ("First Name", "Last Name", "Username", "Password", "Email")
        self.admin_table = ttk.Treeview(table_frame, columns=columns, show="headings")
        for col in columns:
            self.admin_table.heading(col, text=col)
            self.admin_table.column(col, anchor="center", width=80)
        self.admin_table.pack(fill="both", expand=True)

        self.show_all_records()

    # Function to Show All Records
    def show_all_records(self):
        # Clear existing rows in the table
        for row in self.admin_table.get_children():
            self.admin_table.delete(row)
        
        # Fetch data from the database
        query = "SELECT first_name, last_name, user_name, user_password, email FROM admin_user"
        self.cursor.execute(query)
        rows = self.cursor.fetchall()
        
        # Insert data into the Treeview
        for row in rows:
            self.admin_table.insert("", "end", values=row)

    # Placeholder functions for other operations
    def add_record(self):
        # Get values from entry fields
        first_name = self.first_name_entry.get().strip()
        last_name = self.last_name_entry.get().strip()
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()
        email = self.email_entry.get().strip()

        # Basic validation to ensure no fields are empty
        if not first_name or not last_name or not username or not password or not email:
            messagebox.showwarning("Input Error", "All fields are required")
            return

        # Validate first and last name (no special characters or numbers, only alphabets)
        if not re.match(r"^[A-Za-z]+$", first_name):
            messagebox.showwarning("Input Error", "First name can only contain alphabets.")
            return
        if not re.match(r"^[A-Za-z]+$", last_name):
            messagebox.showwarning("Input Error", "Last name can only contain alphabets.")
            return

        # Validate username (no special characters)
        if not re.match(r"^[A-Za-z0-9]+$", username):
            messagebox.showwarning("Input Error", "Username can only contain letters and numbers, no special characters.")
            return

        # Validate password (8-20 characters)
        if not (8 <= len(password) <= 20):
            messagebox.showwarning("Input Error", "Password must be between 8 and 20 characters.")
            return

        # Validate email (must contain "@" and ".com")
        if not re.match(r"^[\w\.-]+@[\w\.-]+\.(com)$", email):
            messagebox.showwarning("Input Error", "Invalid email format. Must contain '@' and end with '.com'.")
            return

        # Check if the username already exists in the database
        try:
            self.cursor.execute("SELECT COUNT(*) FROM admin_user WHERE user_name = %s", (username,))
            result = self.cursor.fetchone()
            
            if result[0] > 0:  # If the count is greater than 0, the username exists
                messagebox.showerror("Username Error", "Username is not acceptable, it already exists.")
                return

            # Insert data into the database
            insert_query = """
                INSERT INTO admin_user (first_name, last_name, user_name, user_password, email)
                VALUES (%s, %s, %s, %s, %s)
            """
            self.cursor.execute(insert_query, (first_name, last_name, username, password, email))
            self.conn.commit()  # Commit the transaction

            # Confirm successful insertion
            messagebox.showinfo("Success", "Record added successfully")

            # Reset the form and refresh the table
            self.reset_form()
            self.show_all_records()  # Refresh to show the new record

        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Error: {err}")
    
    def delete_record(self):
        print("Delete button clicked")

    def update_record(self):
        print("Update button clicked")

    def reset_form(self):
        self.first_name_entry.delete(0, 'end')
        self.last_name_entry.delete(0, 'end')
        self.username_entry.delete(0, 'end')
        self.password_entry.delete(0, 'end')
        self.email_entry.delete(0, 'end')
 

    def search_record(self):
        print("Search button clicked")

    def back_to_main(self):
        print("Back button clicked")

# Initialize the window and run the application
if __name__ == "__main__":
    root = Tk()
    app = Admin_Register(root, "Admin")
    root.mainloop()
