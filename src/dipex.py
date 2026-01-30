"""
Main application for Deltoid Detection & Face Recognition System

This script combines deltoid detection and face recognition functionality.
"""

import cv2
import argparse
import sys
from pathlib import Path

from face_recognition_module import FaceRecognizer
from deltoid_detection_module import DeltoidDetector


class DipexSystem:
    """
    Combined Deltoid Detection and Face Recognition System.
    """
    
    def __init__(self, known_faces_dir=None):
        """
        Initialize the Dipex system.
        
        Args:
            known_faces_dir (str): Optional directory containing known face images
        """
        self.face_recognizer = FaceRecognizer()
        self.deltoid_detector = DeltoidDetector()
        
        if known_faces_dir:
            count = self.face_recognizer.load_known_faces(known_faces_dir)
            print(f"Loaded {count} known faces")
    
    def process_image(self, image_path, output_path=None, enable_face=True, enable_deltoid=True):
        """
        Process an image with face recognition and/or deltoid detection.
        
        Args:
            image_path (str): Path to input image
            output_path (str): Optional path to save output image
            enable_face (bool): Enable face recognition
            enable_deltoid (bool): Enable deltoid detection
            
        Returns:
            numpy array: Processed image
        """
        # Read image
        image = cv2.imread(image_path)
        if image is None:
            print(f"Error: Could not read image from {image_path}")
            return None
        
        result_image = image.copy()
        
        # Face recognition
        if enable_face:
            # Convert BGR to RGB for face_recognition library
            rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            face_results = self.face_recognizer.recognize_faces(rgb_image)
            result_image = self.face_recognizer.draw_results(result_image, face_results)
            print(f"Detected {len(face_results)} face(s)")
        
        # Deltoid detection
        if enable_deltoid:
            pose_results = self.deltoid_detector.detect_pose(result_image)
            result_image = self.deltoid_detector.draw_deltoid_regions(result_image, pose_results)
            if pose_results.pose_landmarks:
                print("Deltoid regions detected")
            else:
                print("No pose detected")
        
        # Save output if path provided
        if output_path:
            cv2.imwrite(output_path, result_image)
            print(f"Saved result to {output_path}")
        
        return result_image
    
    def process_video(self, video_source=0, enable_face=True, enable_deltoid=True):
        """
        Process video stream with face recognition and/or deltoid detection.
        
        Args:
            video_source: Video source (0 for webcam, or path to video file)
            enable_face (bool): Enable face recognition
            enable_deltoid (bool): Enable deltoid detection
        """
        cap = cv2.VideoCapture(video_source)
        
        if not cap.isOpened():
            print(f"Error: Could not open video source {video_source}")
            return
        
        print("Press 'q' to quit")
        
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            
            result_frame = frame.copy()
            
            # Face recognition
            if enable_face:
                rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                face_results = self.face_recognizer.recognize_faces(rgb_frame)
                result_frame = self.face_recognizer.draw_results(result_frame, face_results)
            
            # Deltoid detection
            if enable_deltoid:
                pose_results = self.deltoid_detector.detect_pose(result_frame)
                result_frame = self.deltoid_detector.draw_deltoid_regions(result_frame, pose_results)
            
            # Display result
            cv2.imshow('Dipex - Deltoid Detection & Face Recognition', result_frame)
            
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        
        cap.release()
        cv2.destroyAllWindows()
        self.deltoid_detector.close()
    
    def close(self):
        """Release resources."""
        self.deltoid_detector.close()


def main():
    """Main entry point for the application."""
    parser = argparse.ArgumentParser(
        description='Dipex - Deltoid Detection & Face Recognition System'
    )
    parser.add_argument('--mode', choices=['image', 'video', 'webcam'],
                       default='webcam', help='Processing mode')
    parser.add_argument('--input', type=str, help='Input image or video file')
    parser.add_argument('--output', type=str, help='Output file path (for image mode)')
    parser.add_argument('--known-faces', type=str, help='Directory with known face images')
    parser.add_argument('--face', action='store_true', default=True,
                       help='Enable face recognition (default: True)')
    parser.add_argument('--no-face', action='store_false', dest='face',
                       help='Disable face recognition')
    parser.add_argument('--deltoid', action='store_true', default=True,
                       help='Enable deltoid detection (default: True)')
    parser.add_argument('--no-deltoid', action='store_false', dest='deltoid',
                       help='Disable deltoid detection')
    
    args = parser.parse_args()
    
    # Initialize system
    system = DipexSystem(known_faces_dir=args.known_faces)
    
    try:
        if args.mode == 'image':
            if not args.input:
                print("Error: --input required for image mode")
                sys.exit(1)
            
            system.process_image(
                args.input,
                args.output,
                enable_face=args.face,
                enable_deltoid=args.deltoid
            )
        
        elif args.mode == 'video':
            if not args.input:
                print("Error: --input required for video mode")
                sys.exit(1)
            
            system.process_video(
                args.input,
                enable_face=args.face,
                enable_deltoid=args.deltoid
            )
        
        else:  # webcam
            system.process_video(
                0,
                enable_face=args.face,
                enable_deltoid=args.deltoid
            )
    
    finally:
        system.close()


if __name__ == '__main__':
    main()
