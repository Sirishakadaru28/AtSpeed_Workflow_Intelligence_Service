
import os
import joblib
import pandas as pd


# Path to the saved ML model
MODEL_PATH = os.path.join(
    os.path.dirname(os.path.dirname(__file__)),
    "models",
    "risk_model.joblib"
)


# Load model only once when the application starts
model = joblib.load(MODEL_PATH)


def predict_risk(
    category: str,
    priority: str,
    status: str,
    estimated_hours: float,
    dependency_count: int,
    issue_count: int,
    hours_since_update: float,
    hours_until_due: float
):
    """
    Predict risk level and risk probability.
    """

    # Create input DataFrame
    input_data = pd.DataFrame([{
        "category": category,
        "priority": priority,
        "status": status,
        "estimated_hours": estimated_hours,
        "dependency_count": dependency_count,
        "issue_count": issue_count,
        "hours_since_update": hours_since_update,
        "hours_until_due": hours_until_due
    }])

    # Predict risk level
    risk_level = model.predict(input_data)[0]

    # Get probabilities for each class
    probabilities = model.predict_proba(input_data)[0]

    # Find probability corresponding to predicted class
    class_names = model.classes_

    predicted_index = list(class_names).index(risk_level)

    risk_score = float(probabilities[predicted_index])

    # Generate interpretable factors
    factors = []

    if priority == "HIGH":
        factors.append("high_priority")

    if status == "BLOCKED":
        factors.append("blocked_status")

    if issue_count >= 5:
        factors.append("high_issue_count")

    if dependency_count >= 3:
        factors.append("high_dependency_count")

    if hours_since_update >= 48:
        factors.append("long_time_since_update")

    if estimated_hours >= 40:
        factors.append("high_estimated_effort")

    if hours_until_due <= 48:
        factors.append("near_due_date")

    # If no major factors were detected
    if not factors:
        factors.append("normal_operational_conditions")

    return {
        "risk_level": risk_level,
        "risk_score": risk_score,
        "top_factors": factors[:3]
    }
