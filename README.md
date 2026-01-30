# Dipex - Deltoid Detection & Face Recognition System

A comprehensive computer vision system that combines deltoid (shoulder muscle) detection with face recognition capabilities. This system uses state-of-the-art machine learning models to detect human poses, identify deltoid regions, and recognize faces in real-time.

## Features

- **Face Recognition**: Identify and recognize faces using advanced face encoding techniques
- **Deltoid Detection**: Detect and highlight deltoid muscle regions using pose estimation
- **Real-time Processing**: Process webcam feeds in real-time
- **Image/Video Support**: Process static images or video files
- **Modular Design**: Use face recognition and deltoid detection independently or together

## Installation

### Prerequisites

- Python 3.7 or higher
- pip (Python package manager)
- A webcam (optional, for real-time processing)

### Setup

1. Clone the repository:
```bash
git clone https://github.com/NishantRathod/Dipex.git
cd Dipex
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

**Note**: Installing `dlib` (required by `face_recognition`) may require additional system dependencies:

- **Ubuntu/Debian**:
  ```bash
  sudo apt-get install build-essential cmake
  sudo apt-get install libopenblas-dev liblapack-dev
  ```

- **macOS**:
  ```bash
  brew install cmake
  ```

- **Windows**: Install Visual Studio with C++ build tools

## Usage

### Quick Start

Run the combined system with webcam:
```bash
cd src
python dipex.py --mode webcam
```

### Command Line Options

```bash
python dipex.py [OPTIONS]
```

**Options:**
- `--mode`: Processing mode - `image`, `video`, or `webcam` (default: `webcam`)
- `--input`: Input image or video file path
- `--output`: Output file path (for image mode)
- `--known-faces`: Directory containing known face images
- `--face / --no-face`: Enable/disable face recognition (default: enabled)
- `--deltoid / --no-deltoid`: Enable/disable deltoid detection (default: enabled)

### Examples

#### 1. Process an image with both features:
```bash
python dipex.py --mode image --input photo.jpg --output result.jpg
```

#### 2. Process video with deltoid detection only:
```bash
python dipex.py --mode video --input video.mp4 --no-face
```

#### 3. Webcam with face recognition only:
```bash
python dipex.py --mode webcam --no-deltoid --known-faces ./known_faces
```

### Using Example Scripts

The `examples/` directory contains standalone scripts demonstrating each feature:

#### Face Recognition Only:
```bash
python examples/face_recognition_example.py
```

#### Deltoid Detection Only:
```bash
python examples/deltoid_detection_example.py
```

#### Combined System:
```bash
python examples/combined_example.py
```

## Setting Up Face Recognition

To enable face recognition with known faces:

1. Create a directory called `known_faces`:
   ```bash
   mkdir known_faces
   ```

2. Add face images to this directory:
   - Each image should contain one face
   - Name the image file with the person's name (e.g., `john_doe.jpg`)
   - Supported formats: `.jpg`, `.jpeg`, `.png`

3. Run the system with the known faces directory:
   ```bash
   python src/dipex.py --known-faces known_faces
   ```

## How It Works

### Face Recognition
- Uses the `face_recognition` library built on dlib's deep learning face recognition
- Encodes faces from known images
- Compares detected faces against known encodings
- Displays names for recognized faces

### Deltoid Detection
- Uses MediaPipe's pose estimation model
- Detects 33 body landmarks including shoulders and elbows
- Calculates deltoid regions based on shoulder positions
- Highlights left and right deltoid areas with circles

## Module Documentation

### FaceRecognizer Class
Located in `src/face_recognition_module.py`

**Key Methods:**
- `load_known_faces(faces_dir)`: Load known faces from directory
- `add_face(image, name)`: Add a single face to known faces
- `recognize_faces(image)`: Recognize faces in an image
- `draw_results(image, results)`: Draw bounding boxes and labels

### DeltoidDetector Class
Located in `src/deltoid_detection_module.py`

**Key Methods:**
- `detect_pose(image)`: Detect pose landmarks
- `get_deltoid_regions(image, pose_results)`: Extract deltoid region info
- `draw_deltoid_regions(image, pose_results)`: Draw deltoid highlights

### DipexSystem Class
Located in `src/dipex.py`

**Key Methods:**
- `process_image(image_path, output_path, ...)`: Process static image
- `process_video(video_source, ...)`: Process video or webcam stream

## Requirements

- opencv-python >= 4.8.0
- mediapipe >= 0.10.0
- face-recognition >= 1.3.0
- numpy >= 1.24.0
- Pillow >= 10.0.0

## Project Structure

```
Dipex/
├── src/
│   ├── dipex.py                      # Main application
│   ├── face_recognition_module.py    # Face recognition module
│   └── deltoid_detection_module.py   # Deltoid detection module
├── examples/
│   ├── face_recognition_example.py   # Face recognition demo
│   ├── deltoid_detection_example.py  # Deltoid detection demo
│   └── combined_example.py           # Combined system demo
├── requirements.txt                   # Python dependencies
├── .gitignore                        # Git ignore file
└── README.md                         # This file
```

## Use Cases

- **Fitness Applications**: Track deltoid muscle engagement during workouts
- **Security Systems**: Combine face recognition with body pose analysis
- **Healthcare**: Monitor shoulder mobility and posture
- **Sports Analysis**: Analyze athlete shoulder positioning and technique
- **Access Control**: Multi-factor authentication using face + pose

## Troubleshooting

### Installation Issues

**Problem**: `dlib` installation fails
- **Solution**: Install system dependencies (CMake, build tools) as mentioned in Prerequisites

**Problem**: `face_recognition` import error
- **Solution**: Ensure all dependencies are installed: `pip install --upgrade face_recognition`

### Runtime Issues

**Problem**: Webcam not detected
- **Solution**: Check webcam permissions and ensure no other application is using it

**Problem**: No faces detected
- **Solution**: Ensure proper lighting and face is clearly visible

**Problem**: No deltoids detected
- **Solution**: Ensure shoulders are visible in frame and body is well-lit

## Performance Tips

- For real-time processing, ensure good lighting conditions
- Lower the camera resolution if processing is slow
- Use `--no-face` or `--no-deltoid` to disable features you don't need
- Process every Nth frame for better performance in video mode

## Contributing

Contributions are welcome! Please feel free to submit pull requests or open issues for bugs and feature requests.

## License

This project is open source and available under the MIT License.

## Acknowledgments

- [face_recognition](https://github.com/ageitgey/face_recognition) by Adam Geitgey
- [MediaPipe](https://google.github.io/mediapipe/) by Google
- [OpenCV](https://opencv.org/) for computer vision utilities

## Contact

For questions or support, please open an issue on GitHub.