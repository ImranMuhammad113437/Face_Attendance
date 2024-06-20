import tkinter as tk
from tkinter import messagebox

# Function to handle login
def login():
    username = username_entry.get()
    password = password_entry.get()
    
    # For simplicity, let's assume these are the correct credentials
    if username == "user" and password == "pass":
        messagebox.showinfo("Login", "Login Successful!")
    else:
        messagebox.showerror("Login", "Invalid username or password")

# Create the main window
root = tk.Tk()
root.title("Login Page")
root.geometry("300x200")

# Create and place the username label and entry
username_label = tk.Label(root, text="Username", font=("Arial", 12))
username_label.place (x=0,y=0)
username_entry = tk.Entry(root, font=("Arial", 12))
username_entry.pack(pady=5)

# Create and place the password label and entry
password_label = tk.Label(root, text="Password", font=("Arial", 12))
password_label.pack(pady=5)
password_entry = tk.Entry(root, show='*', font=("Arial", 12))
password_entry.pack(pady=5)

# Create and place the login button
login_button = tk.Button(root, text="Login", command=login, font=("Arial", 12))
login_button.pack(pady=20)

# Run the application
root.mainloop()
