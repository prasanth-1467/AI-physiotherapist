from datetime import datetime
from utils.logger import get_logger
from pypdf import PdfReader

logger = get_logger(__name__)


class ReportParserService:
    """
    Rule-based report parser that converts raw report text into a structured summary.
    """

    JOINT_KEYWORDS = {
        "shoulder": ["shoulder", "rotator", "scapula", "clavicle"],
        "elbow": ["elbow", "ulna", "radius"],
        "wrist": ["wrist", "carpal"],
        "knee": ["knee", "patella", "acl", "mcl", "meniscus"],
        "hip": ["hip", "acetabulum", "femur"],
        "ankle": ["ankle", "achilles", "talus"],
        "back": ["back", "spine", "lumbar", "thoracic"],
        "neck": ["neck", "cervical"],
    }

    def parse_report(self, report_text, patient_id="PT_001", rehab_start_date=None):
        text = (report_text or "").lower()
        joint = self._detect_joint(text) or "shoulder"
        issue = self._detect_issue(text)
        cause = self._detect_cause(text)
        confidence = 0.82 if joint else 0.6
        rehab_start_date = rehab_start_date or datetime.now().strftime("%Y-%m-%d")

        summary = {
            "patient_id": patient_id,
            "affected_joints": [
                {
                    "joint": joint,
                    "issue": issue,
                    "cause": cause,
                    "deviation": 18.0,
                    "confidence": confidence,
                }
            ],
            "specific_injuries": [self._injury_phrase(joint, issue, cause)],
            "follow_up_questions": self._follow_ups(joint),
            "summary_text": f"Patient shows {issue} at the {joint} likely due to {cause}.",
            "affected_body_part": joint,
            "severity": self._detect_severity(text),
            "rehab_start_date": rehab_start_date,
            "confirmed": True,
        }
        logger.info(f"Parsed report for {patient_id}: joint={joint}, issue={issue}")
        return summary

    def parse_pdf(self, file_bytes):
        try:
            reader = PdfReader(file_bytes)
            text = ""
            for page in reader.pages:
                text += page.extract_text() or ""
            return text.strip()
        except Exception as exc:
            logger.error(f"PDF parse error: {exc}")
            return ""

    def _detect_joint(self, text):
        for joint, keys in self.JOINT_KEYWORDS.items():
            if any(k in text for k in keys):
                return joint
        return None

    def _detect_issue(self, text):
        if any(k in text for k in ["fracture", "break"]):
            return "fracture"
        if any(k in text for k in ["tear", "sprain", "strain"]):
            return "soft_tissue_injury"
        if any(k in text for k in ["dislocation", "instability"]):
            return "joint_instability"
        if any(k in text for k in ["weakness", "weak"]):
            return "muscle_weakness"
        return "mobility_limitation"

    def _detect_cause(self, text):
        if "sports" in text or "athletic" in text:
            return "sports_injury"
        if "fall" in text or "fell" in text:
            return "fall"
        if "overuse" in text:
            return "overuse"
        return "unknown"

    def _detect_severity(self, text):
        if any(k in text for k in ["severe", "grade 3", "complete tear"]):
            return "severe"
        if any(k in text for k in ["moderate", "grade 2"]):
            return "moderate"
        if any(k in text for k in ["mild", "grade 1"]):
            return "mild"
        return "moderate"

    def _injury_phrase(self, joint, issue, cause):
        joint_name = joint.replace("_", " ")
        issue_name = issue.replace("_", " ")
        return f"{issue_name.title()} at the {joint_name} ({cause})"

    def _follow_ups(self, joint):
        return [
            f"Do you feel pain when moving your {joint}?",
            f"Do you experience instability or weakness in the {joint}?",
        ]
