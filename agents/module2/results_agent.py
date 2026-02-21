"""Results Agent - Module 2
Core: Validates motion vs targets → ROM + rep quality + tempo + stability → saves → tracker handoff
"""
import numpy as np
from datetime import datetime
from utils.logger import get_logger
from utils.helpers import ensure_directory, safe_write_json
from config import config

logger = get_logger(__name__)

class ResultsAgent:
    def __init__(self, mediapipe_engine=None):
        self.mediapipe_engine = mediapipe_engine
        self.angle_path = config.DATA_PATH / "processed" / "angle_data"
        self.comp_path = config.DATA_PATH / "processed" / "comparisons"
        ensure_directory(self.angle_path)
        ensure_directory(self.comp_path)
        self.results = []

    def _rom_check(self, series, t):
        if not series:
            return None
        mn, mx = float(np.min(series)), float(np.max(series))
        status = "within_range" if t["ideal_angle_min"] <= mn and mx <= t["ideal_angle_max"] \
                 else ("insufficient" if mx < t["ideal_angle_min"] else "excessive")
        return {"joint": t["joint_or_region"], "observed_min": mn, "observed_max": mx,
                "target_min": t["ideal_angle_min"], "target_max": t["ideal_angle_max"], "status": status}

    def _segment_reps(self, series, times):
        if len(series) < 10:
            return [(series, times)]
        peaks = [i for i in range(1, len(series)-1) if series[i] > series[i-1] and series[i] > series[i+1]]
        if not peaks:
            return [(series, times)]
        return [(series[peaks[i]:peaks[i+1]], times[peaks[i]:peaks[i+1]]) for i in range(len(peaks)-1)]

    def _rep_quality(self, angles, tmin, tmax):
        if len(angles) < 3:
            return "shallow"
        depth = np.max(angles) >= tmax * 0.85
        returned = abs(angles[-1] - angles[0]) <= 10
        smooth = (np.std(np.diff(angles)) if len(angles) > 2 else 0) < 15
        return "good" if (depth and returned and smooth) else (
            "shallow" if not depth else ("incomplete_return" if not returned else "erratic"))

    def _tempo(self, dur):
        return "acceptable" if 2.0 <= dur <= 5.0 else ("too_fast" if dur < 2.0 else "too_slow")

    def _stability(self, series, times):
        if len(series) < 2 or len(times) < 2:
            return {"score": 0.0, "label": "unstable"}
        vel_var = float(np.var(np.diff(series) / np.diff(times)))
        return ({"score": 1.0, "label": "stable"} if vel_var < 50 else
                ({"score": 0.6, "label": "moderate"} if vel_var < 150 else {"score": 0.3, "label": "unstable"}))

    def process_exercise(self, session_id, exercise, data):
        targets = exercise.get("movement_targets", [])
        rom = []
        for t in targets:
            series = data.get("angle_series", {}).get(t["joint_or_region"], [])
            r = self._rom_check(series, t)
            if r:
                rom.append(r)
        reps = []
        first_joint = targets[0]["joint_or_region"] if targets else None
        series = data.get("angle_series", {}).get(first_joint, [])
        times = data.get("timestamps", [])
        for i, (a, ts) in enumerate(self._segment_reps(series, times), 1):
            dur = ts[-1] - ts[0] if len(ts) > 1 else 0.0
            q = self._rep_quality(a, targets[0]["ideal_angle_min"], targets[0]["ideal_angle_max"]) if targets else "shallow"
            reps.append({"rep_number": i, "quality": q, "tempo": self._tempo(dur)})
        stab = self._stability(series, times)
        good_rom = all(r["status"] == "within_range" for r in rom) if rom else False
        good_rep = sum(1 for r in reps if r["quality"] == "good") >= max(1, int(0.7*len(reps))) if reps else False
        good_tempo = sum(1 for r in reps if r["tempo"] == "acceptable") >= max(1, int(0.7*len(reps))) if reps else False
        passes = sum([good_rom, good_rep, good_tempo, stab["label"] in ["stable", "moderate"]])
        status = "correct" if passes >= 3 else ("needs_correction" if passes == 2 else "incorrect")
        score = 85.0 if status == "correct" else (60.0 if status == "needs_correction" else 40.0)
        res = {"session_id": session_id, "exercise_name": exercise.get("name", ""),
               "timestamp": datetime.now().isoformat(), "rom": rom, "reps": reps,
               "stability": stab, "overall_status": status, "overall_score": score}
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        safe_write_json(self.angle_path / f"{session_id}_{exercise.get('name','')}_{ts}.json", {"angle_data": data, "result": res})
        safe_write_json(self.comp_path / f"{session_id}_{exercise.get('name','')}_{ts}.json", res)
        self.results.append(res)
        return res

    def complete_session(self):
        avg = float(np.mean([r["overall_score"] for r in self.results])) if self.results else 0.0
        out = {"session_id": self.results[0]["session_id"] if self.results else None,
               "timestamp": datetime.now().isoformat(), "results": self.results, "average_score": round(avg,1)}
        self.results = []
        return out
