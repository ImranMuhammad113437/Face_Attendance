def generate_emotion_report(self):
        
        student_id = self.student_id_entry.get()
        student_name = self.student_name_display.cget("text")
        selected_month = self.month_var.get()  
        selected_year = self.year_var.get()  

        
        if not student_id:
            messagebox.showwarning("Input Error", "Please enter a Student ID.")
            return  

        
        selected_courses = self.selected_courses_listbox.get(0, 'end')

        for course in selected_courses:
            
            filename = f"{student_name}_{student_id}_{course}_report.pdf"

            
            pdf = canvas.Canvas(filename, pagesize=A4)
            pdf.setTitle(f"Emotion Report for {course}")
            width, height = A4
            width, height_2 = A4

            
            pdf.setFont("Helvetica-Bold", 16)
            pdf.drawCentredString(width / 2, height - 50, "Emotion Report")
            pdf.setFont("Helvetica", 12)
            pdf.drawString(100, height - 80, f"Name: {student_name}")
            pdf.drawString(400, height - 80, f"ID: {student_id}")
            pdf.drawString(100, height - 100, f"Month: {selected_month}")
            pdf.drawString(400, height - 100, f"Year: {selected_year}")
            pdf.drawString(100, height - 120, f"Course: {course}")

            
            if self.detail_var.get():
                pdf.setFont("Helvetica-Bold", 14)
                pdf.drawString(100, height - 160, "Detailed Emotion Status:")
                height -= 180  

                
                emotion_img = self.get_emotion_status_report(student_id, student_name, selected_month, selected_year, course)

                
                if emotion_img:
                    image_path = "emotion_status.jpg"
                    pdf.drawImage(image_path, 100, height - 290, width=400, height=300)  
                    height -= 300  

            
            if self.overall_var.get():
                if self.detail_var.get():
                    pdf.setFont("Helvetica-Bold", 14)
                    pdf.drawString(100, height, "Overall Emotion Status:")
                    height -= 20

                    
                    overall_img = self.emotion_status_overall_report(student_id, student_name, selected_month, selected_year, course)

                    
                    if overall_img:
                        overall_image_path = "emotion_status_overall.jpg"
                        pdf.drawImage(overall_image_path, 100, height - 290, width=400, height=300)  
                        height -= 300  
                else:
                    pdf.setFont("Helvetica-Bold", 14)
                    pdf.drawString(100, height - 160, "Overall Emotion Status:")
                    height -= 180

                    
                    overall_img = self.emotion_status_overall_report(student_id, student_name, selected_month, selected_year, course)

                    
                    if overall_img:
                        overall_image_path = "emotion_status_overall.jpg"
                        pdf.drawImage(overall_image_path, 100, height - 290, width=400, height=300)  
                        height -= 300  

            
            if self.table_var.get():
                if self.detail_var.get() and self.overall_var.get():
                    pdf.showPage()  
                    pdf.setFont("Helvetica-Bold", 14)
                    pdf.drawString(100, height_2 - 80, "Emotion Status Table (Detailed Only):")
                    height_2 -= 20

                    
                    pdf.setFont("Helvetica", 10)
                    column_width = 60  
                    pdf.drawString(100 , height_2 - 100, "Date")
                    pdf.drawString(100 + column_width, height_2 - 100, "Neutral")
                    pdf.drawString(100 + 2 * column_width, height_2 - 100, "Happy")
                    pdf.drawString(100 + 3 * column_width, height_2 - 100, "Sad")
                    pdf.drawString(100 + 4 * column_width, height_2 - 100, "Fear")
                    pdf.drawString(100 + 5 * column_width, height_2 - 100, "Surprise")
                    pdf.drawString(100 + 6 * column_width, height_2 - 100, "Angry")
                    height_2 -= 10  

                    
                    emotion_data = self.emotion_status_table(student_id, student_name, selected_month, selected_year, course)

                    for row in emotion_data:
                        pdf.drawString(100, height_2 - 120, row[0])  
                        pdf.drawString(100 + column_width, height_2 - 120, str(row[1]))  
                        pdf.drawString(100 + 2 * column_width, height_2 - 120, str(row[2]))  
                        pdf.drawString(100 + 3 * column_width, height_2 - 120, str(row[3]))  
                        pdf.drawString(100 + 4 * column_width, height_2 - 120, str(row[4]))  
                        pdf.drawString(100 + 5 * column_width, height_2 - 120, str(row[5]))  
                        pdf.drawString(100 + 6 * column_width, height_2 - 120, str(row[6]))  
                        height_2 -= 20  

                elif (self.detail_var.get() and not self.overall_var.get()) or (not self.detail_var.get() and self.overall_var.get()):
                    pdf.setFont("Helvetica-Bold", 14)
                    pdf.drawString(100, height - 10, "Emotion Status Table (Detailed Only):")
                    height -= 20

                    
                    emotion_data = self.emotion_status_table(student_id, student_name, selected_month, selected_year, course)

                    
                    pdf.setFont("Helvetica-Bold", 10)
                    column_width = 60  
                    pdf.drawString(100, height - 10, "Date")
                    pdf.drawString(100 + column_width, height - 10, "Neutral")
                    pdf.drawString(100 + column_width * 2, height - 10, "Happy")
                    pdf.drawString(100 + column_width * 3, height - 10, "Sad")
                    pdf.drawString(100 + column_width * 4, height - 10, "Fear")
                    pdf.drawString(100 + column_width * 5, height - 10, "Surprise")
                    pdf.drawString(100 + column_width * 6, height - 10, "Angry")
                    height -= 20

                    
                    pdf.setFont("Helvetica", 10)
                    for row in emotion_data:
                        pdf.drawString(100, height - 10, row[0])  
                        pdf.drawString(100 + column_width, height - 10, str(row[1]))  
                        pdf.drawString(100 + column_width * 2, height - 10, str(row[2]))  
                        pdf.drawString(100 + column_width * 3, height - 10, str(row[3]))  
                        pdf.drawString(100 + column_width * 4, height - 10, str(row[4]))  
                        pdf.drawString(100 + column_width * 5, height - 10, str(row[5]))  
                        pdf.drawString(100 + column_width * 6, height - 10, str(row[6]))  
                        height -= 20

                

                elif not self.detail_var.get() and not self.overall_var.get():
                    pdf.setFont("Helvetica-Bold", 14)
                    pdf.drawString(100, height - 160, "Emotion Status Table (No Details or Overall):")
                    height -= 180
                    
                    
                    emotion_data = self.emotion_status_table(student_id, student_name, selected_month, selected_year, course)

                    
                    pdf.setFont("Helvetica-Bold", 10)
                    column_width = 60  
                    pdf.drawString(100, height - 10, "Date")
                    pdf.drawString(100 + column_width, height - 10, "Neutral")
                    pdf.drawString(100 + column_width * 2, height - 10, "Happy")
                    pdf.drawString(100 + column_width * 3, height - 10, "Sad")
                    pdf.drawString(100 + column_width * 4, height - 10, "Fear")
                    pdf.drawString(100 + column_width * 5, height - 10, "Surprise")
                    pdf.drawString(100 + column_width * 6, height - 10, "Angry")
                    height -= 20

                    
                    pdf.setFont("Helvetica", 10)
                    for row in emotion_data:
                        pdf.drawString(100, height - 20, row[0])  
                        pdf.drawString(100 + column_width, height - 20, str(row[1]))  
                        pdf.drawString(100 + column_width * 2, height - 20, str(row[2]))  
                        pdf.drawString(100 + column_width * 3, height - 20, str(row[3]))  
                        pdf.drawString(100 + column_width * 4, height - 20, str(row[4]))  
                        pdf.drawString(100 + column_width * 5, height - 20, str(row[5]))  
                        pdf.drawString(100 + column_width * 6, height - 20, str(row[6]))  
                        height -= 20

            
            pdf.save()

            messagebox.showinfo("Success", "PDF reports generated successfully.")