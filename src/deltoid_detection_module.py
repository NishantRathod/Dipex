"""
Deltoid Detection Module

This module provides functionality for detecting deltoid muscles (shoulders) using MediaPipe pose detection.
"""

import cv2
import mediapipe as mp
import numpy as np


class DeltoidDetector:
    """
    A class for detecting deltoid muscles in images and video streams.
    
    Uses MediaPipe pose detection to identify shoulder landmarks and highlight deltoid regions.
    """
    
    def __init__(self, min_detection_confidence=0.5, min_tracking_confidence=0.5):
        """
        Initialize the DeltoidDetector.
        
        Args:
            min_detection_confidence (float): Minimum confidence for pose detection
            min_tracking_confidence (float): Minimum confidence for pose tracking
        """
        self.mp_pose = mp.solutions.pose
        self.mp_drawing = mp.solutions.drawing_utils
        self.mp_drawing_styles = mp.solutions.drawing_styles
        
        self.pose = self.mp_pose.Pose(
            min_detection_confidence=min_detection_confidence,
            min_tracking_confidence=min_tracking_confidence
        )
        
        # Deltoid region landmarks (shoulders and nearby points)
        self.left_deltoid_landmarks = [
            self.mp_pose.PoseLandmark.LEFT_SHOULDER,
            self.mp_pose.PoseLandmark.LEFT_ELBOW,
        ]
        self.right_deltoid_landmarks = [
            self.mp_pose.PoseLandmark.RIGHT_SHOULDER,
            self.mp_pose.PoseLandmark.RIGHT_ELBOW,
        ]
    
    def detect_pose(self, image):
        """
        Detect pose landmarks in an image.
        
        Args:
            image: Image array (numpy array) in BGR format
            
        Returns:
            pose_results: MediaPipe pose detection results
        """
        # Convert BGR to RGB
        image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        
        # Process the image
        results = self.pose.process(image_rgb)
        
        return results
    
    def get_deltoid_regions(self, image, pose_results):
        """
        Extract deltoid region information from pose results.
        
        Args:
            image: Image array (numpy array)
            pose_results: MediaPipe pose detection results
            
        Returns:
            dict: Dictionary containing left and right deltoid information
        """
        if not pose_results.pose_landmarks:
            return None
        
        h, w, _ = image.shape
        landmarks = pose_results.pose_landmarks.landmark
        
        deltoid_info = {
            'left': None,
            'right': None
        }
        
        # Get left deltoid region
        left_shoulder = landmarks[self.mp_pose.PoseLandmark.LEFT_SHOULDER.value]
        left_elbow = landmarks[self.mp_pose.PoseLandmark.LEFT_ELBOW.value]
        
        # Visibility threshold of 0.5 means we need at least 50% confidence in landmark detection
        if left_shoulder.visibility > 0.5 and left_elbow.visibility > 0.5:
            deltoid_info['left'] = {
                'shoulder': (int(left_shoulder.x * w), int(left_shoulder.y * h)),
                'elbow': (int(left_elbow.x * w), int(left_elbow.y * h)),
                'visibility': (left_shoulder.visibility + left_elbow.visibility) / 2
            }
        
        # Get right deltoid region
        right_shoulder = landmarks[self.mp_pose.PoseLandmark.RIGHT_SHOULDER.value]
        right_elbow = landmarks[self.mp_pose.PoseLandmark.RIGHT_ELBOW.value]
        
        # Visibility threshold of 0.5 means we need at least 50% confidence in landmark detection
        if right_shoulder.visibility > 0.5 and right_elbow.visibility > 0.5:
            deltoid_info['right'] = {
                'shoulder': (int(right_shoulder.x * w), int(right_shoulder.y * h)),
                'elbow': (int(right_elbow.x * w), int(right_elbow.y * h)),
                'visibility': (right_shoulder.visibility + right_elbow.visibility) / 2
            }
        
        return deltoid_info
    
    def draw_deltoid_regions(self, image, pose_results):
        """
        Draw deltoid regions on the image.
        
        Args:
            image: Image array (numpy array) in BGR format
            pose_results: MediaPipe pose detection results
            
        Returns:
            numpy array: Image with drawn deltoid regions
        """
        if not pose_results.pose_landmarks:
            return image
        
        image_copy = image.copy()
        
        # Draw pose landmarks
        self.mp_drawing.draw_landmarks(
            image_copy,
            pose_results.pose_landmarks,
            self.mp_pose.POSE_CONNECTIONS,
            landmark_drawing_spec=self.mp_drawing_styles.get_default_pose_landmarks_style()
        )
        
        # Get deltoid regions
        deltoid_info = self.get_deltoid_regions(image, pose_results)
        
        if deltoid_info:
            # Highlight left deltoid
            if deltoid_info['left']:
                shoulder_pos = deltoid_info['left']['shoulder']
                elbow_pos = deltoid_info['left']['elbow']
                
                # Calculate deltoid region (approximate circular region)
                center_x = shoulder_pos[0]
                center_y = shoulder_pos[1]
                radius = int(abs(shoulder_pos[1] - elbow_pos[1]) * 0.3)
                
                # Draw circular region for left deltoid
                cv2.circle(image_copy, (center_x, center_y), radius, (255, 0, 0), 3)
                # Label positioning: 40 pixels left of center, 10 pixels above the circle
                cv2.putText(image_copy, "L.Deltoid", (center_x - 40, center_y - radius - 10),
                           cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 0, 0), 2)
            
            # Highlight right deltoid
            if deltoid_info['right']:
                shoulder_pos = deltoid_info['right']['shoulder']
                elbow_pos = deltoid_info['right']['elbow']
                
                # Calculate deltoid region (approximate circular region)
                center_x = shoulder_pos[0]
                center_y = shoulder_pos[1]
                radius = int(abs(shoulder_pos[1] - elbow_pos[1]) * 0.3)
                
                # Draw circular region for right deltoid
                cv2.circle(image_copy, (center_x, center_y), radius, (255, 0, 0), 3)
                # Label positioning: 40 pixels left of center, 10 pixels above the circle
                cv2.putText(image_copy, "R.Deltoid", (center_x - 40, center_y - radius - 10),
                           cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 0, 0), 2)
        
        return image_copy
    
    def close(self):
        """Release resources."""
        self.pose.close()
