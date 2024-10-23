from tkinter import *
from tkinter import messagebox
from PIL import Image, ImageTk
import mysql.connector
import admit_interface  # Import the admit_interface module
import sign_up_page
import teacher_interface


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

        # Load eye icons
        self.eye_open_img = ImageTk.PhotoImage(Image.open("Image/view.png").resize((20, 20)))
        self.eye_closed_img = ImageTk.PhotoImage(Image.open("Image/hide.png").resize((20, 20)))

        # Password visibility toggle button
        self.toggle_password_btn = Button(self.login_frame, image=self.eye_closed_img, command=self.toggle_password, bg="white", borderwidth=0)
        self.toggle_password_btn.place(x=360, y=100)

        self.is_password_visible = False  # Track visibility state


        self.login_button = Button(self.login_frame, text="Login", command=self.login, font=("Arial", 14), bg="orange", fg="white")
        self.login_button.place(x=150, y=150, width=100)

        self.signup_button = Button(self.login_frame, text="Sign Up", command=self.open_signup_interface, font=("Arial", 14), bg="orange", fg="white")
        self.signup_button.place(x=260, y=150, width=100)


    def toggle_password(self):
        """Toggle the visibility of the password."""
        if self.is_password_visible:
            self.password_entry.config(show="*")  # Hide password
            self.toggle_password_btn.config(image=self.eye_closed_img)  # Change to closed eye icon
        else:
            self.password_entry.config(show="")  # Show password
            self.toggle_password_btn.config(image=self.eye_open_img)  # Change to open eye icon
        
        self.is_password_visible = not self.is_password_visible  # Toggle state

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

                # Check admin_user table
                cursor.execute("SELECT * FROM admin_user WHERE user_name = %s AND user_password = %s", (username, password))
                result = cursor.fetchone()

                if result:
                    # Close the current window and open the admit interface for admin
                    self.root.destroy()  # Close the login page
                    self.open_admit_interface(username)  # Pass username
                else:
                    # Check teacher_user table
                    cursor.execute("SELECT * FROM teacher_user WHERE user_name = %s AND password = %s", (username, password))
                    result = cursor.fetchone()

                    if result:
                        # Close the current window and open the admit interface for teacher
                        self.root.destroy()  # Close the login page
                        self.open_teacher_interface(username)  # You might want to define this method

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

    def open_teacher_interface(self, username):
        # Create a new window for the admit interface and pass the username
        new_window = Tk()  # Create a new Tkinter instance
        teacher_interface.Teacher_Interface(new_window, username)  # Pass the username

    def open_signup_interface(self):
        # Create a new window for the sign-up interface
        self.root.destroy()
        new_window = Tk()
        sign_up_page.Sign_Up_Page(new_window)

if __name__ == "__main__":
    root = Tk()
    root.resizable(False, False)
    obj = Login_Page(root)
    root.mainloop()
