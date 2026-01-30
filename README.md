# Dipex - Deltoid Detection & Face Recognition

A computer vision project that includes deltoid muscle detection and face recognition capabilities.

## Features

- **Deltoid Detection**: Real-time detection and visualization of deltoid muscles using MediaPipe pose estimation
- **Face Recognition**: Face detection and recognition system with dataset support

## Project Structure

```
Dipex/
├── deltoid/
│   ├── deltoid_detector.py      # Deltoid muscle detection
│   └── pose_landmarker_lite.task # MediaPipe pose model
└── face_recognition/
    ├── face_reco.py              # Face recognition implementation
    └── dataset/                  # Training dataset
        └── nishant/              # Sample user dataset
```

## Requirements

- Python 3.x
- OpenCV
- MediaPipe
- NumPy

## Installation

1. Clone the repository:
```bash
git clone <your-repo-url>
cd Dipex
```

2. Create a virtual environment:
```bash
python -m venv .venv
.venv\Scripts\Activate.ps1  # On Windows
```

3. Install dependencies:
```bash
pip install opencv-python mediapipe numpy
```

## Usage

### Deltoid Detection
```bash
python deltoid/deltoid_detector.py
```
Press 'q' to quit the application.

### Face Recognition
```bash
python face_recognition/face_reco.py
```

## Notes

- The deltoid detector uses MediaPipe's pose estimation to identify shoulder and elbow landmarks
- Deltoid regions are approximated as rectangles between the shoulder and upper arm
- Face recognition module uses a dataset-based approach for training and recognition

## License

MIT License
