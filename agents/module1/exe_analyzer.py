import cv2
import mediapipe as mp
import numpy as np
import math
import time
import json
import os
from mediapipe.tasks import python
from mediapipe.tasks.python import vision

# -----------------------------
# Load ideal exercises
# -----------------------------
with open("ideal_exercises.json", "r") as f:
    ideal_exercises_data = json.load(f)

def calculate_angle(a, b, c):
    a = np.array(a)
    b = np.array(b)
    c = np.array(c)
    radians = math.atan2(c[1]-b[1], c[0]-b[0]) - math.atan2(a[1]-b[1], a[0]-b[0])
    angle = abs(radians * 180.0 / math.pi)
    if angle > 180.0:
        angle = 360 - angle
    return angle

def get_ideal_angles_from_coords(coords_dict):
    def get_pt(idx):
        return (coords_dict[str(idx)]["x"], coords_dict[str(idx)]["y"])
    angles = {}
    angles["left_shoulder"] = calculate_angle(get_pt(13), get_pt(11), get_pt(23))
    angles["right_shoulder"] = calculate_angle(get_pt(14), get_pt(12), get_pt(24))
    angles["left_elbow"] = calculate_angle(get_pt(11), get_pt(13), get_pt(15))
    angles["right_elbow"] = calculate_angle(get_pt(12), get_pt(14), get_pt(16))
    angles["left_hip"] = calculate_angle(get_pt(11), get_pt(23), get_pt(25))
    angles["right_hip"] = calculate_angle(get_pt(12), get_pt(24), get_pt(26))
    angles["left_knee"] = calculate_angle(get_pt(23), get_pt(25), get_pt(27))
    angles["right_knee"] = calculate_angle(get_pt(24), get_pt(26), get_pt(28))
    return angles

ideal_exercise_angles = {}
for exercise_name, poses in ideal_exercises_data.items():
    coords = poses.get("pose_1", poses)
    ideal_exercise_angles[exercise_name] = get_ideal_angles_from_coords(coords)

# -----------------------------
# Setup Pose Landmarker
# -----------------------------

MODEL_PATH = "pose_landmarker_lite.task"  # use lite model for quick testing
base_options = python.BaseOptions(model_asset_path=MODEL_PATH)
options = vision.PoseLandmarkerOptions(
    base_options=base_options,
    running_mode=vision.RunningMode.IMAGE,  # <-- switch from LIVE_STREAM to IMAGE
    min_pose_detection_confidence=0.5,
    min_pose_presence_confidence=0.5,
    min_tracking_confidence=0.5
)

pose_landmarker = vision.PoseLandmarker.create_from_options(options)
# -----------------------------
# Detect anomalies
# -----------------------------
def detect_joint_anomalies(joint_angles, exercise, threshold=10.0):
    anomalies = {}
    ideal_vals = ideal_exercise_angles.get(exercise, {})
    for joint, ideal_angle in ideal_vals.items():
        if joint in joint_angles:
            deviation = joint_angles[joint] - ideal_angle
            if abs(deviation) > threshold:
                anomalies[joint] = deviation
    return anomalies

# -----------------------------
# Run exercise analysis for 15 sec
# -----------------------------
def run_exercise_analysis(exercise_name="T_pose", threshold=10.0, monitor_time=15):
    cap = cv2.VideoCapture(0)
    all_detected_anomalies = {}
    start_time = time.time()

    while cap.isOpened() and (time.time() - start_time < monitor_time):
        ret, frame = cap.read()
        if not ret:
            break

        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=frame_rgb)
        results = pose_landmarker.detect(mp_image)
        joint_angles = {}

        if results.pose_landmarks:
            landmarks = results.pose_landmarks[0]

            def get_lm(idx):
                return (landmarks[idx].x, landmarks[idx].y)

            joint_angles["left_shoulder"] = calculate_angle(get_lm(13), get_lm(11), get_lm(23))
            joint_angles["right_shoulder"] = calculate_angle(get_lm(14), get_lm(12), get_lm(24))
            joint_angles["left_elbow"] = calculate_angle(get_lm(11), get_lm(13), get_lm(15))
            joint_angles["right_elbow"] = calculate_angle(get_lm(12), get_lm(14), get_lm(16))
            joint_angles["left_hip"] = calculate_angle(get_lm(11), get_lm(23), get_lm(25))
            joint_angles["right_hip"] = calculate_angle(get_lm(12), get_lm(24), get_lm(26))
            joint_angles["left_knee"] = calculate_angle(get_lm(23), get_lm(25), get_lm(27))
            joint_angles["right_knee"] = calculate_angle(get_lm(24), get_lm(26), get_lm(28))

            anomalies = detect_joint_anomalies(joint_angles, exercise_name, threshold)
            if anomalies:
                for joint, deviation in anomalies.items():
                    all_detected_anomalies[joint] = {"deviation": deviation, "issue": f"deviation of {deviation:.2f}°"}

        cv2.imshow("Exercise Analyzer", frame)
        if cv2.waitKey(5) & 0xFF == 27:
            break

    cap.release()
    cv2.destroyAllWindows()

    # -----------------------------
    # Save anomalies to JSON
    # -----------------------------
    os.makedirs("output", exist_ok=True)
    output_path = os.path.join("output", f"{exercise_name}_anomalies.json")
    with open(output_path, "w") as f:
        json.dump(all_detected_anomalies, f, indent=4)

    print(f"Monitoring complete. Abnormal joints saved to {output_path}")
    return all_detected_anomalies

# -----------------------------
# Removed standalone execution to allow safe importing in main.py
# -----------------------------