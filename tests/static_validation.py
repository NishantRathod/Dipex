"""
Static validation script that checks file structure without importing dependencies.

This script validates the Dipex system can be properly set up.
"""

import os
import ast
from pathlib import Path


def check_file_exists(filepath, description):
    """Check if a file exists."""
    if os.path.exists(filepath):
        print(f"✓ {description}: {filepath}")
        return True
    else:
        print(f"✗ {description} MISSING: {filepath}")
        return False


def check_python_syntax(filepath):
    """Check if a Python file has valid syntax."""
    try:
        with open(filepath, 'r') as f:
            ast.parse(f.read())
        return True
    except SyntaxError as e:
        print(f"✗ Syntax error in {filepath}: {e}")
        return False


def check_class_in_file(filepath, class_name):
    """Check if a class exists in a Python file."""
    try:
        with open(filepath, 'r') as f:
            tree = ast.parse(f.read())
        
        for node in ast.walk(tree):
            if isinstance(node, ast.ClassDef) and node.name == class_name:
                return True
        return False
    except Exception as e:
        print(f"✗ Error checking class in {filepath}: {e}")
        return False


def main():
    """Main validation function."""
    print("=" * 60)
    print("Dipex System Static Validation")
    print("=" * 60)
    print()
    
    base_dir = Path(__file__).parent.parent
    all_checks = []
    
    # Check directories
    print("Checking directories...")
    all_checks.append(check_file_exists(base_dir / 'src', "Source directory"))
    all_checks.append(check_file_exists(base_dir / 'examples', "Examples directory"))
    all_checks.append(check_file_exists(base_dir / 'tests', "Tests directory"))
    print()
    
    # Check required files
    print("Checking required files...")
    all_checks.append(check_file_exists(base_dir / 'README.md', "README"))
    all_checks.append(check_file_exists(base_dir / 'requirements.txt', "Requirements"))
    all_checks.append(check_file_exists(base_dir / '.gitignore', "Git ignore"))
    print()
    
    # Check source files
    print("Checking source files...")
    face_module = base_dir / 'src' / 'face_recognition_module.py'
    deltoid_module = base_dir / 'src' / 'deltoid_detection_module.py'
    dipex_module = base_dir / 'src' / 'dipex.py'
    
    all_checks.append(check_file_exists(face_module, "Face recognition module"))
    all_checks.append(check_file_exists(deltoid_module, "Deltoid detection module"))
    all_checks.append(check_file_exists(dipex_module, "Main application"))
    print()
    
    # Check Python syntax
    print("Checking Python syntax...")
    if face_module.exists():
        all_checks.append(check_python_syntax(face_module))
        print(f"✓ Face recognition module syntax valid")
    if deltoid_module.exists():
        all_checks.append(check_python_syntax(deltoid_module))
        print(f"✓ Deltoid detection module syntax valid")
    if dipex_module.exists():
        all_checks.append(check_python_syntax(dipex_module))
        print(f"✓ Main application syntax valid")
    print()
    
    # Check classes exist
    print("Checking class definitions...")
    if face_module.exists():
        has_class = check_class_in_file(face_module, 'FaceRecognizer')
        all_checks.append(has_class)
        if has_class:
            print(f"✓ FaceRecognizer class found")
    
    if deltoid_module.exists():
        has_class = check_class_in_file(deltoid_module, 'DeltoidDetector')
        all_checks.append(has_class)
        if has_class:
            print(f"✓ DeltoidDetector class found")
    
    if dipex_module.exists():
        has_class = check_class_in_file(dipex_module, 'DipexSystem')
        all_checks.append(has_class)
        if has_class:
            print(f"✓ DipexSystem class found")
    print()
    
    # Check example files
    print("Checking example files...")
    examples = [
        'face_recognition_example.py',
        'deltoid_detection_example.py',
        'combined_example.py'
    ]
    for example in examples:
        example_path = base_dir / 'examples' / example
        all_checks.append(check_file_exists(example_path, f"Example: {example}"))
        if example_path.exists():
            all_checks.append(check_python_syntax(example_path))
    print()
    
    # Final result
    print("=" * 60)
    if all(all_checks):
        print("✓ ALL CHECKS PASSED")
        print()
        print("The Dipex system structure is valid!")
        print()
        print("Next steps:")
        print("1. Install dependencies: pip install -r requirements.txt")
        print("2. Run an example: python examples/combined_example.py")
        print("3. Or use the main app: python src/dipex.py --mode webcam")
        return 0
    else:
        print("✗ SOME CHECKS FAILED")
        print("Please review the errors above.")
        return 1


if __name__ == '__main__':
    import sys
    sys.exit(main())
