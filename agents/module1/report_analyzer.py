import cv2
import mediapipe as mp
import numpy as np
import math
import time
import json
import os
from PIL import Image
import pytesseract
import PyPDF2
import asyncio
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
from google import genai
from pydantic import BaseModel, Field
from typing import List, Dict

# -----------------------------
# Pydantic input/output schemas
# -----------------------------
class MedicalReportInput(BaseModel):
    report_text: str

class MedicalReportAnalysisOutput(BaseModel):
    abnormalities: List[str]
    severity: Dict[str, str]
    affected_joints: Dict[str, str]
    follow_up_questions: List[str]

class PatientSummaryInput(BaseModel):
    patient_id: str
    exercise_anomalies: Dict
    report_analysis: Dict
    joint_analysis: Dict

class PatientSummaryOutput(BaseModel):
    patient_id: str
    affected_joints: List[Dict]
    specific_injuries: List[str]
    follow_up_questions: List[str]
    summary_text: str

# -----------------------------
# Initialize LLM agents
# -----------------------------
class MedicalReportAnalyzer:
    def __init__(self, api_key: str = None):
        key = "AIzaSyCKvdywgqlLscJkER4-ft9M-JL6QVEQZZQ"
        if not key:
            raise ValueError("GOOGLE_API_KEY environment variable is missing. Please set it using: export GOOGLE_API_KEY='your_api_key'")
        self.client = genai.Client(api_key=key)
        self.model = "gemini-2.5-flash"
        
    def analyze_report(self, text: str) -> MedicalReportAnalysisOutput:
        prompt = f"""
        Analyze the following medical report and extract information in the specified format:

        Medical Report:
        {text}

        Please provide the following analysis:
        1. abnormalities: List of abnormal findings detected
        2. severity: Dictionary mapping each abnormality to its severity
        3. affected_joints: Dictionary mapping each affected joint to its condition
        4. follow_up_questions: List of questions for further clarification

        Return EXACTLY this JSON format and nothing else:
        {{
            "abnormalities": ["finding1", "finding2"],
            "severity": {{"finding1": "high"}},
            "affected_joints": {{"joint1": "condition"}},
            "follow_up_questions": ["question1"]
        }}
        """
        
        try:
            response = self.client.models.generate_content(
                model=self.model,
                contents=f"You are a medical report analysis assistant. Extract and analyze medical findings accurately.\n\n{prompt}",
                config={
                    'response_mime_type': 'application/json',
                    'temperature': 0.3
                }
            )
            try:
                analysis_data = json.loads(response.text)
            except json.JSONDecodeError:
                cleaned_text = response.text.strip().replace('```json', '').replace('```', '')
                analysis_data = json.loads(cleaned_text)
            return MedicalReportAnalysisOutput(**analysis_data)
        except Exception as e:
            raise Exception(f"Error analyzing report: {str(e)}")

class PatientSummaryAnalyzer:
    def __init__(self, api_key: str = None):
        key = api_key or "AIzaSyCKvdywgqlLscJkER4-ft9M-JL6QVEQZZQ" or os.environ.get("GOOGLE_API_KEY")
        if not key:
            raise ValueError("GOOGLE_API_KEY environment variable is missing. Please set it using: export GOOGLE_API_KEY='your_api_key'")
        self.client = genai.Client(api_key=key)
        self.model = "gemini-2.5-flash"
        
    def generate_summary(self, patient_id: str, exercise_anomalies: dict, report_analysis: dict, joint_analysis: dict) -> PatientSummaryOutput:
        prompt = f"""
        You are a physiotherapy summarizer agent. Combine exercise anomalies and medical report findings.
        Identify affected joints, specific injuries, and causes. Confirm uncertain issues with the patient by generating questions.
        Generate a structured summary report.

        Input Data:
        Patient ID: {patient_id}
        Exercise Anomalies: {json.dumps(exercise_anomalies)}
        Report Analysis: {json.dumps(report_analysis)}
        Joint Analysis: {json.dumps(joint_analysis)}

        Return EXACTLY this JSON format and nothing else:
        {{
            "patient_id": "{patient_id}",
            "affected_joints": [{{"joint_name": "condition"}}],
            "specific_injuries": ["injury1"],
            "follow_up_questions": ["question1"],
            "summary_text": "Detailed summary..."
        }}
        """
        
        try:
            response = self.client.models.generate_content(
                model=self.model,
                contents=f"You are a physiotherapy summarizer assistant.\n\n{prompt}",
                config={
                    'response_mime_type': 'application/json',
                    'temperature': 0.3
                }
            )
            try:
                analysis_data = json.loads(response.text)
            except json.JSONDecodeError:
                cleaned_text = response.text.strip().replace('```json', '').replace('```', '')
                analysis_data = json.loads(cleaned_text)
            if "patient_id" not in analysis_data:
                analysis_data["patient_id"] = patient_id
            return PatientSummaryOutput(**analysis_data)
        except Exception as e:
            raise Exception(f"Error generating summary: {str(e)}")

# -----------------------------
# Load ideal exercise poses
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
MODEL_PATH = "pose_landmarker_lite.task"
base_options = python.BaseOptions(model_asset_path=MODEL_PATH)
options = vision.PoseLandmarkerOptions(
    base_options=base_options,
    running_mode=vision.RunningMode.IMAGE,
    min_pose_detection_confidence=0.5,
    min_pose_presence_confidence=0.5,
    min_tracking_confidence=0.5
)
pose_landmarker = vision.PoseLandmarker.create_from_options(options)

# -----------------------------
# Detect joint anomalies
# -----------------------------
def detect_joint_anomalies(joint_angles, exercise, threshold=10.0):
    anomalies = {}
    ideal_vals = ideal_exercise_angles.get(exercise, {})
    for joint, ideal_angle in ideal_vals.items():
        if joint in joint_angles:
            deviation = joint_angles[joint] - ideal_angle
            if abs(deviation) > threshold:
                anomalies[joint] = {"deviation": deviation, "issue": f"deviation of {deviation:.2f}°"}
    return anomalies

# -----------------------------
# OCR / PDF helpers
# -----------------------------
def extract_text_from_pdf(pdf_path: str) -> str:
    text = ""
    with open(pdf_path, "rb") as f:
        reader = PyPDF2.PdfReader(f)
        for page in reader.pages:
            text += page.extract_text() or ""
    return text

def extract_text_from_image(image_path: str) -> str:
    img = Image.open(image_path)
    return pytesseract.image_to_string(img)

# -----------------------------
# Analyze medical report
# -----------------------------
def analyze_medical_report(file_path: str, patient_id: str = "patient", output_folder: str = "output"):
    ext = os.path.splitext(file_path)[1].lower()
    if ext in [".pdf"]:
        text = extract_text_from_pdf(file_path)
    elif ext in [".jpg", ".jpeg", ".png", ".bmp", ".tiff"]:
        text = extract_text_from_image(file_path)
    else:
        raise ValueError("Unsupported file type")

    analyzer = MedicalReportAnalyzer()
    result = analyzer.analyze_report(text)

    os.makedirs(output_folder, exist_ok=True)
    output_path = os.path.join(output_folder, f"{patient_id}_medical_report_analysis.json")
    with open(output_path, "w") as f:
        if hasattr(result, "model_dump"):
            json.dump(result.model_dump(), f, indent=4)
        else:
            json.dump(result, f, indent=4)

    print(f"Medical report analysis saved to {output_path}")
    return result
# -----------------------------
# Generate patient summary
# -----------------------------
def generate_patient_summary(patient_id: str, exercise_anomalies: dict, report_analysis: dict, joint_analysis: dict, output_folder: str = "output"):
    input_dict = {
        "patient_id": patient_id,
        "exercise_anomalies": exercise_anomalies,
        "report_analysis": report_analysis,
        "joint_analysis": joint_analysis
    }

    analyzer = PatientSummaryAnalyzer()
    summary_result = analyzer.generate_summary(
        patient_id=patient_id, 
        exercise_anomalies=exercise_anomalies, 
        report_analysis=report_analysis, 
        joint_analysis=joint_analysis
    )

    os.makedirs(output_folder, exist_ok=True)
    output_path = os.path.join(output_folder, f"{patient_id}_summary.json")
    with open(output_path, "w") as f:
        if hasattr(summary_result, "model_dump"):
            json.dump(summary_result.model_dump(), f, indent=4)
        else:
            json.dump(summary_result, f, indent=4)

    print(f"Patient summary saved to {output_path}")
    return summary_result
# -----------------------------
# Main pipeline
# -----------------------------
if __name__ == "__main__":
    patient_id = "patient123"

    # 1️⃣ Monitor exercise
    anomalies = {}
    # Replace 'data.json' with the path to your actual JSON file
    file_path = 'output/T_pose_anomalies.json'
    # Open the JSON file in read mode ('r')
    with open(file_path, 'r') as file:
        # Use json.load() to convert the file content to a Python dictionary
        anomalies = json.load(file)
    # 2️⃣ Analyze medical report
    file_path = "Elbow_fractures.pdf"  # replace with your file
    report_result = analyze_medical_report(file_path, patient_id=patient_id)

    # 3️⃣ Generate patient summary
    summary = generate_patient_summary(
        patient_id=patient_id,
        exercise_anomalies=anomalies,
        report_analysis=report_result.model_dump() if hasattr(report_result, "model_dump") else report_result,
        joint_analysis=anomalies
    )

    # 4️⃣ Save combined JSON
    combined = {
        "patient_id": patient_id,
        "exercise_anomalies": anomalies,
        "medical_report_analysis": report_result.model_dump() if hasattr(report_result, "model_dump") else report_result,
        "patient_summary": summary.model_dump() if hasattr(summary, "model_dump") else summary
    }

    os.makedirs("output", exist_ok=True)
    combined_path = os.path.join("output", f"{patient_id}_combined_analysis.json")
    with open(combined_path, "w") as f:
        json.dump(combined, f, indent=4)

    print(f"Combined analysis saved to {combined_path}")