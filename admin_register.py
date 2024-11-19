from tkinter import Tk, Label, Button, Entry, Frame, LabelFrame, StringVar
from tkinter import ttk
from tkinter import *
import tkinter as tk
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

        
        #Title
        self.main_frame2 = Frame(background_img_main_position, bg="orange")
        self.main_frame2.place(x=180, y=10, width=824, height=60)

        # Add the "ghost button" on the left
        def on_enter(event):
            back_button.config(image=back_hover_image, bg="white")  # Change to hover image and background

        def on_leave(event):
            back_button.config(image=back_default_image, bg="red")  # Change to default image and background

    

        # Load the images using Pillow for resizing
        back_default_pil_image = Image.open("Image/back.png").resize((60, 60), Image.Resampling.LANCZOS)  # Resize to 60x60
        back_hover_pil_image = Image.open("Image/back (1).png").resize((60, 60), Image.Resampling.LANCZOS)  # Resize to 60x60

        # Convert Pillow images to Tkinter-compatible PhotoImage
        back_default_image = ImageTk.PhotoImage(back_default_pil_image)
        back_hover_image = ImageTk.PhotoImage(back_hover_pil_image)

        # Create the back button
        back_button = Button(
            self.main_frame2,
            image=back_default_image,
            bg="red",
            bd=0,  # Remove button border
            activebackground="white",  # Background color when pressed
            command=self.back_to_main  # Function to call on click
        )
        back_button.place(x=0, y=0, width=60, height=60)

        # Bind hover events
        back_button.bind("<Enter>", on_enter)  # Hover over
        back_button.bind("<Leave>", on_leave)  # Hover out

        # Add the "Student Information" label
        save_button = Label(self.main_frame2, text="Admin Registration", bg="orange", fg="white", font=("New Time Roman", 20, "bold"))
        save_button.place(x=80, y=10, width=280, height=40)  # Positioned next to the back button

        # Create the username label
        self.username_label = Label(self.main_frame2, text=f"{username}", bg="orange", fg="white", font=("Arial", 12))

        # Update x-position of the username so it aligns to the right of the frame
        frame_width = 824  # The width of the frame
        button_width = 60  # Width of the ghost button
        gap = 10           # Gap between the button and username label
        label_width = self.username_label.winfo_reqwidth()  # Get the width of the username label

        # Position the username label on the right
        self.username_label.place(x=frame_width - label_width - 10, y=0, height=60)  # 10px gap from the right edge


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

        # Configure the columns to distribute space evenly
        button_frame.grid_columnconfigure(0, weight=1)
        button_frame.grid_columnconfigure(1, weight=1)
        button_frame.grid_columnconfigure(2, weight=1)
        button_frame.grid_columnconfigure(3, weight=1)

        # Add buttons with adjusted configurations
        Button(button_frame, text="Add", bg="orange", fg="white", command=self.add_record).grid(row=0, column=0, padx=5, pady=5, sticky="nsew")
        Button(button_frame, text="Delete", bg="orange", fg="white", command=self.delete_record).grid(row=0, column=1, padx=5, pady=5, sticky="nsew")
        Button(button_frame, text="Update", bg="orange", fg="white", command=self.update_record).grid(row=0, column=2, padx=5, pady=5, sticky="nsew")
        Button(button_frame, text="Reset", bg="orange", fg="white", command=self.reset_form).grid(row=0, column=3, padx=5, pady=5, sticky="nsew")

        # Search Frame
        search_frame = LabelFrame(middle_frame, text="Search Table", bg="white", fg="black")
        search_frame.place(x=20, y=290, width=400, height=90)

        # Search Label
        search_label = Label(search_frame, text="Search:", bg="white", fg="black")
        search_label.grid(row=0, column=0, padx=5, pady=5, sticky="w")

        # Search Options
        search_options = ["First Name", "Last Name", "Username", "Email"]
        self.search_by = StringVar()
        self.search_by_combobox = ttk.Combobox(search_frame, textvariable=self.search_by, values=search_options, state="readonly")
        self.search_by_combobox.grid(row=0, column=1, padx=5, pady=5)
        self.search_by_combobox.set("Select Option")

        # Dropdown Menu for Search Entry (changed to Entry field)
        self.search_entry = tk.Entry(search_frame)
        self.search_entry.grid(row=0, column=2, padx=5, pady=5)


        # Buttons
        Button(search_frame, text="Search", bg="orange", fg="white", width=10, command=self.search_record).grid(row=1, column=0, padx=5, pady=5)
        Button(search_frame, text="Show All", bg="orange", fg="white", width=15, command=self.show_all_records).grid(row=1, column=1, padx=5, pady=5)
        Button(search_frame, text="Refresh Page", bg="orange", fg="white", width=10, command=lambda: self.refresh_page(username)).grid(row=1, column=2, padx=5, pady=5)



        # Treeview for Admin List
        table_frame = Frame(middle_frame, bg="orange")
        table_frame.place(x=450, y=20, width=420, height=360)
        columns = ("First Name", "Last Name", "Username", "Password", "Email")
        self.admin_table = ttk.Treeview(table_frame, columns=columns, show="headings")
        for col in columns:
            self.admin_table.heading(col, text=col)
            self.admin_table.column(col, anchor="center", width=80)
        self.admin_table.pack(fill="both", expand=True)
        # Adding selection cursor
        self.admin_table.bind("<ButtonRelease-1>", self.on_admin_selected)
    
        self.show_all_records()

    # Function to search and display records
    def search_record(self):
        # Get the selected search option and the value to search
        search_option = self.search_by_combobox.get()
        search_value = self.search_entry.get()  # Updated to use Entry instead of Combobox
        
        if not search_value:
            messagebox.showwarning("Input Error", "Please enter a search value.")
            return
        
        # Map search options to column names in the database
        column_mapping = {
            "First Name": "first_name",
            "Last Name": "last_name",
            "Username": "user_name",
            "Email": "email"
        }
        
        # Check if the search option is valid
        if search_option not in column_mapping:
            messagebox.showwarning("Input Error", "Please select a valid search option.")
            return
        
        # Get the corresponding column name for the search option
        column_name = column_mapping[search_option]
        
        # Connect to the database and query the data
        try:
            connection = mysql.connector.connect(
                host="localhost",   # Adjust to your DB host
                user="root",        # Your DB username
                password="Nightcore_1134372019!",  # Your DB password
                database="attendnow"
            )
            cursor = connection.cursor()

            # Create the SQL query with the WHERE condition
            query = f"SELECT first_name, last_name, user_name, user_password, email FROM admin_user WHERE {column_name} = %s"
            
            # Execute the query with the search value
            cursor.execute(query, (search_value,))
            
            # Fetch the results
            records = cursor.fetchall()
            
            # Clear the previous rows in the table
            for row in self.admin_table.get_children():
                self.admin_table.delete(row)
            
            # Insert the fetched records into the Treeview
            for row in records:
                self.admin_table.insert("", "end", values=row)
            
            # Close the cursor and the connection
            cursor.close()
            connection.close()

        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Error: {err}")

    
    
    

    
    def fetch_search_values(self):
        search_option = self.search_by_combobox.get()  # Get the selected search option
        if search_option == "First Name":
            column = "first_name"
        elif search_option == "Last Name":
            column = "last_name"
        elif search_option == "Username":
            column = "user_name"
        elif search_option == "Email":
            column = "email"
        else:
            return []  # Return an empty list if no valid option is selected

        # Connect to the database
        try:
            connection = mysql.connector.connect(
                host="localhost",   # Adjust to your DB host
                user="root",        # Your DB username
                password="Nightcore_1134372019!",  # Your DB password
                database="attendnow"
            )
            cursor = connection.cursor()

            # Query the database for the selected column
            query = f"SELECT DISTINCT {column} FROM admin_user"
            cursor.execute(query)

            # Fetch the results and return as a list
            search_values = [row[0] for row in cursor.fetchall()]

            # Close the connection
            cursor.close()
            connection.close()

            return search_values

        except mysql.connector.Error as err:
            print(f"Error: {err}")
            return []

    
    def refresh_page(self, username):
        self.root.destroy()  # Close the curriculum interface
        new_window = Tk()  # Create a new Tk window
        admin_register.Admin_Register(new_window, username)
    
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
    # Function to handle row selection and populate entries with selected row data
    def on_admin_selected(self, event):
        # Get selected row
        selected_item = self.admin_table.focus()
        
        # Fetch row data
        values = self.admin_table.item(selected_item, 'values')
        
        if values:
            # Populate entry fields with selected row data
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
        # Get the selected username to delete
        selected_username = self.username_entry.get().strip()

        if not selected_username:
            messagebox.showerror("Error", "Username is required to delete the record")
            return

        # Confirmation dialog before deletion
        confirmation = messagebox.askyesno("Confirm Deletion", f"Are you sure you want to delete the record for {selected_username}?")

        if confirmation:  # If user confirms
            try:
                # Connect to the database
                connection = mysql.connector.connect(
                    host='localhost',
                    user='root',
                    password='Nightcore_1134372019!',
                    database='attendnow'
                )

                cursor = connection.cursor()

                # SQL delete query to delete the record based on username
                sql = "DELETE FROM admin_user WHERE user_name = %s"
                val = (selected_username,)
                cursor.execute(sql, val)

                # Commit the deletion and refresh the table view
                connection.commit()
                self.show_all_records()  # Refresh the table to show the latest list

                # Success message
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

        # Validate first and last name (allow spaces in the middle but not at the start or end)
        if not re.match(r"^[A-Za-z]+(?: [A-Za-z]+)*$", first_name):
            messagebox.showwarning("Input Error", "First name can only contain alphabets and may have a single space between words.")
            return
        if not re.match(r"^[A-Za-z]+(?: [A-Za-z]+)*$", last_name):
            messagebox.showwarning("Input Error", "Last name can only contain alphabets and may have a single space between words.")
            return

        # Validate password (8-20 characters)
        if not (8 <= len(password) <= 20):
            messagebox.showwarning("Input Error", "Password must be between 8 and 20 characters.")
            return

        # Validate email (must contain "@" and ".com")
        if not re.match(r"^[\w\.-]+@[\w\.-]+\.(com)$", email):
            messagebox.showwarning("Input Error", "Invalid email format. Must contain '@' and end with '.com'.")
            return

        # Update the record in the database
        try:
            # Check if the username exists
            self.cursor.execute("SELECT COUNT(*) FROM admin_user WHERE user_name = %s", (username,))
            result = self.cursor.fetchone()
            
            if result[0] == 0:  # If the count is 0, the username doesn't exist
                messagebox.showerror("Update Error", "Username does not exist.")
                return

            # Update data in the database where username matches
            update_query = """
                UPDATE admin_user
                SET first_name = %s, last_name = %s, user_password = %s, email = %s
                WHERE user_name = %s
            """
            self.cursor.execute(update_query, (first_name, last_name, password, email, username))
            self.conn.commit()  # Commit the transaction

            # Confirm successful update
            messagebox.showinfo("Success", "Record updated successfully")

            # Reset the form and refresh the table
            self.reset_form()
            self.show_all_records()  # Refresh to show the updated record

        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Error: {err}")



    def reset_form(self):
        self.first_name_entry.delete(0, 'end')
        self.last_name_entry.delete(0, 'end')
        self.username_entry.delete(0, 'end')
        self.password_entry.delete(0, 'end')
        self.email_entry.delete(0, 'end')
 

    def back_to_main(self):
        self.root.destroy()  # Close the current window
        new_window = Tk()  # Create a new Tk window for the admit interface
        admit_interface.Admit_Interface(new_window, self.username)

# Initialize the window and run the application
if __name__ == "__main__":
    root = Tk()
    app = Admin_Register(root, "Admin")
    root.mainloop()
