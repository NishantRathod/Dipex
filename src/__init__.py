"""
Dipex - Deltoid Detection & Face Recognition System

This package provides modules for detecting deltoid muscles and recognizing faces.
"""

__version__ = "1.0.0"
__author__ = "Nishant Rathod"
__all__ = ["FaceRecognizer", "DeltoidDetector", "DipexSystem"]

from .face_recognition_module import FaceRecognizer
from .deltoid_detection_module import DeltoidDetector
from .dipex import DipexSystem
