"""
Example script for deltoid detection only.

This script demonstrates how to use the deltoid detection module.
"""

import cv2
import sys
import os

# Add src directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from deltoid_detection_module import DeltoidDetector


def main():
    # Initialize deltoid detector
    detector = DeltoidDetector()
    
    # Open webcam
    cap = cv2.VideoCapture(0)
    
    if not cap.isOpened():
        print("Error: Could not open webcam")
        return
    
    print("Press 'q' to quit")
    print("Position yourself so your shoulders are visible in the frame")
    
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        
        # Detect pose
        pose_results = detector.detect_pose(frame)
        
        # Draw deltoid regions
        output = detector.draw_deltoid_regions(frame, pose_results)
        
        # Display
        cv2.imshow('Deltoid Detection', output)
        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    
    cap.release()
    cv2.destroyAllWindows()
    detector.close()


if __name__ == '__main__':
    main()
