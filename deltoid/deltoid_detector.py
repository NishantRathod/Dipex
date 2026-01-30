import cv2
import numpy as np
import mediapipe as mp

# MediaPipe Pose setup (classic API)
mp_pose = mp.solutions.pose
pose = mp_pose.Pose(
    static_image_mode=False,
    model_complexity=1,
    smooth_landmarks=True,
    enable_segmentation=False,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5
)

# Landmark indices
LEFT_SHOULDER = mp_pose.PoseLandmark.LEFT_SHOULDER.value
RIGHT_SHOULDER = mp_pose.PoseLandmark.RIGHT_SHOULDER.value
LEFT_ELBOW = mp_pose.PoseLandmark.LEFT_ELBOW.value
RIGHT_ELBOW = mp_pose.PoseLandmark.RIGHT_ELBOW.value

# Webcam
cap = cv2.VideoCapture(0)

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.flip(frame, 1)
    h, w, _ = frame.shape

    # Convert to RGB
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = pose.process(rgb_frame)

    if results.pose_landmarks:
        landmarks = results.pose_landmarks.landmark

        left_shoulder = (
            int(landmarks[LEFT_SHOULDER].x * w),
            int(landmarks[LEFT_SHOULDER].y * h)
        )
        left_elbow = (
            int(landmarks[LEFT_ELBOW].x * w),
            int(landmarks[LEFT_ELBOW].y * h)
        )

        right_shoulder = (
            int(landmarks[RIGHT_SHOULDER].x * w),
            int(landmarks[RIGHT_SHOULDER].y * h)
        )
        right_elbow = (
            int(landmarks[RIGHT_ELBOW].x * w),
            int(landmarks[RIGHT_ELBOW].y * h)
        )

        def draw_deltoid_box(frame, shoulder, elbow, color):
            box_height = int(abs(elbow[1] - shoulder[1]) / 3)
            box_width = int(abs(elbow[0] - shoulder[0]) * 1.4)

            top_left = (
                shoulder[0] - box_width // 2,
                shoulder[1]
            )
            bottom_right = (
                shoulder[0] + box_width // 2,
                shoulder[1] + box_height
            )

            cv2.rectangle(frame, top_left, bottom_right, color, 2)
            cv2.putText(
                frame, "Deltoid",
                (top_left[0], top_left[1] - 10),
                cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2
            )

        draw_deltoid_box(frame, left_shoulder, left_elbow, (0, 255, 0))
        draw_deltoid_box(frame, right_shoulder, right_elbow, (255, 0, 0))

        # Draw pose landmarks
        for lm in landmarks:
            x, y = int(lm.x * w), int(lm.y * h)
            cv2.circle(frame, (x, y), 3, (0, 255, 255), -1)

    cv2.imshow("Deltoid Detector (No .task)", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
