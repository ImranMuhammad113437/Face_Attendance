from PIL import Image
import os
import numpy as np
import cv2

class Data_Training:
    def __init__(self):
        
        self.train_classifier()

    
    def train_classifier(self):
        data_directory = 'data'
        path = [os.path.join(data_directory, f) for f in os.listdir(data_directory)]
        faces = []
        ids = []

        for image in path:
            
            img = Image.open(image).convert('L')
            img_numpy = np.array(img, 'uint8')

            
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

        
        clf = cv2.face.LBPHFaceRecognizer_create()
        clf.train(faces, ids)
        clf.write('classifier.xml')
        cv2.destroyAllWindows()

if __name__ == "__main__":
    obj = Data_Training()
