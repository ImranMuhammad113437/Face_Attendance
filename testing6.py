import tkinter as tk
from tkinter import messagebox, ttk
import mysql.connector
import calendar

class EmotionStatusApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Emotion Status Table")
        self.root.geometry("1000x600")  # Adjust window size as needed

        # Main Frame (Split into left and right)
        self.main_frame = tk.Frame(self.root, bd=2, bg="orange")
        self.main_frame.place(x=490, y=70, width=500, height=400)

        # Input fields and buttons
        self.selected_student_input = tk.StringVar()
        self.student_id_input = tk.StringVar()
        self.year_input = tk.StringVar()

        # Drop-down for student selection
        tk.Label(self.root, text="Student Name").place(x=50, y=50)
        tk.Entry(self.root, textvariable=self.selected_student_input).place(x=150, y=50)

        tk.Label(self.root, text="Student ID").place(x=50, y=100)
        tk.Entry(self.root, textvariable=self.student_id_input).place(x=150, y=100)

        tk.Label(self.root, text="Year").place(x=50, y=150)
        tk.Entry(self.root, textvariable=self.year_input).place(x=150, y=150)

        # Month dropdown
        self.month_var = tk.StringVar()
        self.month_dropdown = ttk.Combobox(self.root, textvariable=self.month_var, state='readonly')
        self.month_dropdown['values'] = [calendar.month_name[i] for i in range(1, 13)]
        self.month_dropdown.place(x=150, y=200)
        tk.Label(self.root, text="Month").place(x=50, y=200)

        # Button to trigger table display
        self.get_emotion_status_button = tk.Button(self.root, text="Get Emotion Status", command=self.emotion_status_table)
        self.get_emotion_status_button.place(x=150, y=250)

        # Additional buttons (disabled until emotion status is fetched)
        self.emotion_status_detail_button = tk.Button(self.root, text="Emotion Details", state="disabled")
        self.emotion_status_detail_button.place(x=50, y=300)

        self.emotion_status_overall_button = tk.Button(self.root, text="Overall Emotion", state="disabled")
        self.emotion_status_overall_button.place(x=150, y=300)

        self.emotion_status_table_button = tk.Button(self.root, text="Table", state="disabled")
        self.emotion_status_table_button.place(x=250, y=300)

    def display_selected_month(self):
        # Get the selected month as a number (1 to 12)
        return self.month_dropdown.current() + 1

    def emotion_status_table(self):
        # Clear the existing chart from the main_frame
        for widget in self.main_frame.winfo_children():
            widget.destroy()

        student_name = self.selected_student_input.get()
        student_id = self.student_id_input.get()
        month_value = self.display_selected_month()
        month_name = calendar.month_name[int(month_value)]
        selected_year = self.year_input.get()  # Get the selected year from the year dropdown

        if not student_name or not student_id:
            messagebox.showwarning("Warning", "Please select a student.")
            return

        if selected_year == "Select Year":  # Check if a valid year is selected
            messagebox.showwarning("Warning", "Please select a year.")
            return

        # Connect to the MySQL database
        connection = mysql.connector.connect(
            host="localhost",  # Replace with your host if different
            user="root",
            password="Nightcore_1134372019!",
            database="attendnow"
        )

        cursor = connection.cursor()

        # SQL query to extract emotion data by student name, ID, month, and year
        query = """
            SELECT date, neutral, happy, sad, fear, surprise, angry
            FROM student_emotion
            WHERE student_name = %s 
            AND student_id = %s 
            AND MONTH(date) = %s
            AND YEAR(date) = %s
            ORDER BY date;
        """

        cursor.execute(query, (student_name, student_id, month_value, selected_year))
        results = cursor.fetchall()

        # Close the database connection 
        connection.close()

        if not results:
            messagebox.showinfo("Info", f"No emotion data found for the selected student in {month_name}, {selected_year}.")
            return

        # Create a frame for the Treeview and scrollbars
        self.tree_frame = ttk.Frame(self.main_frame)
        self.tree_frame.pack(fill="both", expand=True)

        # Create a Treeview widget to display the table
        columns = ["Date", "Neutral", "Happy", "Sad", "Fear", "Surprise", "Angry", "Overall Emotion"]
        
        # Set the Treeview's width to fit the main_frame
        self.attendance_table = ttk.Treeview(self.tree_frame, columns=columns, show='headings')

        # Define the column headings and their widths (adjust to fit within main_frame width)
        column_widths = [80, 50, 50, 50, 50, 50, 50, 120]  # Adjust the widths as necessary
        total_width = sum(column_widths)  # Get total width of all columns

        if total_width > 500:  # Ensure it fits in the 500px width of main_frame
            scale_factor = 500 / total_width
            column_widths = [int(w * scale_factor) for w in column_widths]  # Scale down

        for column, width in zip(columns, column_widths):
            self.attendance_table.heading(column, text=column)
            self.attendance_table.column(column, anchor='center', width=width)

        # Scrollbar for the Treeview (Only Vertical)
        scroll_y = ttk.Scrollbar(self.tree_frame, orient='vertical', command=self.attendance_table.yview)

        # Configure the Treeview to only use the vertical scrollbar
        self.attendance_table.configure(yscrollcommand=scroll_y.set)

        # Inserting data into the Treeview
        for row in results:
            date_str = str(row[0])  # Assuming the date is in a datetime format
            overall_emotion = max(('Neutral', row[1]), ('Happy', row[2]), ('Sad', row[3]), 
                                ('Fear', row[4]), ('Surprise', row[5]), ('Angry', row[6]), 
                                key=lambda x: x[1])[0]  # Get the emotion with the highest value

            # Insert the row into the Treeview
            self.attendance_table.insert('', 'end', values=(date_str, row[1], row[2], row[3], row[4], row[5], row[6], overall_emotion))

        # Pack the Treeview and the vertical scrollbar
        self.attendance_table.pack(side="left", fill="both", expand=True)
        scroll_y.pack(side="right", fill="y")

        # Enable the buttons after the "Get Emotion Status" is pressed
        self.emotion_status_detail_button.config(state="normal")
        self.emotion_status_overall_button.config(state="normal")
        self.emotion_status_table_button.config(state="normal")
        self.get_emotion_status_button.config(state="disabled")


# Main application
if __name__ == "__main__":
    root = tk.Tk()
    app = EmotionStatusApp(root)
    root.mainloop()
