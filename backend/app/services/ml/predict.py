import joblib
import pandas as pd
from app.services.ml.feature_builder import SalaryFeatureBuilder  # noqa: F401 (needed for unpickling)

_salary_bundle = None
_category_bundle = None

def _load_models():
    global _salary_bundle, _category_bundle
    if _salary_bundle is None:
        _salary_bundle = joblib.load("salary_model.joblib")
    if _category_bundle is None:
        _category_bundle = joblib.load("category_model.joblib")

def predict_salary(title: str, location: str, skills: list[str], years_experience: float = 3.0) -> dict:
    _load_models()
    builder = _salary_bundle["builder"]
    model = _salary_bundle["model"]

    X = pd.DataFrame([{
        "title": title,
        "location": location,
        "skills": " ".join(skills),
        "years_experience": years_experience,
    }])

    X_feat = builder.transform(X)
    pred = model.predict(X_feat)[0]
    return {
        "predicted_salary": round(float(pred), 2),
        "confidence_range": [round(pred * 0.85, 2), round(pred * 1.15, 2)],
    }

def predict_category(description: str) -> str:
    _load_models()
    vectorizer = _category_bundle["vectorizer"]
    model = _category_bundle["model"]
    X_vec = vectorizer.transform([description])
    return model.predict(X_vec)[0]