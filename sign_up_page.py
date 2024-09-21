from tkinter import *
from tkinter import messagebox
from PIL import Image, ImageTk
import mysql.connector

class Sign_Up_Page:
    def __init__(self, root):
        self.root = root
        self.root.geometry("1024x590+0+0")
        self.root.title("Sign Up - AttendNow")

        # Background Image
        background_img = Image.open(r"Image\Background.png")
        background_img = background_img.resize((1024, 590), Image.Resampling.LANCZOS)
        self.photo_background_img = ImageTk.PhotoImage(background_img)

        background_img_position = Label(self.root, image=self.photo_background_img)
        background_img_position.place(x=0, y=0, width=1024, height=590)

         # Logo
        logo_img = Image.open(r"Image\Logo.png")
        self.photo_logo_img = ImageTk.PhotoImage(logo_img)
        logo_label = Label(self.root, image=self.photo_logo_img)
        logo_label.place(x=100, y=222, width=150, height=150)

        # Title of the System
        title_img = Image.open(r"Image\Title.png")
        self.photo_title_img = ImageTk.PhotoImage(title_img)
        title_label = Label(self.root, image=self.photo_title_img)
        title_label.place(x=251, y=267, width=275, height=57)

        # Sign Up Form
        self.signup_frame = Frame(self.root, bg="white")
        self.signup_frame.place(x=550, y=150, width=400, height=300)

        self.username_label = Label(self.signup_frame, text="Username", bg="white", font=("Arial", 14))
        self.username_label.place(x=30, y=50)

        self.username_entry = Entry(self.signup_frame, font=("Arial", 14))
        self.username_entry.place(x=150, y=50, width=200)

        self.password_label = Label(self.signup_frame, text="Password", bg="white", font=("Arial", 14))
        self.password_label.place(x=30, y=100)

        self.password_entry = Entry(self.signup_frame, show="*", font=("Arial", 14))
        self.password_entry.place(x=150, y=100, width=200)

        self.signup_button = Button(self.signup_frame, text="Sign Up", command=self.signup, font=("Arial", 14), bg="orange", fg="white")
        self.signup_button.place(x=150, y=150, width=100)

    def signup(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        if username and password:
            # Connect to the database
            try:
                connection = mysql.connector.connect(
                    host='localhost',  # Change if necessary
                    user='root',  # Your MySQL username
                    password='Nightcore_1134372019!',  # Your MySQL password
                    database='attendnow'
                )
                
                cursor = connection.cursor()
                # Insert the user credentials into the admin_user table
                cursor.execute("INSERT INTO admin_user (user_name, user_password) VALUES (%s, %s)", (username, password))
                connection.commit()
                
                messagebox.showinfo("Sign Up Success", "Account Created Successfully!")
                
                # Redirect to the Login_Page after successful sign-up
                self.root.destroy()  # Close the current window
                from login_page import Login_Page  # Import the login page class
                new_window = Tk()  # Create a new window for the login page
                Login_Page(new_window)  # Initialize the login page
                new_window.mainloop()  # Start the login page loop

            except mysql.connector.Error as err:
                messagebox.showerror("Database Error", f"Error: {err}")
            finally:
                if connection.is_connected():
                    cursor.close()
                    connection.close()
        else:
            messagebox.showerror("Sign Up Error", "Please fill in all fields")

if __name__ == "__main__":
    root = Tk()
    obj = Sign_Up_Page(root)
    root.mainloop()
