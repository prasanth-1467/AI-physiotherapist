# Module 2 - Exercise Suggestion and Results Tracking

This module is responsible for generating personalized exercise suggestions, tracking real-time performance during exercises, monitoring weekly progress, and providing voice feedback to users.

## 📁 Module Structure

```
module2/
├── __init__.py                    # Module exports
├── suggestion_agent.py            # Generates exercise suggestions
├── results_agent.py               # Tracks exercise performance
├── tracker_agent.py               # Monitors weekly progress
├── voice_feedback_agent.py        # Provides real-time voice feedback
└── README.md                      # This file
```

---

## 🎯 Agents Overview

### 1. **Suggestion Agent** (`suggestion_agent.py`)

**Purpose:** Receives confirmed injury summary and generates personalized exercise suggestions.

**Key Responsibilities:**
- Load user's rehabilitation history
- Use LLM to suggest 2-3 exercises tailored to injury type
- Validate exercise safety (angle ranges, difficulty level)
- Save suggestions for tracking

**Input:**
```python
{
    "user_id": "user_001",
    "injury_type": "sprain",
    "affected_body_part": "shoulder",
    "severity": "moderate",
    "confirmed": True,
    "rehab_start_date": "2026-02-01"
}
```

**Output:**
```python
{
    "user_id": "user_001",
    "week_number": 1,
    "suggestions": [
        {
            "name": "Shoulder Raise",
            "target_joint": "shoulder",
            "reps": 10,
            "sets": 3,
            "ideal_angle_min": 60,
            "ideal_angle_max": 180,
            "difficulty_level": "easy",
            "reason": "Improves shoulder mobility"
        }
    ],
    "total_suggestions": 2,
    "status": "success"
}
```

**Usage:**
```python
from agents.module2 import SuggestionAgent

agent = SuggestionAgent(llm_client=your_llm_client)
result = agent.process_summary(summary_data, user_id="user_001")
```

---

### 2. **Results Agent** (`results_agent.py`)

**Purpose:** Tracks exercise performance in real-time by monitoring pose and angles.

**Key Responsibilities:**
- Start live stream for each exercise
- Get pose keypoints from each frame (30 FPS)
- Calculate joint angles and compare to ideal range
- Track correct vs incorrect frames
- Calculate performance score (0-100%)
- Identify persistent errors (>2 seconds)
- Save detailed results

**Input:** Exercise suggestions from Suggestion Agent

**Output:**
```python
{
    "user_id": "user_001",
    "session_date": "2026-02-21",
    "total_exercises": 2,
    "average_score": 78.5,
    "results": [
        {
            "exercise_name": "Shoulder Raise",
            "target_joint": "shoulder",
            "ideal_angle_min": 60,
            "ideal_angle_max": 180,
            "total_frames": 900,
            "correct_frames": 720,
            "performance_score": 80.0,
            "performance_rating": "Good",
            "errors": [
                {
                    "joint": "shoulder",
                    "avg_deviation": 15.2,
                    "duration": 3.5,
                    "frame_start": 100,
                    "frame_end": 205
                }
            ]
        }
    ],
    "status": "success"
}
```

**Performance Ratings:**
- 90-100%: Excellent
- 75-89%: Good
- 60-74%: Fair
- 40-59%: Needs Improvement
- 0-39%: Poor

**Usage:**
```python
from agents.module2 import ResultsAgent

agent = ResultsAgent(
    live_stream_service=stream_service,
    pose_estimation_service=pose_service,
    angle_calculator_service=angle_service
)
result = agent.process_suggestions(suggestions)
```

---

### 3. **Tracker Agent** (`tracker_agent.py`)

**Purpose:** Accumulates daily results into weekly logs and analyzes progress trends.

**Key Responsibilities:**
- Store daily results in weekly log (7 days)
- On Day 7: run comprehensive analysis
- Calculate improvement delta (within week)
- Compare with previous weeks
- Identify weak and strong joints
- Generate recommendations for next week
- Use LLM for detailed insights

**Input:** Daily results from Results Agent

**Output (Week Complete):**
```python
{
    "user_id": "user_001",
    "week_number": 1,
    "week_completed": True,
    "analysis": {
        "days_attended": 7,
        "overall_week_score": 76.5,
        "improvement_delta": 8.2,
        "improvement_from_last_week": 5.3,
        "trend": "improving",
        "daily_scores": [70, 72, 74, 76, 78, 80, 82],
        "weak_joints": ["shoulder"],
        "strong_joints": ["elbow"],
        "recommendations": [
            "Continue with current routine",
            "Consider increasing difficulty",
            "Pay extra attention to shoulder"
        ],
        "overall_assessment": "Week 1 completed with positive progress."
    },
    "status": "success"
}
```

**Trend Categories:**
- **Improving:** improvement_delta > 5%
- **Stable:** -5% ≤ improvement_delta ≤ 5%
- **Regressing:** improvement_delta < -5%

**Usage:**
```python
from agents.module2 import TrackerAgent

agent = TrackerAgent(llm_client=your_llm_client)
result = agent.process_daily_result(daily_result)
```

---

### 4. **Voice Feedback Agent** (`voice_feedback_agent.py`)

**Purpose:** Provides real-time audio feedback during exercises (every 5 seconds).

**Key Responsibilities:**
- Run in parallel thread during exercise
- Check angles every 5 seconds
- Generate contextual feedback based on performance
- Convert text to speech via voice_service
- Play audio immediately to user
- Save audio clips for review

**Feedback Types:**
- **Correct angle:** "Perfect! Keep it up!"
- **Angle too low:** "Raise your shoulder a little more"
- **Angle too high:** "Don't overextend, bring it down"
- **Posture issue:** "Straighten your back"

**Usage:**
```python
from agents.module2 import VoiceFeedbackAgent, VoiceFeedbackContext

agent = VoiceFeedbackAgent(
    voice_service=voice_service,
    pose_estimation_service=pose_service,
    angle_calculator_service=angle_service
)

# Manual control
agent.start(exercise_data, frame_getter_function)
# ... exercise runs ...
agent.stop()

# Or use context manager (recommended)
with VoiceFeedbackContext(agent, exercise_data, frame_getter_function):
    # Feedback runs automatically during this block
    track_exercise_performance()
```

---

## 🔄 Data Flow

```
Module 1 (Summarizer)
    ↓
[Confirmed Summary]
    ↓
Suggestion Agent ──→ Generates exercises
    ↓
[Exercise Suggestions]
    ↓
Results Agent ──────→ Tracks performance
    ↓                 ↑
[Daily Results]       │
    ↓                 │
Tracker Agent         │ (parallel)
    ↓                 │
[Weekly Analysis] ←───┘ Voice Feedback Agent
    ↓
Module 3 (Reporting)
```

---

## 📊 Storage Paths

All paths are relative to project root:

### Input Storage
- **Rehab History:** `storage/user_profiles/rehab_history/{user_id}_history.json`

### Output Storage
- **Exercise Suggestions:** `output/suggestions/exercise_suggestions/{user_id}_week{N}_{timestamp}.json`
- **Exercise Results:** `output/results/{user_id}_{date}_{timestamp}_results.json`
- **Angle Data:** `storage/processed/angle_data/{user_id}_{date}_{timestamp}_results.json`
- **Weekly Logs:** `storage/sessions/weekly/{user_id}_week{N}.json`
- **Weekly Summaries:** `output/tracker/{user_id}_week{N}_summary_{timestamp}.json`
- **Voice Feedback:** `output/feedback/voice_feedback/feedback_{count}_{timestamp}.wav`

---

## 🧪 Testing

Each agent includes a `__main__` block for standalone testing:

```bash
# Test Suggestion Agent
python agents/module2/suggestion_agent.py

# Test Results Agent
python agents/module2/results_agent.py

# Test Tracker Agent
python agents/module2/tracker_agent.py

# Test Voice Feedback Agent
python agents/module2/voice_feedback_agent.py
```

---

## 🔗 Dependencies

### Internal
- `utils.logger` - Logging functionality
- `utils.validator` - Data validation
- `utils.helpers` - Helper functions
- `models.*` - Data models
- `config` - Configuration settings

### External Services
- **Live Stream Service** - Camera/video feed
- **Pose Estimation Service** - Body keypoint detection
- **Angle Calculator Service** - Joint angle calculation
- **Voice Service** - Text-to-speech conversion
- **LLM Client** - AI-powered analysis and suggestions

---

## 🛠️ Configuration

Key configuration parameters in `config.py`:

```python
# Exercise tracking
CAMERA_INDEX = 0
FRAME_WIDTH = 640
FRAME_HEIGHT = 480
FPS = 30

# Voice feedback
VOICE_FEEDBACK_INTERVAL = 5  # seconds

# Performance thresholds
EXCELLENT_THRESHOLD = 90
GOOD_THRESHOLD = 75
FAIR_THRESHOLD = 60
POOR_THRESHOLD = 40

# Weekly tracking
DAYS_PER_WEEK = 7
IMPROVEMENT_THRESHOLD = 5  # percent
```

---

## 📝 Notes

1. **LLM Integration:** Both Suggestion and Tracker agents use LLM for intelligent analysis. If LLM is unavailable, fallback logic is used.

2. **Real-time Processing:** Results Agent processes at 30 FPS. Voice Feedback Agent runs every 5 seconds to avoid overwhelming the user.

3. **Error Handling:** All agents include comprehensive error handling with fallback mechanisms.

4. **Thread Safety:** Voice Feedback Agent runs in a separate daemon thread and safely coordinates with the main Results Agent.

5. **Data Validation:** Exercise suggestions are validated for safety (angle ranges, difficulty appropriateness) before being presented to users.

---

## 🚀 Integration Example

```python
from agents.module2 import (
    SuggestionAgent,
    ResultsAgent,
    TrackerAgent,
    VoiceFeedbackAgent
)

# Initialize agents
suggestion_agent = SuggestionAgent(llm_client=llm)
results_agent = ResultsAgent(
    live_stream_service=stream,
    pose_estimation_service=pose,
    angle_calculator_service=angle
)
tracker_agent = TrackerAgent(llm_client=llm)
voice_agent = VoiceFeedbackAgent(
    voice_service=voice,
    pose_estimation_service=pose,
    angle_calculator_service=angle
)

# Process workflow
# 1. Generate suggestions
suggestions = suggestion_agent.process_summary(summary, user_id)

# 2. Track exercises with voice feedback
with VoiceFeedbackContext(voice_agent, exercise, frame_getter):
    results = results_agent.process_suggestions(suggestions)

# 3. Track progress
tracking = tracker_agent.process_daily_result(results)

# 4. Check if week complete
if tracking['week_completed']:
    print(f"Week completed! Analysis: {tracking['analysis']}")
```

---

**Module 2 Complete ✅**
