import cv2
import os


face_cascade_path = r'Library\haarcascade_frontalface_default.xml'


face_cascade = cv2.CascadeClassifier(face_cascade_path)


def draw_green_rectangle(image, x, y, w, h):
    cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)  


if not os.path.exists('data'):
    os.makedirs('data')


cap = cv2.VideoCapture(0)


image_count = 0

while image_count < 100:
    
    ret, frame = cap.read()
  
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    faces = face_cascade.detectMultiScale(gray, 1.3, 5)

   
    for (x, y, w, h) in faces:
        draw_green_rectangle(frame, x, y, w, h)
        face_image = frame[y:y+h, x:x+w]
        face_image_path = f'data/face_{image_count + 1}.jpg'
        cv2.imwrite(face_image_path, face_image)
        
    
        image_count += 1

  
        if image_count >= 100:
            break


    cv2.imshow('Face Detection', frame)


    if cv2.waitKey(1) & 0xFF == ord('q'):
        break


cap.release()
cv2.destroyAllWindows()

print(f"Captured {image_count} images of faces and saved to 'data' folder.")
