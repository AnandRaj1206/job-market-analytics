"""
Shared feature-building class for the salary model. Lives in its
own file (not train.py) so joblib pickles a stable, importable
reference (app.services.ml.feature_builder.SalaryFeatureBuilder)
instead of "__main__", which breaks when loaded from a different
entry point (e.g. the FastAPI server vs. the training script).
"""
from scipy.sparse import hstack, csr_matrix
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import OneHotEncoder
from sklearn.base import BaseEstimator, TransformerMixin


class SalaryFeatureBuilder(BaseEstimator, TransformerMixin):
    def __init__(self):
        self.title_vec = TfidfVectorizer(max_features=200)
        self.skills_vec = TfidfVectorizer(max_features=200)
        self.loc_enc = OneHotEncoder(handle_unknown="ignore")

    def fit(self, X, y=None):
        self.title_vec.fit(X["title"])
        self.skills_vec.fit(X["skills"])
        self.loc_enc.fit(X[["location"]])
        return self

    def transform(self, X):
        title_feat = self.title_vec.transform(X["title"])
        skills_feat = self.skills_vec.transform(X["skills"])
        loc_feat = self.loc_enc.transform(X[["location"]])
        years_feat = csr_matrix(X[["years_experience"]].to_numpy(dtype=float))
        return hstack([title_feat, skills_feat, loc_feat, years_feat])