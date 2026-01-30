"""
Validation script to verify the Dipex system structure and configuration.

This script checks that all required files exist and have the correct structure.
"""

import os
import sys
from pathlib import Path


def check_file_exists(filepath, description):
    """Check if a file exists."""
    if os.path.exists(filepath):
        print(f"✓ {description}: {filepath}")
        return True
    else:
        print(f"✗ {description} MISSING: {filepath}")
        return False


def check_directory_exists(dirpath, description):
    """Check if a directory exists."""
    if os.path.isdir(dirpath):
        print(f"✓ {description}: {dirpath}")
        return True
    else:
        print(f"✗ {description} MISSING: {dirpath}")
        return False


def validate_module(module_path, class_name, required_methods):
    """Validate a Python module has the required class and methods."""
    try:
        # Add parent directory to path
        parent_dir = os.path.dirname(module_path)
        sys.path.insert(0, parent_dir)
        
        # Import module
        module_name = os.path.basename(module_path).replace('.py', '')
        module = __import__(module_name)
        
        # Check class exists
        if not hasattr(module, class_name):
            print(f"✗ Class {class_name} not found in {module_path}")
            return False
        
        cls = getattr(module, class_name)
        
        # Check methods
        missing_methods = []
        for method in required_methods:
            if not hasattr(cls, method):
                missing_methods.append(method)
        
        if missing_methods:
            print(f"✗ {class_name} missing methods: {', '.join(missing_methods)}")
            return False
        
        print(f"✓ Module {module_name} validated ({class_name} with {len(required_methods)} methods)")
        return True
        
    except Exception as e:
        print(f"✗ Error validating {module_path}: {e}")
        return False


def main():
    """Main validation function."""
    print("=" * 60)
    print("Dipex System Validation")
    print("=" * 60)
    print()
    
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    all_checks_passed = True
    
    # Check directories
    print("Checking directories...")
    all_checks_passed &= check_directory_exists(os.path.join(base_dir, 'src'), "Source directory")
    all_checks_passed &= check_directory_exists(os.path.join(base_dir, 'examples'), "Examples directory")
    all_checks_passed &= check_directory_exists(os.path.join(base_dir, 'tests'), "Tests directory")
    print()
    
    # Check required files
    print("Checking required files...")
    all_checks_passed &= check_file_exists(os.path.join(base_dir, 'README.md'), "README")
    all_checks_passed &= check_file_exists(os.path.join(base_dir, 'requirements.txt'), "Requirements")
    all_checks_passed &= check_file_exists(os.path.join(base_dir, '.gitignore'), "Git ignore")
    print()
    
    # Check source files
    print("Checking source files...")
    all_checks_passed &= check_file_exists(
        os.path.join(base_dir, 'src', 'face_recognition_module.py'),
        "Face recognition module"
    )
    all_checks_passed &= check_file_exists(
        os.path.join(base_dir, 'src', 'deltoid_detection_module.py'),
        "Deltoid detection module"
    )
    all_checks_passed &= check_file_exists(
        os.path.join(base_dir, 'src', 'dipex.py'),
        "Main application"
    )
    print()
    
    # Check example files
    print("Checking example files...")
    all_checks_passed &= check_file_exists(
        os.path.join(base_dir, 'examples', 'face_recognition_example.py'),
        "Face recognition example"
    )
    all_checks_passed &= check_file_exists(
        os.path.join(base_dir, 'examples', 'deltoid_detection_example.py'),
        "Deltoid detection example"
    )
    all_checks_passed &= check_file_exists(
        os.path.join(base_dir, 'examples', 'combined_example.py'),
        "Combined example"
    )
    print()
    
    # Validate modules
    print("Validating module structure...")
    all_checks_passed &= validate_module(
        os.path.join(base_dir, 'src', 'face_recognition_module.py'),
        'FaceRecognizer',
        ['load_known_faces', 'add_face', 'recognize_faces', 'draw_results']
    )
    all_checks_passed &= validate_module(
        os.path.join(base_dir, 'src', 'deltoid_detection_module.py'),
        'DeltoidDetector',
        ['detect_pose', 'get_deltoid_regions', 'draw_deltoid_regions', 'close']
    )
    all_checks_passed &= validate_module(
        os.path.join(base_dir, 'src', 'dipex.py'),
        'DipexSystem',
        ['process_image', 'process_video', 'close']
    )
    print()
    
    # Final result
    print("=" * 60)
    if all_checks_passed:
        print("✓ ALL CHECKS PASSED")
        print("The Dipex system is properly configured!")
        return 0
    else:
        print("✗ SOME CHECKS FAILED")
        print("Please review the errors above.")
        return 1


if __name__ == '__main__':
    sys.exit(main())
