"""
Trains two models on collected postings:
1. Salary regressor (RandomForestRegressor)
2. Job category classifier (TF-IDF + LogisticRegression)
Run as a script: python -m app.services.ml.train
"""
import pandas as pd
import joblib
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import LogisticRegression
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from app.services.ml.feature_builder import SalaryFeatureBuilder


def train_salary_model(df: pd.DataFrame):
    df = df.dropna(subset=["salary_min", "salary_max"]).copy()
    df["salary_avg"] = (df["salary_min"] + df["salary_max"]) / 2
    df["years_experience"] = df["years_experience"].fillna(3.0)

    X = df[["title", "location", "skills", "years_experience"]]
    y = df["salary_avg"]

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    builder = SalaryFeatureBuilder()
    X_train_feat = builder.fit_transform(X_train)
    X_test_feat = builder.transform(X_test)

    model = RandomForestRegressor(n_estimators=200, random_state=42)
    model.fit(X_train_feat, y_train)
    print("Salary model R^2 on holdout:", model.score(X_test_feat, y_test))

    joblib.dump({"builder": builder, "model": model}, "salary_model.joblib")
    return builder, model


def train_category_model(df: pd.DataFrame):
    df = df.dropna(subset=["category", "description"])
    tfidf = TfidfVectorizer(max_features=500, stop_words="english")
    X_train, X_test, y_train, y_test = train_test_split(
        df["description"], df["category"], test_size=0.2, random_state=42
    )
    X_train_vec = tfidf.fit_transform(X_train)
    X_test_vec = tfidf.transform(X_test)

    clf = LogisticRegression(max_iter=1000)
    clf.fit(X_train_vec, y_train)
    print("Category model accuracy:", clf.score(X_test_vec, y_test))

    joblib.dump({"vectorizer": tfidf, "model": clf}, "category_model.joblib")
    return tfidf, clf


if __name__ == "__main__":
    from app.database import engine
    with engine.connect() as conn:
        df = pd.read_sql_table("job_postings", conn)
    train_salary_model(df)
    train_category_model(df)