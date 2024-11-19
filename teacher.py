from tkinter import *
from tkinter import ttk
from PIL import Image, ImageTk
import os
import admit_interface  # Import admit_interface for the back button functionality
import mysql.connector  # Import MySQL Connector
from tkinter import messagebox


class Teacher_Interface:
    def __init__(self, root, username):
        self.root = root
        self.username = username  # Storing username for future use
        self.root.geometry("1024x590")  # Adjusted window size for side-by-side layout
        self.root.title("AttendNow - Curriculum")

        self.var_full_name = StringVar()
        self.var_email = StringVar()
        self.var_password = StringVar()
        self.var_phone_number = StringVar()
        self.var_username = StringVar()


       

        # Background Image
        background_img_main = Image.open(r"Image\Background.png")
        background_img_main = background_img_main.resize((1200, 600), Image.Resampling.LANCZOS)
        self.photo_background_img_main = ImageTk.PhotoImage(background_img_main)
        background_img_main_position = Label(self.root, image=self.photo_background_img_main)
        background_img_main_position.place(x=0, y=0, width=1200, height=600)

        # LogoTitle Image
        left_title = Image.open(r"Image\LogoTitle_Left Top.png")
        self.photoleft_title = ImageTk.PhotoImage(left_title)
        left_title_position = Label(self.root, image=self.photoleft_title)
        left_title_position.place(x=0, y=0, width=163, height=60)

        # Title Bar
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
            command=self.go_back  # Function to call on click
        )
        back_button.place(x=0, y=0, width=60, height=60)

        # Bind hover events
        back_button.bind("<Enter>", on_enter)  # Hover over
        back_button.bind("<Leave>", on_leave)  # Hover out

        # Add the "Student Information" label
        save_button = Label(self.main_frame2, text="Teacher Information", bg="orange", fg="white", font=("New Time Roman", 20, "bold"))
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
       

        # Main Frame (Split into left and right)
        main_frame = Frame(self.root, bd=2, bg="orange")
        main_frame.place(x=20,y=70,width=984,height=500)

        # Left Frame for Teacher Registration Form
       # Main frame for teacher registration
        # Left side frame for the form
        left_frame = LabelFrame(main_frame, bd=2, relief=RIDGE, text="Teacher Registration Form", bg="white")
        left_frame.place(x=10, y=10, width=477, height=470)  # Adjust height to accommodate the middle frame

        # Upper frame for input fields
        upper_frame = LabelFrame(left_frame, bg="white", relief=RIDGE, text="Teacher Information")
        upper_frame.place(x=5, y=0, width=465, height=260)

        # Middle frame for search dropdowns and buttons
        middle_frame = LabelFrame(left_frame, bg="white", relief=RIDGE, text="Search & Filter")
        middle_frame.place(x=5, y=270, width=465, height=70)

        # Lower frame for buttons
        lower_frame = LabelFrame(left_frame, bg="white", relief=RIDGE, text="Actions")
        lower_frame.place(x=5, y=350, width=465, height=100)

        # Input fields in the upper frame
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
        self.password_input = ttk.Entry(upper_frame, show="*", width=40,textvariable=self.var_password)  # Hides the password input
        self.password_input.grid(row=3, column=1, padx=10, pady=10)

        phone_number_label = Label(upper_frame, text="Phone Number:", bg="white", fg="black", )
        phone_number_label.grid(row=4, column=0, padx=10, pady=10, sticky=W)
        self.phone_number_input = ttk.Entry(upper_frame, width=40, textvariable=self.var_phone_number)
        self.phone_number_input.grid(row=4, column=1, padx=10, pady=10)

        # Username Label and Input
        username_label = Label(upper_frame, text="Username:", bg="white", fg="black")
        username_label.grid(row=5, column=0, padx=10, pady=10, sticky=W)
        self.username_input = ttk.Entry(upper_frame, width=40, textvariable=self.var_username)
        self.username_input.grid(row=5, column=1, padx=10, pady=10)

        # Search dropdowns and buttons in the middle frame
        search_label_1 = Label(middle_frame, text="Search By:", bg="white", fg="black")
        search_label_1.grid(row=0, column=0, padx=3, pady=5, sticky=W)
        
        # Dropdown menu with specified list including a default "Select Option"
        self.search_dropdown_1 = ttk.Combobox(middle_frame, width=12, state="readonly")
        self.search_dropdown_1['values'] = ("Select Option", "Full Name", "Email Address", "Password", "Phone Number", "Username")
        self.search_dropdown_1.grid(row=0, column=1, padx=3, pady=5)

        # Set "Select Option" as the default value
        self.search_dropdown_1.current(0)  # Sets "Select Option" as the default option


        self.search_dropdown_2 = ttk.Combobox(middle_frame, width=15, state="readonly")
        self.search_dropdown_2.grid(row=0, column=2, padx=3, pady=5)

        search_button = Button(middle_frame, text="Search", bg="orange", fg="white", width=10,command=self.search_database)
        search_button.grid(row=0, column=4, padx=3, pady=5)

        show_all_button = Button(middle_frame, text="Show All", bg="orange", fg="white", width=10,command=self.fetch_data)
        show_all_button.grid(row=0, column=5, padx=3, pady=5)

        # Buttons in the lower frame
        button_width = 28
        add_button = Button(lower_frame, text="Add", bg="orange", command=self.add_data,fg="white", width=button_width)
        add_button.grid(row=0, column=0, padx=3, pady=5)

        delete_button = Button(lower_frame, text="Delete", bg="orange",command=self.delete_data, fg="white", width=button_width)
        delete_button.grid(row=0, column=1, padx=3, pady=5)

        update_button = Button(lower_frame, text="Update", bg="orange",command=self.update_data ,fg="white", width=button_width)
        update_button.grid(row=1, column=0, padx=3, pady=5)

        reset_button = Button(lower_frame, text="Reset", bg="orange", command=self.reset_fields ,fg="white", width=button_width)
        reset_button.grid(row=1, column=1, padx=3, pady=5)


        # Right Frame for Curriculum Table
        right_frame = LabelFrame(main_frame, bd=2, relief=RIDGE, text="Curriculum Table Management", bg="white")
        right_frame.place(x=497,y=10,width=475,height=470)  # Right side (table) with height 600

                # Database Frame inside the Right Section
        database_frame = LabelFrame(right_frame, bd=2, relief=RIDGE)
        database_frame.place(x=5, y=5, width=460, height=400)

        # Scrollbars
        scroll_left_right = ttk.Scrollbar(database_frame, orient=HORIZONTAL)
        scroll_up_down = ttk.Scrollbar(database_frame, orient=VERTICAL)

        # Teacher Database Treeview with added "Username" column
        self.teacher_database = ttk.Treeview(database_frame, columns=( "Full Name", "Email", "Password", "Phone Number", "Username"),
                                            xscrollcommand=scroll_left_right.set,
                                            yscrollcommand=scroll_up_down.set)

        # Packing Scrollbars
        scroll_up_down.pack(side=RIGHT, fill=Y)
        scroll_up_down.config(command=self.teacher_database.yview)

        scroll_left_right.pack(side=BOTTOM, fill=X)
        scroll_left_right.config(command=self.teacher_database.xview)

        # Setting up headings
        self.teacher_database.heading("Full Name", text="Full Name")
        self.teacher_database.heading("Email", text="Email Address")
        self.teacher_database.heading("Password", text="Password")
        self.teacher_database.heading("Phone Number", text="Phone Number")
        self.teacher_database.heading("Username", text="Username")
        # Show headings only
        self.teacher_database["show"] = "headings"

        # Setting column widths
        self.teacher_database.column("Full Name", width=200)
        self.teacher_database.column("Email", width=200)
        self.teacher_database.column("Password", width=100)  # Consider hiding this in practice
        self.teacher_database.column("Phone Number", width=100)
        self.teacher_database.column("Username", width=200)  # Adjust column width as needed

        # Packing the Treeview
        self.teacher_database.pack(fill=BOTH, expand=1)
        self.teacher_database.bind("<ButtonRelease>", self.get_cursor)
        self.fetch_data()  # Fetch data on initialization
        # Bind the function to dropdown 1's selection event
        self.search_dropdown_1.bind("<<ComboboxSelected>>", self.search_specific)


    # Event handler function to populate dropdown 2 based on dropdown 1 selection
    def search_specific(self, event):
        selected_option = self.search_dropdown_1.get()

        # Map the selected text in dropdown_1 to actual database column names
        column_mapping = {
            "Full Name": "full_name",
            "Email Address": "email",
            "Password": "password",
            "Phone Number": "phone_number",
            "Username": "user_name"
        }

        # Get the corresponding column name
        column_name = column_mapping.get(selected_option)

        if column_name:
            # Fetch the data for the selected column
            try:
                # Connect to the MySQL database
                connection = mysql.connector.connect(
                    host="localhost",  # Adjust if necessary
                    user="root",
                    password="Nightcore_1134372019!",
                    database="attendnow"
                )
                cursor = connection.cursor()

                # Query to get unique values in the selected column
                query = f"SELECT DISTINCT {column_name} FROM teacher_user"
                cursor.execute(query)
                results = cursor.fetchall()

                # Extract data from results and update dropdown_2
                values = [row[0] for row in results]  # Get the first item in each row
                self.search_dropdown_2['values'] = values  # Update dropdown_2 values

                # Optionally set a default selection
                if values:
                    self.search_dropdown_2.current(0)
                else:
                    self.search_dropdown_2.set("No data available")

            except mysql.connector.Error as e:
                print(f"Database error: {e}")
                self.search_dropdown_2.set("Error")

            finally:
                # Ensure the connection is closed
                if connection.is_connected():
                    cursor.close()
                    connection.close()

    

    def go_back(self):
        self.root.destroy()  # Close the curriculum interface
        self.open_admit_interface()  # Reopen admit interface


    def open_admit_interface(self):
        new_window = Tk()  # Create a new Tk window
        admit_interface.Admit_Interface(new_window, self.username)  # Open the admit interface with the stored username

    def fetch_data(self):
        try:
            # Connect to the database
            conn = mysql.connector.connect(
                host="localhost",  # Assuming localhost as the host
                user="root",
                password="Nightcore_1134372019!",  # Your MySQL password
                database="attendnow"
            )
            my_cursor = conn.cursor()

            # Execute the SQL query to fetch all the data from teacher_user table
            my_cursor.execute("SELECT * FROM teacher_user")
            rows = my_cursor.fetchall()  # Fetch all the rows from the table

            # Clear any existing data in the table (Treeview widget)
            if len(rows) != 0:
                self.teacher_database.delete(*self.teacher_database.get_children())  # Delete old data in Treeview
                for row in rows:
                    self.teacher_database.insert("", END, values=row)  # Insert each row into Treeview

            conn.close()  # Close the connection to the database

        except Exception as e:
            # Display an error message if something goes wrong
            messagebox.showerror("Error", f"Error due to: {str(e)}", parent=self.root)


    # Define the search function to be called when the Search button is clicked
    def search_database(self):
        selected_option = self.search_dropdown_1.get()
        search_value = self.search_dropdown_2.get()

        # Map the dropdown selection to the database column
        column_mapping = {
            "Full Name": "Full_name",
            "Email Address": "email",
            "Password": "password",
            "Phone Number": "phone_number",
            "Username": "user_name"
        }

        # Get the corresponding column name
        column_name = column_mapping.get(selected_option)

        # Only proceed if a valid column is selected and a value is entered in dropdown_2
        if column_name and search_value:
            try:
                # Connect to the MySQL database
                conn = mysql.connector.connect(
                    host="localhost",
                    user="root",
                    password="Nightcore_1134372019!",
                    database="attendnow"
                )
                my_cursor = conn.cursor()

                # Prepare the SQL query with the selected column and value
                query = f"SELECT * FROM teacher_user WHERE {column_name} = %s"
                my_cursor.execute(query, (search_value,))  # Use a parameterized query for security

                # Fetch the filtered rows
                rows = my_cursor.fetchall()

                # Clear the existing data in Treeview
                self.teacher_database.delete(*self.teacher_database.get_children())

                # Insert each row that matches the search criteria
                if rows:
                    for row in rows:
                        self.teacher_database.insert("", "end", values=row)
                else:
                    messagebox.showinfo("No Results", "No matching records found.", parent=self.root)

                conn.close()  # Close the database connection

            except mysql.connector.Error as e:
                messagebox.showerror("Database Error", f"Error: {str(e)}", parent=self.root)
        else:
            messagebox.showwarning("Invalid Search", "Please select a valid search criterion and value.", parent=self.root)


    def add_data(self):
    # Retrieve the input data from the form
        full_name = self.var_full_name.get()
        email = self.var_email.get()
        password = self.var_password.get()
        phone_number = self.var_phone_number.get()
        user_name = self.var_username.get()

        # Check if all fields are filled
        if full_name == "" or email == "" or password == "" or phone_number == "" or user_name == "":
            messagebox.showerror("Error", "All fields are required")
        else:
            try:
                # Establish the connection to the MySQL database
                connection = mysql.connector.connect(
                    host="localhost",
                    user="root",
                    password="Nightcore_1134372019!",
                    database="attendnow"
                )

                cursor = connection.cursor()

                # Insert data into the teacher_user table
                insert_query = """
                INSERT INTO teacher_user (full_name, email, password, phone_number,user_name)
                VALUES (%s, %s, %s, %s, %s)
                """
                values = (full_name, email, password, phone_number, user_name)

                cursor.execute(insert_query, values)
                connection.commit()  # Commit the transaction

                # Show a success message
                messagebox.showinfo("Success", "Teacher added successfully")

                # Reset the fields after successful insertion
                self.reset_fields()

            except mysql.connector.Error as err:
                # Handle any errors that occur
                messagebox.showerror("Database Error", f"Error: {str(err)}")
            finally:
                # Close the connection
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
                # Establish connection to the database
                conn = mysql.connector.connect(
                    host="localhost",
                    user="root",
                    password="Nightcore_1134372019!",
                    database="attendnow"
                )
                my_cursor = conn.cursor()

                # SQL delete query to delete record based on email
                sql = "DELETE FROM teacher_user WHERE full_name=%s and email=%s and password=%s and phone_number=%s and user_name=%s"
                val = (full_name, email, password, phone_number,user_name)
                my_cursor.execute(sql, val)

                conn.commit()
                self.fetch_data()
                conn.close()

                # Call fetch_data to refresh the view after deletion
                self.fetch_data()
                messagebox.showinfo("Deletion", "Successfully Deleted")

            except Exception as e:
                messagebox.showerror("Error", f"Error due to: {str(e)}")
        
    def update_data(self):
        # Retrieve the input data from the form
        full_name = self.var_full_name.get()
        email = self.var_email.get()
        password = self.var_password.get()
        phone_number = self.var_phone_number.get()
        user_name = self.var_username.get()  # Username is the unique identifier

        # Check if the user_name field is provided
        if user_name == "":
            messagebox.showerror("Error", "Username is required to update the record")
            return

        # Check if all fields are filled
        if full_name == "" or email == "" or password == "" or phone_number == "":
            messagebox.showerror("Error", "All fields are required to update the record")
            return

        try:
            # Establish a connection to the MySQL database
            connection = mysql.connector.connect(
                host="localhost",
                user="root",
                password="Nightcore_1134372019!",
                database="attendnow"
            )
            cursor = connection.cursor()

            # Update query for the teacher_user table based on user_name
            update_query = """
            UPDATE teacher_user
            SET full_name = %s, email = %s, password = %s, phone_number = %s
            WHERE user_name = %s
            """
            values = (full_name, email, password, phone_number, user_name)

            # Execute the update query
            cursor.execute(update_query, values)
            connection.commit()  # Commit the changes

            # Check if any rows were affected to confirm if the update was successful
            if cursor.rowcount > 0:
                messagebox.showinfo("Success", "Teacher record updated successfully")
            else:
                messagebox.showwarning("Not Found", "No record found with the given Username")

            # Refresh the Treeview display
            self.fetch_data()

        except mysql.connector.Error as err:
            # Display an error message if any error occurs
            messagebox.showerror("Database Error", f"Error: {str(err)}")
        finally:
            # Close the database connection
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
