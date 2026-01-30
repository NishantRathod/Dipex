# Quick Start Guide - Dipex System

## Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/NishantRathod/Dipex.git
   cd Dipex
   ```

2. **Create a virtual environment (recommended):**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

   **Note:** If you encounter issues installing `face_recognition`:
   - On Ubuntu/Debian: `sudo apt-get install build-essential cmake libopenblas-dev liblapack-dev`
   - On macOS: `brew install cmake`
   - On Windows: Install Visual Studio with C++ build tools

## Running the System

### Option 1: Quick Demo (Webcam)
```bash
cd src
python dipex.py --mode webcam
```

### Option 2: Process an Image
```bash
cd src
python dipex.py --mode image --input /path/to/image.jpg --output result.jpg
```

### Option 3: Run Examples
```bash
# Face recognition only
python examples/face_recognition_example.py

# Deltoid detection only
python examples/deltoid_detection_example.py

# Combined system
python examples/combined_example.py
```

## Adding Known Faces

To enable face recognition with known people:

1. Create a directory called `known_faces`:
   ```bash
   mkdir known_faces
   ```

2. Add face images (one face per image):
   - Name format: `person_name.jpg`
   - Example: `john_doe.jpg`, `jane_smith.jpg`

3. Run with known faces:
   ```bash
   cd src
   python dipex.py --mode webcam --known-faces ../known_faces
   ```

## Command Line Options

```bash
python dipex.py [OPTIONS]

Options:
  --mode {image,video,webcam}   Processing mode (default: webcam)
  --input PATH                  Input file (required for image/video modes)
  --output PATH                 Output file (for image mode)
  --known-faces DIR             Directory with known face images
  --face / --no-face           Enable/disable face recognition
  --deltoid / --no-deltoid     Enable/disable deltoid detection
```

## Examples

### 1. Deltoid detection only on webcam:
```bash
python src/dipex.py --mode webcam --no-face
```

### 2. Face recognition only on image:
```bash
python src/dipex.py --mode image --input photo.jpg --output result.jpg --no-deltoid
```

### 3. Full system with known faces:
```bash
python src/dipex.py --mode webcam --known-faces known_faces
```

## Validation

To verify your installation:
```bash
python tests/static_validation.py
```

## Troubleshooting

**Issue:** Webcam not working
- Solution: Check camera permissions and ensure no other app is using it

**Issue:** No pose detected
- Solution: Ensure shoulders are visible in frame, improve lighting

**Issue:** Poor face recognition
- Solution: Use clear, well-lit face images in `known_faces` directory

## Controls

- **Press 'q'** to quit the application when running in webcam/video mode

## Performance Tips

- Use `--no-face` or `--no-deltoid` to disable features you don't need
- Ensure good lighting for better detection
- Keep face and shoulders clearly visible in frame
- For slower systems, process every Nth frame

## Support

For issues or questions:
- Open an issue on GitHub: https://github.com/NishantRathod/Dipex/issues
- Check the full README.md for detailed documentation
