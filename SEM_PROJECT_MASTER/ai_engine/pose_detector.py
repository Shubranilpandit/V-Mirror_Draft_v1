import cv2 # OpenCV for image processing
import mediapipe as mp # MediaPipe for pose detection
from mediapipe.tasks import python # BaseOptions for model configuration
from mediapipe.tasks.python import vision # Vision tasks for pose detection
import urllib.request # For downloading the model if it doesn't exist 
import os # For handling file paths

class PoseDetector:
    def __init__(self, min_detection_confidence=0.5, min_tracking_confidence=0.5):
        model_path = os.path.join(os.path.dirname(__file__), 'pose_landmarker.task')
        if not os.path.exists(model_path):
            url = 'https://storage.googleapis.com/mediapipe-models/pose_landmarker/pose_landmarker_lite/float16/1/pose_landmarker_lite.task'
            urllib.request.urlretrieve(url, model_path)
        base_options = python.BaseOptions(model_asset_path=model_path)
        options = vision.PoseLandmarkerOptions(
            base_options=base_options,
            running_mode=vision.RunningMode.IMAGE,
            min_pose_detection_confidence=min_detection_confidence,
            min_pose_presence_confidence=min_tracking_confidence,
            min_tracking_confidence=min_tracking_confidence,
        )
        self.landmarker = vision.PoseLandmarker.create_from_options(options)

    def detect(self, frame):
        mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
        result = self.landmarker.detect(mp_image)
        height, width = frame.shape[:2]
        pose_data = {}

        if not result.pose_landmarks:
            return pose_data

        landmarks = result.pose_landmarks[0]
        def _coord(index):
            landmark = landmarks[index]
            return int(landmark.x * width), int(landmark.y * height)

        pose_data['nose'] = _coord(0)  # NOSE
        pose_data['left_shoulder'] = _coord(11)  # LEFT_SHOULDER
        pose_data['right_shoulder'] = _coord(12)  # RIGHT_SHOULDER
        pose_data['left_hip'] = _coord(23)  # LEFT_HIP
        pose_data['right_hip'] = _coord(24)  # RIGHT_HIP
        return pose_data
