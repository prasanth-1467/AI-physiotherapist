import os
import json
from google import genai
from pydantic import BaseModel, Field
from typing import List, Dict, Optional

os.environ["GOOGLE_API_KEY"] = "AIzaSyCKvdywgqlLscJkER4-ft9M-JL6QVEQZZQ"

class PatientSummaryOutput(BaseModel):
    summary: str
    key_findings: List[str]
    recommendations: List[str]
    risk_factors: List[str]

class PatientSummaryAnalyzer:
    def __init__(self, api_key: str = None):
        key = api_key or "AIzaSyCKvdywgqlLscJkER4-ft9M-JL6QVEQZZQ" or os.environ.get("GOOGLE_API_KEY")
        if not key:
            raise ValueError("GOOGLE_API_KEY environment variable is missing. Please set it using: export GOOGLE_API_KEY='your_api_key'")
        self.client = genai.Client(api_key=key)
        self.model = "gemini-2.5-flash"
        
    def generate_summary(self, patient_id: str, exercise_anomalies: dict, report_analysis: dict, joint_analysis: dict, user_answers: dict = None) -> PatientSummaryOutput:
        
        user_answers_context = f"- user_answers (patient's direct responses to follow-up questions): {json.dumps(user_answers)}" if user_answers else ""
        
        prompt = f"""
        You are a specialized medical report summarization agent. 
        Analyze patient data and generate comprehensive summaries.
        
        Input Data:
        - patient_id: {patient_id}
        - exercise_anomalies: {json.dumps(exercise_anomalies)}
        - report_analysis: {json.dumps(report_analysis)}
        - joint_analysis: {json.dumps(joint_analysis)}
        {user_answers_context}

        Return EXACTLY this JSON format and nothing else:
        {{
            "summary": "Comprehensive patient summary",
            "key_findings": ["list of key findings"],
            "recommendations": ["list of recommendations"],
            "risk_factors": ["list of risk factors"]
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
                result_data = json.loads(response.text)
            except json.JSONDecodeError:
                cleaned = response.text.replace('```json', '').replace('```', '').strip()
                result_data = json.loads(cleaned)
            
            return PatientSummaryOutput(
                summary=result_data.get("summary", ""),
                key_findings=result_data.get("key_findings", []),
                recommendations=result_data.get("recommendations", []),
                risk_factors=result_data.get("risk_factors", [])
            )
        except Exception as e:
            raise Exception(f"Error generating summary: {str(e)}")

def generate_patient_summary(patient_id: str, exercise_anomalies_file: str,
                            report_analysis_file: str, joint_analysis_file: str = None, user_answers_file: str = None) -> PatientSummaryOutput:
    """Generate patient summary"""
    
    # Load files
    with open(exercise_anomalies_file, 'r') as f:
        exercise_anomalies = json.load(f)
    
    with open(report_analysis_file, 'r') as f:
        report_analysis = json.load(f)
    
    if joint_analysis_file:
        with open(joint_analysis_file, 'r') as f:
            joint_analysis = json.load(f)
    else:
        joint_analysis = exercise_anomalies
        
    user_answers = None
    if user_answers_file and os.path.exists(user_answers_file):
        with open(user_answers_file, 'r') as f:
            user_answers = json.load(f)
    
    analyzer = PatientSummaryAnalyzer()
    return analyzer.generate_summary(
        patient_id=patient_id,
        exercise_anomalies=exercise_anomalies,
        report_analysis=report_analysis,
        joint_analysis=joint_analysis,
        user_answers=user_answers
    )

# Main
if __name__ == "__main__":
    result = generate_patient_summary(
        patient_id="patient123",
        exercise_anomalies_file="output/T_pose_anomalies.json",
        report_analysis_file="output/patient123_medical_report_analysis.json",
        joint_analysis_file=None,
        user_answers_file="output/patient123_user_answers.json"
    )
    
    print(f"Summary: {result.summary}")
    print(f"Key Findings: {result.key_findings}")
    print(f"Recommendations: {result.recommendations}")
    print(f"Risk Factors: {result.risk_factors}")