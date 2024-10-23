from fpdf import FPDF

class PDF(FPDF):
    def header(self):
        # Add a title at the top of the PDF
        self.set_font('Arial', 'B', 12)
        self.cell(0, 10, 'Selected Courses', 0, 1, 'C')

    def footer(self):
        # Add a page number at the bottom of the page
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.cell(0, 10, 'Page %s' % self.page_no(), 0, 0, 'C')

def print_courses_to_pdf(selected_courses):
    pdf = PDF()
    pdf.add_page()
    pdf.set_font('Arial', '', 12)
    
    # Iterate through selected courses and add them to the PDF
    for course in selected_courses:
        pdf.cell(0, 10, course, 0, 1)  # Adding each course on a new line
    
    # Save the PDF
    pdf_output = 'Selected_Courses.pdf'
    pdf.output(pdf_output)
    print(f"PDF saved as {pdf_output}")

# Assuming 'selected_courses' contains the list from the listbox
selected_courses = ['Course 1', 'Course 2', 'Course 3']  # This would be fetched from your listbox
print_courses_to_pdf(selected_courses)
