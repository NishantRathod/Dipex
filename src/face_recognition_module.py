"""
Face Recognition Module

This module provides functionality for detecting and recognizing faces in images and video streams.
"""

import face_recognition
import cv2
import numpy as np
import os
from pathlib import Path


class FaceRecognizer:
    """
    A class for face recognition operations.
    
    Attributes:
        known_face_encodings (list): List of face encodings for known faces
        known_face_names (list): List of names corresponding to known face encodings
    """
    
    def __init__(self):
        """Initialize the FaceRecognizer with empty lists for known faces."""
        self.known_face_encodings = []
        self.known_face_names = []
    
    def load_known_faces(self, faces_dir):
        """
        Load known faces from a directory.
        
        Args:
            faces_dir (str): Path to directory containing face images
            
        Returns:
            int: Number of faces loaded
        """
        faces_dir = Path(faces_dir)
        if not faces_dir.exists():
            print(f"Warning: Directory {faces_dir} does not exist")
            return 0
        
        count = 0
        for image_file in faces_dir.glob("*.jpg"):
            # Load image
            image = face_recognition.load_image_file(str(image_file))
            
            # Get face encodings
            encodings = face_recognition.face_encodings(image)
            
            if encodings:
                self.known_face_encodings.append(encodings[0])
                self.known_face_names.append(image_file.stem)
                count += 1
                print(f"Loaded face: {image_file.stem}")
        
        return count
    
    def add_face(self, image, name):
        """
        Add a face to the known faces list.
        
        Args:
            image: Image array (numpy array)
            name (str): Name to associate with the face
            
        Returns:
            bool: True if face was added successfully, False otherwise
        """
        encodings = face_recognition.face_encodings(image)
        
        if encodings:
            self.known_face_encodings.append(encodings[0])
            self.known_face_names.append(name)
            return True
        return False
    
    def recognize_faces(self, image):
        """
        Recognize faces in an image.
        
        Args:
            image: Image array (numpy array) in RGB format
            
        Returns:
            list: List of tuples containing (name, location) for each recognized face
                  location is (top, right, bottom, left)
        """
        # Find all face locations and encodings in the image
        face_locations = face_recognition.face_locations(image)
        face_encodings = face_recognition.face_encodings(image, face_locations)
        
        results = []
        
        for (face_encoding, face_location) in zip(face_encodings, face_locations):
            # See if the face matches any known faces
            matches = face_recognition.compare_faces(self.known_face_encodings, face_encoding)
            name = "Unknown"
            
            # Use the known face with the smallest distance
            if self.known_face_encodings:
                face_distances = face_recognition.face_distance(self.known_face_encodings, face_encoding)
                best_match_index = np.argmin(face_distances)
                
                if matches[best_match_index]:
                    name = self.known_face_names[best_match_index]
            
            results.append((name, face_location))
        
        return results
    
    def draw_results(self, image, results):
        """
        Draw bounding boxes and labels on the image.
        
        Args:
            image: Image array (numpy array) in BGR format (OpenCV format)
            results: List of tuples containing (name, location)
            
        Returns:
            numpy array: Image with drawn results
        """
        image_copy = image.copy()
        
        for (name, (top, right, bottom, left)) in results:
            # Draw rectangle around face
            cv2.rectangle(image_copy, (left, top), (right, bottom), (0, 255, 0), 2)
            
            # Draw label below face
            cv2.rectangle(image_copy, (left, bottom - 35), (right, bottom), (0, 255, 0), cv2.FILLED)
            font = cv2.FONT_HERSHEY_DUPLEX
            cv2.putText(image_copy, name, (left + 6, bottom - 6), font, 0.6, (255, 255, 255), 1)
        
        return image_copy
