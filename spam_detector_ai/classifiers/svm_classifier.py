# spam_detector_ai/classifiers/svm_classifier.py
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import LinearSVC
from .base_classifier import BaseClassifier


class SVMClassifier(BaseClassifier):
    def __init__(self):
        super().__init__()
        self.vectoriser = TfidfVectorizer(**BaseClassifier.TFIDF_PARAMS)

    def train(self, X_train, y_train):
        X_train_vectorized = self.vectoriser.fit_transform(X_train)
        self.classifier = LinearSVC(C=1.0, max_iter=2000, random_state=0)
        self.classifier.fit(X_train_vectorized, y_train)

    def predict(self, texts):
        vectorized = self.vectoriser.transform(texts)
        return self.classifier.predict(vectorized)
