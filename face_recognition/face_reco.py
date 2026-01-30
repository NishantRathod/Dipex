import cv2
import numpy as np
import os

# Config
DATASET_DIR = "dataset"  # Folder with subfolders: dataset/person1, dataset/person2, etc.
CONF_THRESHOLD = 70
HAAR = cv2.data.haarcascades + "haarcascade_frontalface_default.xml"

# Load face detector
face_cascade = cv2.CascadeClassifier(HAAR)

# Create LBPH recognizer
recognizer = cv2.face.LBPHFaceRecognizer_create()

# Prepare training data
faces = []
labels = []
label_names = {}
current_label = 0

for person_name in os.listdir(DATASET_DIR):
    person_folder = os.path.join(DATASET_DIR, person_name)
    if not os.path.isdir(person_folder):
        continue

    label_names[current_label] = person_name  # Map label to name

    for filename in os.listdir(person_folder):
        img_path = os.path.join(person_folder, filename)
        img = cv2.imread(img_path)
        if img is None:
            continue

        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        detected_faces = face_cascade.detectMultiScale(gray, 1.3, 5)
        for (x, y, w, h) in detected_faces:
            face_roi = gray[y:y+h, x:x+w]
            faces.append(face_roi)
            labels.append(current_label)

    current_label += 1

if len(faces) == 0:
    print("[ERROR] No faces found in dataset!")
    exit()

recognizer.train(faces, np.array(labels))
print(f"[INFO] Training done. Recognizing {len(label_names)} people...")

# Webcam loop
cap = cv2.VideoCapture(0)
if not cap.isOpened():
    print("[ERROR] Could not open webcam.")
    exit()

while True:
    ret, frame = cap.read()
    if not ret:
        break

    gray_live = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces_live = face_cascade.detectMultiScale(gray_live, 1.3, 5)

    for (x, y, w, h) in faces_live:
        roi_live = gray_live[y:y+h, x:x+w]
        id_, conf = recognizer.predict(roi_live)

        if conf < CONF_THRESHOLD:
            name = label_names[id_]
            label = f"{name} ({int(conf)})"
            color = (0, 255, 0)
        else:
            label = f"Unknown ({int(conf)})"
            color = (0, 0, 255)

        cv2.rectangle(frame, (x, y), (x+w, y+h), color, 2)
        cv2.putText(frame, label, (x, y-10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, color, 2)

    cv2.imshow("Multiple Face Recognition", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
