from tkinter import *
from tkinter import messagebox
from PIL import Image, ImageTk
import mysql.connector
import admit_interface  # Import the admit_interface module

class Login_Page:
    def __init__(self, root):
        self.root = root
        self.root.geometry("1024x590+0+0")
        self.root.title("AttendNow")

        # Disable window resizing
        self.root.resizable(False, False)

        # Background Image
        background_img = Image.open(r"Image\Background.png")
        background_img = background_img.resize((1024, 590), Image.Resampling.LANCZOS)
        self.photo_background_img = ImageTk.PhotoImage(background_img)

        background_img_position = Label(self.root, image=self.photo_background_img)
        background_img_position.place(x=0, y=0, width=1024, height=590)

        # Title of the System
        title_img = Image.open(r"Image\Title.png")
        self.photo_title_img = ImageTk.PhotoImage(title_img)
        title_label = Label(self.root, image=self.photo_title_img)
        title_label.place(x=251, y=267, width=275, height=57)

        # Logo
        logo_img = Image.open(r"Image\Logo.png")
        self.photo_logo_img = ImageTk.PhotoImage(logo_img)
        logo_label = Label(self.root, image=self.photo_logo_img)
        logo_label.place(x=100, y=222, width=150, height=150)

        # Login Form
        self.login_frame = Frame(self.root, bg="white")
        self.login_frame.place(x=550, y=150, width=400, height=300)

        self.username_label = Label(self.login_frame, text="Username", bg="white", font=("Arial", 14))
        self.username_label.place(x=30, y=50)

        self.username_entry = Entry(self.login_frame, font=("Arial", 14))
        self.username_entry.place(x=150, y=50, width=200)

        self.password_label = Label(self.login_frame, text="Password", bg="white", font=("Arial", 14))
        self.password_label.place(x=30, y=100)

        self.password_entry = Entry(self.login_frame, show="*", font=("Arial", 14))
        self.password_entry.place(x=150, y=100, width=200)

        self.login_button = Button(self.login_frame, text="Login", command=self.login, font=("Arial", 14), bg="orange", fg="white")
        self.login_button.place(x=150, y=150, width=100)

        self.signup_button = Button(self.login_frame, text="Sign Up", command=self.open_signup_interface, font=("Arial", 14), bg="orange", fg="white")
        self.signup_button.place(x=260, y=150, width=100)

    def login(self):
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
                cursor.execute("SELECT * FROM admin_user WHERE user_name = %s AND user_password = %s", (username, password))
                result = cursor.fetchone()
                
                if result:
                    # Close the current window and open the admit interface
                    self.root.destroy()  # Close the login page
                    self.open_admit_interface(username)  # Pass username
                    
                else:
                    messagebox.showerror("Login Error", "Invalid Username or Password")
            except mysql.connector.Error as err:
                messagebox.showerror("Database Error", f"Error: {err}")
            finally:
                if connection.is_connected():
                    cursor.close()
                    connection.close()
        else:
            messagebox.showerror("Input Error", "Please fill in both fields")

    def open_admit_interface(self, username):
        # Create a new window for the admit interface and pass the username
        new_window = Tk()  # Create a new Tkinter instance
        admit_interface.Admit_Interface(new_window, username)  # Pass the username

    def open_signup_interface(self):
        # Create a new window for the sign-up interface
        new_window = Toplevel(self.root)
        from sign_up_page import Sign_Up_Page  # Assuming you have a separate module for the sign-up page
        Sign_Up_Page(new_window)

if __name__ == "__main__":
    root = Tk()
    obj = Login_Page(root)
    root.mainloop()
