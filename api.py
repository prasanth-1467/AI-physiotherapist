from fastapi import FastAPI, UploadFile, File, Form
from pydantic import BaseModel, Field
from typing import Optional, Dict, Any

from core.data_flow import Module2Flow
from core.pipeline import Pipeline
from services import (
    LiveStreamService,
    PoseEstimationService,
    AngleCalculatorService,
    ReportParserService,
    VoiceService,
)
from config import config
from agents.module3 import TrackerWeekAgent, TrackerMonthAgent, FeedbackAgent


class RunRequest(BaseModel):
    user_id: str = Field("PT_001", description="User identifier")
    rehab_goal: str = Field("restore full mobility", description="Rehab goal statement")
    report_text: Optional[str] = Field(None, description="Raw medical report text")
    summary: Optional[Dict[str, Any]] = Field(None, description="Pre-parsed summary")
    rehab_start_date: Optional[str] = Field(None, description="YYYY-MM-DD")
    week_number: int = Field(1, description="Rehab week number")
    fps: int = Field(30, description="Frames per second for tracking")
    duration: int = Field(10, description="Seconds per exercise")


class WeeklyReportRequest(BaseModel):
    user_id: str
    week_number: int = 1
    analysis: Dict[str, Any]


class MonthlyReportRequest(BaseModel):
    user_id: str
    month_number: int = 1
    current_result: Dict[str, Any]


class FeedbackRequest(BaseModel):
    user_id: str
    weekly_report: Dict[str, Any]
    monthly_report: Optional[Dict[str, Any]] = None


def create_app() -> FastAPI:
    app = FastAPI(title="AI Physiotherapist API", version="1.0.0")

    report_parser = ReportParserService()
    stream = LiveStreamService(
        camera_index=config.CAMERA_INDEX,
        fps=30,
        width=config.FRAME_WIDTH,
        height=config.FRAME_HEIGHT,
    )
    pose = PoseEstimationService()
    angle = AngleCalculatorService()
    module2 = Module2Flow(
        live_stream_service=stream,
        pose_estimation_service=pose,
        angle_calculator_service=angle,
        voice_service=None,
    )
    pipeline = Pipeline(stream=stream, pose=pose, angle=angle)
    week_agent = TrackerWeekAgent()
    month_agent = TrackerMonthAgent()
    feedback_agent = FeedbackAgent()

    @app.get("/health")
    def health():
        return {"status": "ok"}

    @app.post("/run")
    def run_pipeline(payload: RunRequest):
        summary = payload.summary
        if not summary:
            summary = report_parser.parse_report(
                payload.report_text or "",
                patient_id=payload.user_id,
                rehab_start_date=payload.rehab_start_date,
            )
        module2_result = module2.run(
            summary,
            payload.user_id,
            week_number=payload.week_number,
            fps=payload.fps,
            duration=payload.duration,
        )
        pipeline_result = pipeline.store(pipeline.evaluate(pipeline.analyze(pipeline.capture())))
        return {
            "summary": summary,
            "module2": module2_result,
            "pipeline": pipeline_result,
            "status": "success",
        }

    @app.post("/run-pdf")
    async def run_pipeline_pdf(
        user_id: str = Form(...),
        rehab_goal: str = Form("restore full mobility"),
        rehab_start_date: Optional[str] = Form(None),
        week_number: int = Form(1),
        fps: int = Form(30),
        duration: int = Form(10),
        file: UploadFile = File(...),
    ):
        content = await file.read()
        text = report_parser.parse_pdf(content)
        summary = report_parser.parse_report(
            text,
            patient_id=user_id,
            rehab_start_date=rehab_start_date,
        )
        module2_result = module2.run(
            summary,
            user_id,
            week_number=week_number,
            fps=fps,
            duration=duration,
        )
        pipeline_result = pipeline.store(pipeline.evaluate(pipeline.analyze(pipeline.capture())))
        return {
            "summary": summary,
            "module2": module2_result,
            "pipeline": pipeline_result,
            "status": "success",
        }

    @app.post("/module3/weekly-report")
    def weekly_report(payload: WeeklyReportRequest):
        report = week_agent.generate_weekly_report(payload.user_id, payload.week_number, payload.analysis)
        return {"report": report, "status": "success"}

    @app.post("/module3/monthly-report")
    def monthly_report(payload: MonthlyReportRequest):
        report = month_agent.generate_monthly_report(payload.user_id, payload.current_result, payload.month_number)
        return {"report": report, "status": "success"}

    @app.post("/module3/feedback")
    def feedback(payload: FeedbackRequest):
        report = feedback_agent.generate_feedback(payload.user_id, payload.weekly_report, payload.monthly_report)
        return {"feedback": report, "status": "success"}

    return app


app = create_app()
