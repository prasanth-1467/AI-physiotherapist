import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.append(str(ROOT))

from services import LiveStreamService, PoseEstimationService, AngleCalculatorService, ReportParserService, VoiceService
from core.data_flow import Module2Flow
from core.pipeline import Pipeline
from agents.module3 import TrackerWeekAgent, TrackerMonthAgent, FeedbackAgent
from config import config


def run():
    report_parser = ReportParserService()
    stream = LiveStreamService(
        camera_index=config.CAMERA_INDEX,
        fps=30,
        width=config.FRAME_WIDTH,
        height=config.FRAME_HEIGHT,
    )
    pose = PoseEstimationService()
    angle = AngleCalculatorService()
    voice = VoiceService()

    summary = report_parser.parse_report(
        "Patient reports shoulder pain and mild instability after a fall.",
        patient_id="PT_002",
        rehab_start_date="2026-02-10",
    )

    module2 = Module2Flow(
        live_stream_service=stream,
        pose_estimation_service=pose,
        angle_calculator_service=angle,
        voice_service=voice,
    )
    module2_result = module2.run(summary, user_id="PT_002", week_number=1)

    pipeline = Pipeline(stream=stream, pose=pose, angle=angle)
    pipeline_snapshot = pipeline.store(pipeline.evaluate(pipeline.analyze(pipeline.capture())))

    week_agent = TrackerWeekAgent()
    weekly_report = week_agent.generate_weekly_report(
        "PT_002", 1, module2_result["tracking"]["analysis"] or {}
    )

    month_agent = TrackerMonthAgent()
    monthly_report = month_agent.generate_monthly_report(
        "PT_002", module2_result["daily_result"], 1
    )

    feedback_agent = FeedbackAgent()
    feedback = feedback_agent.generate_feedback("PT_002", weekly_report, monthly_report)

    output = {
        "summary": summary,
        "module2": module2_result,
        "pipeline": pipeline_snapshot,
        "weekly_report": weekly_report,
        "monthly_report": monthly_report,
        "feedback": feedback,
    }
    print(json.dumps(output, indent=2))


if __name__ == "__main__":
    run()
