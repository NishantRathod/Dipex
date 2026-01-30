"""
Basic unit tests for the Dipex system modules.

These tests verify the structure and basic functionality of the system.
"""

import unittest
import sys
import os

# Add src directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))


class TestModuleImports(unittest.TestCase):
    """Test that all modules can be imported."""
    
    def test_face_recognition_module_exists(self):
        """Test that face recognition module can be imported."""
        try:
            import face_recognition_module
        except ImportError as e:
            self.fail(f"Failed to import face_recognition_module: {e}")
    
    def test_deltoid_detection_module_exists(self):
        """Test that deltoid detection module can be imported."""
        try:
            import deltoid_detection_module
        except ImportError as e:
            self.fail(f"Failed to import deltoid_detection_module: {e}")
    
    def test_dipex_module_exists(self):
        """Test that main dipex module can be imported."""
        try:
            import dipex
        except ImportError as e:
            self.fail(f"Failed to import dipex: {e}")


class TestFaceRecognizerClass(unittest.TestCase):
    """Test FaceRecognizer class structure."""
    
    def test_face_recognizer_class_exists(self):
        """Test that FaceRecognizer class exists."""
        from face_recognition_module import FaceRecognizer
        self.assertTrue(callable(FaceRecognizer))
    
    def test_face_recognizer_has_required_methods(self):
        """Test that FaceRecognizer has required methods."""
        from face_recognition_module import FaceRecognizer
        
        required_methods = [
            'load_known_faces',
            'add_face',
            'recognize_faces',
            'draw_results'
        ]
        
        for method_name in required_methods:
            self.assertTrue(
                hasattr(FaceRecognizer, method_name),
                f"FaceRecognizer missing method: {method_name}"
            )


class TestDeltoidDetectorClass(unittest.TestCase):
    """Test DeltoidDetector class structure."""
    
    def test_deltoid_detector_class_exists(self):
        """Test that DeltoidDetector class exists."""
        from deltoid_detection_module import DeltoidDetector
        self.assertTrue(callable(DeltoidDetector))
    
    def test_deltoid_detector_has_required_methods(self):
        """Test that DeltoidDetector has required methods."""
        from deltoid_detection_module import DeltoidDetector
        
        required_methods = [
            'detect_pose',
            'get_deltoid_regions',
            'draw_deltoid_regions',
            'close'
        ]
        
        for method_name in required_methods:
            self.assertTrue(
                hasattr(DeltoidDetector, method_name),
                f"DeltoidDetector missing method: {method_name}"
            )


class TestDipexSystemClass(unittest.TestCase):
    """Test DipexSystem class structure."""
    
    def test_dipex_system_class_exists(self):
        """Test that DipexSystem class exists."""
        from dipex import DipexSystem
        self.assertTrue(callable(DipexSystem))
    
    def test_dipex_system_has_required_methods(self):
        """Test that DipexSystem has required methods."""
        from dipex import DipexSystem
        
        required_methods = [
            'process_image',
            'process_video',
            'close'
        ]
        
        for method_name in required_methods:
            self.assertTrue(
                hasattr(DipexSystem, method_name),
                f"DipexSystem missing method: {method_name}"
            )


if __name__ == '__main__':
    unittest.main()
