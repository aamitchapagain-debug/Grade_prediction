from pathlib import Path
import joblib
import numpy as np
from django.conf import settings

MODEL_PATH = Path(settings.BASE_DIR) / "predictor" / "grade_model.joblib"
FEATURES = ["attendance", "unit_tests", "assignments", "classwork"]

def score_to_grade(score):
    # Change these cutoffs to match your institution's grading policy.
    if score >= 90: return "A+"
    if score >= 80: return "A"
    if score >= 70: return "B"
    if score >= 60: return "C"
    if score >= 50: return "D"
    return "F"

def predict_score(attendance, unit_tests, assignments, classwork):
    values = np.array([[attendance, unit_tests, assignments, classwork]], dtype=float)
    if MODEL_PATH.exists():
        model = joblib.load(MODEL_PATH)
        score = float(model.predict(values)[0])
        method = "trained ML model"
    else:
        # Transparent baseline: replace weights with your college's policy if needed.
        score = (attendance * 0.10 + unit_tests * 0.40 +
                 assignments * 0.30 + classwork * 0.20)
        method = "weighted baseline (no trained model found)"
    score = max(0.0, min(100.0, score))
    return round(score, 2), score_to_grade(score), method
