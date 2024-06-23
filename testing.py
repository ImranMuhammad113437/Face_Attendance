import tkinter as tk

def round_rectangle(canvas, x1, y1, x2, y2, radius=25, **kwargs):
    points = [x1 + radius, y1,
              x1 + radius, y1,
              x2 - radius, y1,
              x2 - radius, y1,
              x2, y1,
              x2, y1 + radius,
              x2, y1 + radius,
              x2, y2 - radius,
              x2, y2 - radius,
              x2, y2,
              x2 - radius, y2,
              x2 - radius, y2,
              x1 + radius, y2,
              x1 + radius, y2,
              x1, y2,
              x1, y2 - radius,
              x1, y2 - radius,
              x1, y1 + radius,
              x1, y1 + radius,
              x1, y1]
    return canvas.create_polygon(points, **kwargs, smooth=True)

# Create the main window
root = tk.Tk()
root.geometry("300x200")

# Create a Canvas widget
canvas = tk.Canvas(root, width=300, height=200)
canvas.pack()

# Draw a rounded rectangle
round_rectangle(canvas, 50, 50, 250, 150, radius=20, fill="blue", outline="black")

# Start the Tkinter main loop
root.mainloop()

