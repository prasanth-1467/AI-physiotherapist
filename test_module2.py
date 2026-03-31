"""Quick test for Module 2 agents."""
import json
from agents.module2 import SuggestionAgent, ResultsAgent, TrackerAgent
from services import LiveStreamService, PoseEstimationService, AngleCalculatorService
from config import config

# ---------------------------------------------------
# Confirmed summary from Module 1 (Patient Schema)
# ---------------------------------------------------
summary = {
    "patient_id": "PT_002",
    "affected_joints": [
        {"joint": "shoulder", "issue": "joint_instability", "cause": "dislocation", "deviation": 22.5, "confidence": 0.87},
        {"joint": "scapula", "issue": "muscle_weakness", "cause": "post_dislocation", "deviation": 16.0, "confidence": 0.81}
    ],
    "specific_injuries": ["Anterior shoulder dislocation"],
    "follow_up_questions": [
        "Do you feel instability while lifting your arm?",
        "Do you experience pain during rotation?"
    ],
    "summary_text": "Patient presents with shoulder instability following dislocation, along with weakness in scapular stabilizers affecting controlled arm elevation.",
    "affected_body_part": "shoulder",
    "severity": "moderate",
    "rehab_start_date": "2026-02-10",
    "confirmed": True
}

# ---------------------------------------------------
# Rehab Goal (used by Suggestion Agent prompt)
# ---------------------------------------------------
rehab_goal = "I want to cure my shoulder dislocation and regain full, stable shoulder movement."

# ---------------------------------------------------
# 1) Suggestion Agent
# ---------------------------------------------------
print("=== SUGGESTION AGENT ===")
sa = SuggestionAgent()

# pass rehab_goal if your agent supports it
suggestions = sa.process_summary(summary, rehab_goal=rehab_goal, user_id="PT_002")

print(json.dumps(suggestions, indent=2))


# ---------------------------------------------------
# 2) Results Agent
# (Simulates performing suggested exercises)
# ---------------------------------------------------
print("\n=== RESULTS AGENT ===")
stream = LiveStreamService(
    camera_index=config.CAMERA_INDEX,
    fps=30,
    width=config.FRAME_WIDTH,
    height=config.FRAME_HEIGHT,
)
pose = PoseEstimationService()
angle = AngleCalculatorService()
ra = ResultsAgent(live_stream_service=stream, pose_estimation_service=pose, angle_calculator_service=angle)

daily_result = ra.process_suggestions(suggestions)

print(json.dumps(daily_result, indent=2))


# ---------------------------------------------------
# 3) Tracker Agent (Simulate 7-Day Recovery Window)
# ---------------------------------------------------
print("\n=== TRACKER AGENT ===")
ta = TrackerAgent()

for day in range(1, 8):
    fake_daily = {
        "user_id": "PT_002",
        "session_date": f"2026-02-{day + 14}",
        "total_exercises": len(suggestions),
        "average_score": 62 + day * 4,   # simulate improvement
        "results": [
            {"target_joint": "shoulder", "performance_score": 62 + day * 4}
        ],
        "status": "success"
    }

    track = ta.process_daily_result(fake_daily, week_number=1)

    status = "WEEK COMPLETE" if track["week_completed"] else f"day {track['days_logged']}/7"
    print(f"  Day {day}: score={fake_daily['average_score']}, {status}")


# ---------------------------------------------------
# Weekly Analysis Output
# ---------------------------------------------------
if track["week_completed"]:
    print("\n=== WEEKLY ANALYSIS ===")
    print(json.dumps(track["analysis"], indent=2))


print("\nModule 2 test PASSED ")
