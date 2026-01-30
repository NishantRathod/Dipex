"""
Example script for face recognition only.

This script demonstrates how to use the face recognition module.
"""

import cv2
import sys
import os

# Add src directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from face_recognition_module import FaceRecognizer


def main():
    # Initialize face recognizer
    recognizer = FaceRecognizer()
    
    # Load known faces (create this directory and add face images)
    # Each image should be named with the person's name, e.g., "john_doe.jpg"
    known_faces_dir = "known_faces"
    if os.path.exists(known_faces_dir):
        count = recognizer.load_known_faces(known_faces_dir)
        print(f"Loaded {count} known faces")
    else:
        print(f"Note: {known_faces_dir} directory not found. Create it and add face images.")
    
    # Open webcam
    cap = cv2.VideoCapture(0)
    
    if not cap.isOpened():
        print("Error: Could not open webcam")
        return
    
    print("Press 'q' to quit")
    
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        
        # Convert BGR to RGB
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        
        # Recognize faces
        results = recognizer.recognize_faces(rgb_frame)
        
        # Draw results
        output = recognizer.draw_results(frame, results)
        
        # Display
        cv2.imshow('Face Recognition', output)
        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    
    cap.release()
    cv2.destroyAllWindows()


if __name__ == '__main__':
    main()
