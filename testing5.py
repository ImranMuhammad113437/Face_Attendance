import tkinter as tk
from tkinter import messagebox
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import fitz  # PyMuPDF
import os
from PIL import Image, ImageTk

def create_pdf():
    # Create a PDF file
    pdf_filename = "report.pdf"
    c = canvas.Canvas(pdf_filename, pagesize=letter)
    c.drawString(100, 750, "This is a sample PDF document.")
    c.drawString(100, 735, "You can preview it before downloading.")
    c.save()
    return pdf_filename

def show_preview():
    pdf_file = create_pdf()
    
    # Create a new top-level window for preview
    preview_window = tk.Toplevel(root)
    preview_window.title("PDF Preview")

    # Open the PDF with PyMuPDF
    pdf_document = fitz.open(pdf_file)
    first_page = pdf_document[0]
    
    # Render the first page to an image
    pix = first_page.get_pixmap()
    img_path = "preview_image.png"
    pix.save(img_path)

    # Load the image and display it in Tkinter
    img = Image.open(img_path)
    img.thumbnail((400, 600))  # Resize the image to fit
    photo = ImageTk.PhotoImage(img)

    label = tk.Label(preview_window, image=photo)
    label.image = photo  # Keep a reference to avoid garbage collection
    label.pack(fill="both", expand=True)

    # Add a download button
    download_button = tk.Button(preview_window, text="Download PDF", command=lambda: download_pdf(pdf_file))
    download_button.pack(pady=10)

def download_pdf(pdf_file):
    # Trigger file download
    os.startfile(pdf_file)
    messagebox.showinfo("Download", "PDF has been downloaded.")

# Main Tkinter window
root = tk.Tk()
root.title("PDF Document Preview")

# Create a button to generate and preview the PDF
preview_button = tk.Button(root, text="Generate and Preview PDF", command=show_preview)
preview_button.pack(pady=20)

root.mainloop()
