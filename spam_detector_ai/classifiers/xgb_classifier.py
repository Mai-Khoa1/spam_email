# spam_detector_ai/classifiers/xgb_classifier.py
# XGBoost không build được trong môi trường này → dùng GradientBoostingClassifier từ sklearn
from joblib import dump, load
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.feature_extraction.text import TfidfVectorizer
from .base_classifier import BaseClassifier


class XGBSpamClassifier(BaseClassifier):
    def __init__(self):
        super().__init__()
        self.vectoriser = TfidfVectorizer(**BaseClassifier.TFIDF_PARAMS)

    def train(self, X_train, y_train):
        X_train_vectorized = self.vectoriser.fit_transform(X_train)
        self.classifier = GradientBoostingClassifier(
            n_estimators=200,
            learning_rate=0.1,
            max_depth=4,
            random_state=0,
        )
        self.classifier.fit(X_train_vectorized.toarray(), y_train)

    def save_model(self, model_path, vectoriser_path):
        # GradientBoosting dùng joblib, đổi extension .json → .joblib
        actual_path = model_path.replace('.json', '.joblib')
        dump(self.classifier, actual_path)
        dump(self.vectoriser, vectoriser_path)

    def load_model(self, model_path, vectoriser_path):
        actual_path = model_path.replace('.json', '.joblib')
        self.classifier = load(actual_path)
        self.vectoriser = load(vectoriser_path)

    def predict(self, texts):
        vectorized = self.vectoriser.transform(texts).toarray()
        return self.classifier.predict(vectorized)
