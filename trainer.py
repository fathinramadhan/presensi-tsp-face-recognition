import cv2
import os
import numpy as np
from PIL import Image

recognizer = cv2.face.LBPHFaceRecognizer_create()

dataset_path = "dataset"
trainer_path = "trainer/trainer.yml"

faces = []
ids = []

def get_images_and_labels(path):
    image_paths = []

    for root, dirs, files in os.walk(path):
        for file in files:
            if file.endswith(".jpg"):
                image_paths.append(os.path.join(root, file))

    face_samples = []
    ids = []

    for image_path in image_paths:

        img = Image.open(image_path).convert("L")
        img_numpy = np.array(img, "uint8")

        filename = os.path.basename(image_path)

        id = int(filename.split(".")[1])

        face_samples.append(img_numpy)
        ids.append(id)

    return face_samples, ids

def train_model():

    print("MASUK KE TRAIN MODEL")

    recognizer = cv2.face.LBPHFaceRecognizer_create()

    faces, ids = get_images_and_labels(dataset_path)

    if len(faces) == 0:
        return False, "Dataset kosong"


    recognizer.train(
        faces,
        np.array(ids)
    )

    print("TRAINING SELESAI")


    if not os.path.exists("trainer"):
        os.makedirs("trainer")


    recognizer.write(trainer_path)


    jumlah = len(np.unique(ids))


    return True, jumlah