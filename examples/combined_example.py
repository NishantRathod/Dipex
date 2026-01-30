"""
Example script showing combined deltoid detection and face recognition.

This script demonstrates how to use both modules together.
"""

import cv2
import sys
import os

# Add src directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from dipex import DipexSystem


def main():
    # Initialize the combined system
    # Optionally provide path to known faces directory
    system = DipexSystem(known_faces_dir="known_faces")
    
    print("Starting Dipex System...")
    print("Press 'q' to quit")
    print("Position yourself so your face and shoulders are visible")
    
    # Process webcam feed
    system.process_video(
        video_source=0,
        enable_face=True,
        enable_deltoid=True
    )


if __name__ == '__main__':
    main()
