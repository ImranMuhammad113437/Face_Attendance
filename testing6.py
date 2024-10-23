from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch

def generate_attendance_pdf(student_name, student_id, attendance_data):
    pdf_file_path = f"{student_name}_attendance_report.pdf"
    c = canvas.Canvas(pdf_file_path, pagesize=A4)
    width, height = A4

    # Title
    title_text = "Attendance Status"
    c.setFont("Times-Roman", 18)
    title_width = c.stringWidth(title_text, "Times-Roman", 18)
    c.drawString((width - title_width) / 2, height - 50, title_text)

    # Student Info
    c.setFont("Times-Roman", 12)
    c.drawString(100, height - 80, f"Name: {student_name} | ID: {student_id}")
    c.drawString(100, height - 100, f"Month: October | Year: 2024")

    # Table Headers
    headers = ["Date", "Hour", "Status"]
    left_margin = 0.5 * inch
    column_width = 2 * inch
    table_start_y = height - 150

    c.setFont("Helvetica-Bold", 12)
    for col_index, header in enumerate(headers):
        header_x = left_margin + col_index * column_width
        c.drawString(header_x, table_start_y, header)

    # Table Rows
    row_height = 0.4 * inch
    c.setFont("Helvetica", 10)
    for data_index, data in enumerate(attendance_data):
        data_y = table_start_y - ((data_index + 1) * row_height)
        for col_index, value in enumerate(data):
            data_x = left_margin + col_index * column_width
            c.drawString(data_x, data_y, str(value))

    c.save()
    print(f"PDF generated at: {pdf_file_path}")

# Sample data
attendance_data = [
    ["2024-10-01", "08:00 - 09:00", "P"],
    ["2024-10-02", "08:00 - 09:00", "P"],
    ["2024-10-03", "08:00 - 09:00", "P"],
    ["2024-10-04", "08:00 - 09:00", "P"],
    ["2024-10-05", "08:00 - 09:00", "P"],
    ["2024-10-06", "08:00 - 09:00", "P"],
    ["2024-10-07", "08:00 - 09:00", "P"],
    ["2024-10-08", "08:00 - 09:00", "P"],
    ["2024-10-09", "08:00 - 09:00", "P"],
    ["2024-10-10", "08:00 - 09:00", "P"],
    ["2024-10-11", "08:00 - 09:00", "P"],
    ["2024-10-12", "08:00 - 09:00", "P"],
    ["2024-10-13", "08:00 - 09:00", "P"],
    ["2024-10-14", "08:00 - 09:00", "P"],
    ["2024-10-15", "08:00 - 09:00", "P"],
    ["2024-10-16", "08:00 - 09:00", "P"],
    ["2024-10-17", "09:00 - 10:00", "P"]
]

# Call the function to generate PDF
generate_attendance_pdf("John Doe", "123456", attendance_data)
