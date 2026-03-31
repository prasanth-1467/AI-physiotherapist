"""Module 2 Data Flow
Connects SuggestionAgent → ResultsAgent (+ VoiceFeedback) → TrackerAgent.
"""
from utils.logger import get_logger
from agents.module2 import SuggestionAgent, ResultsAgent, TrackerAgent, VoiceFeedbackAgent, VoiceFeedbackContext

logger = get_logger(__name__)

class Module2Flow:
    def __init__(self, llm_client=None, live_stream_service=None,
                 pose_estimation_service=None, angle_calculator_service=None, voice_service=None):
        self.suggestion = SuggestionAgent(llm_client=llm_client)
        self.results = ResultsAgent(live_stream_service=live_stream_service,
                                    pose_estimation_service=pose_estimation_service,
                                    angle_calculator_service=angle_calculator_service)
        self.tracker = TrackerAgent(llm_client=llm_client)
        self.voice = VoiceFeedbackAgent(voice_service=voice_service,
                                        pose_estimation_service=pose_estimation_service,
                                        angle_calculator_service=angle_calculator_service)
        self.stream = live_stream_service
        logger.info("Module2Flow initialized")

    def run(self, summary, user_id, week_number=1, fps=None, duration=None):
        # 1. Generate exercise suggestions from confirmed summary
        suggestions = self.suggestion.process_summary(summary, user_id)
        logger.info(f"Suggestions ready: {suggestions['total_suggestions']} exercises")

        # 2. Track each exercise with voice feedback running in parallel
        frame_getter = self.stream.get_frame if self.stream else None
        for ex in suggestions["suggestions"]:
            with VoiceFeedbackContext(self.voice, ex, frame_getter):
                pass  # ResultsAgent handles frames internally
        daily_result = self.results.process_suggestions(suggestions, fps=fps, duration=duration)
        logger.info(f"Session done, avg score: {daily_result['average_score']}")

        # 3. Feed daily result into weekly tracker
        tracking = self.tracker.process_daily_result(daily_result, week_number)
        logger.info(f"Tracking: day {tracking['days_logged']}, week_completed={tracking['week_completed']}")

        return {"suggestions": suggestions, "daily_result": daily_result, "tracking": tracking}
