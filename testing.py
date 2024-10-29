from fer import FER  # Import FER for emotion detection

def face_recog(self):
    # No need for course validation

    # Load the face detection classifier
    faceCascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

    # Load the face recognition model
    clf = cv2.face.LBPHFaceRecognizer_create()
    clf.read("classifier.xml")

    # Initialize the emotion detector
    emotion_detector = FER()

    # Start video capture for face recognition
    self.video_cap = cv2.VideoCapture(0)
    self.recognize(faceCascade, clf, emotion_detector)

def recognize(self, faceCascade, clf, emotion_detector):
    ret, img = self.video_cap.read()
    if not ret:
        self.video_cap.release()
        return

    gray_image = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    features = faceCascade.detectMultiScale(gray_image, scaleFactor=1.1, minNeighbors=10)

    for (x, y, w, h) in features:
        cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 3)  # Draw rectangle around face
        id, predict = clf.predict(gray_image[y:y + h, x:x + w])
        confidence = int((100 * (1 - predict / 300)))

        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="Nightcore_1134372019!",
            database="attendnow"
        )
        my_cursor = conn.cursor()

        # Retrieve student name and ID based on student ID only (no course filter)
        my_cursor.execute("SELECT student_name, student_id FROM students WHERE student_id=%s", (id,))
        result = my_cursor.fetchone()
        student_name = result[0] if result else "Unknown"
        student_id = result[1] if result else "Unknown"

        conn.close()

        # Emotion detection on the cropped face
        face_img = img[y:y + h, x:x + w]
        emotions = emotion_detector.detect_emotions(face_img)

        if emotions:
            dominant_emotion = max(emotions[0]['emotions'], key=emotions[0]['emotions'].get)
        else:
            dominant_emotion = "No emotion detected"

        # Add text overlay on video frame for face recognition and emotion detection
        if confidence > 70:
            cv2.putText(img, f"Name: {student_name}", (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)
            cv2.putText(img, f"ID: {student_id}", (x, y + h + 30), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)
            cv2.putText(img, f"Emotion: {dominant_emotion}", (x, y + h + 60), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255, 0, 0), 2)
        else:
            cv2.putText(img, "Unknown", (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 0, 255), 2)

    # Convert OpenCV image to ImageTk format for Tkinter display
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    img_pil = Image.fromarray(img_rgb)
    imgtk = ImageTk.PhotoImage(image=img_pil)

    # Update video feed in the Tkinter interface
    self.video_label.imgtk = imgtk
    self.video_label.configure(image=imgtk)

    # Continuously update the video feed
    self.video_label.after(10, lambda: self.recognize(faceCascade, clf, emotion_detector))
