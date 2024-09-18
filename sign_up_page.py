from tkinter import *
from tkinter import messagebox
from PIL import Image, ImageTk
import admit_interface  # Import the admit_interface module

class Sign_Up_Page:
    def __init__(self, root):
        self.root = root
        self.root.geometry("1024x590+0+0")
        self.root.title("AttendNow")

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
            # Here, you can implement saving user credentials or further processing
            messagebox.showinfo("Sign Up Success", "Account Created Successfully!")
            # Open the admit interface window after sign up
            self.open_admit_interface()
        else:
            messagebox.showerror("Sign Up Error", "Please fill in all fields")

    def open_admit_interface(self):
        # Create a new window for the admit interface
        new_window = Toplevel(self.root)
        admit_interface.Admit_Interface(new_window)

if __name__ == "__main__":
    root = Tk()
    obj = Sign_Up_Page(root)
    root.mainloop()
