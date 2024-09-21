from tkinter import *
from PIL import Image
import os
import numpy as np
import cv2

class Data_Training:
    def __init__(self, root):
        self.root = root
        self.root.geometry("400x200")
        self.root.title("AttendNow")
        
        # Call the training function when the application starts
        self.train_classifier()

    # Function for training the classifier
    def train_classifier(self):
        data_directory = 'data'
        path = [os.path.join(data_directory, f) for f in os.listdir(data_directory)]
        faces = []
        ids = []

        for image in path:
            # Load the image and convert it to grayscale
            img = Image.open(image).convert('L')
            img_numpy = np.array(img, 'uint8')

            # Extract the ID from the filename
            try:
                id = int(os.path.split(image)[1].split('.')[1])
            except (IndexError, ValueError) as e:
                print(f"Error processing file {image}: {e}")
                continue

            faces.append(img_numpy)
            ids.append(id)
            cv2.imshow("Training", img_numpy)
            cv2.waitKey(1) == 13

        ids = np.array(ids)

        # Train the classifier
        clf = cv2.face.LBPHFaceRecognizer_create()
        clf.train(faces, ids)
        clf.write('classifier.xml')
        cv2.destroyAllWindows()

if __name__ == "__main__":
    root = Tk()
    obj = Data_Training(root)
    root.mainloop()
