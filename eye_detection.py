import cv2
import time

# Load the pre-trained Haar Cascade classifiers for face and eyes
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
eye_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_eye.xml')

# Initialize the webcam
cap = cv2.VideoCapture(0)

# Variables to track eye closure time
eyes_closed_start_time = None
eyes_closed_duration_threshold = 10  # 10 seconds threshold

while True:
    # Capture frame-by-frame from the webcam
    ret, frame = cap.read()
    if not ret:
        break  # If no frame is captured, exit

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)  # Convert frame to grayscale for faster processing

    # Detect faces in the frame
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)

    for (x, y, w, h) in faces:
        # Draw a rectangle around the face
        cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)

        # Focus on the face region for detecting eyes
        face_region_gray = gray[y:y + h, x:x + w]
        face_region_color = frame[y:y + h, x:x + w]

        # Detect eyes within the face region
        eyes = eye_cascade.detectMultiScale(face_region_gray, 1.3, 5)

        if len(eyes) == 0:
            # Eyes closed
            if eyes_closed_start_time is None:
                # Start the timer when eyes are first detected closed
                eyes_closed_start_time = time.time()

            # Calculate how long eyes have been closed
            eyes_closed_duration = time.time() - eyes_closed_start_time

            if eyes_closed_duration >= eyes_closed_duration_threshold:
                # If eyes closed for more than 10 seconds, mark as asleep/not paying attention
                cv2.putText(frame, "Asleep/Not Paying Attention", (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
            else:
                # Still counting, display a warning
                cv2.putText(frame, f"Eyes closed for {int(eyes_closed_duration)} sec", (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2)

        else:
            # Eyes are open -> Awake
            cv2.putText(frame, "Awake", (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            # Reset the eyes closed timer
            eyes_closed_start_time = None

        # Draw rectangles around detected eyes
        for (ex, ey, ew, eh) in eyes:
            cv2.rectangle(face_region_color, (ex, ey), (ex + ew, ey + eh), (0, 255, 0), 2)

    # Display the frame
    cv2.imshow('Eye State Detector', frame)

    # Press 'q' to quit the video feed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the capture and close windows
cap.release()
cv2.destroyAllWindows()
