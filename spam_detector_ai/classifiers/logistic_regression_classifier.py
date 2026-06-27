# spam_detector_ai/classifiers/logistic_regression_classifier.py
from sklearn.linear_model import LogisticRegression
from sklearn.feature_extraction.text import TfidfVectorizer
from .base_classifier import BaseClassifier


class LogisticRegressionSpamClassifier(BaseClassifier):
    def __init__(self):
        super().__init__()
        self.vectoriser = TfidfVectorizer(**BaseClassifier.TFIDF_PARAMS)

    def train(self, X_train, y_train):
        X_train_vectorized = self.vectoriser.fit_transform(X_train)
        self.classifier = LogisticRegression(C=5, max_iter=500, penalty='l2', solver='saga', random_state=0)
        self.classifier.fit(X_train_vectorized, y_train)

    def predict(self, texts):
        vectorized = self.vectoriser.transform(texts)
        return self.classifier.predict(vectorized)
