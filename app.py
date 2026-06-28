import re
from pathlib import Path

import joblib
import numpy as np
from flask import Flask, jsonify, render_template, request
from flask_cors import CORS

from spam_detector_ai.loading_and_processing.preprocessor import Preprocessor
from spam_detector_ai.prediction.predict import VotingSpamDetector

app = Flask(__name__)
CORS(app)
detector = VotingSpamDetector()


BASE_DIR = Path(__file__).parent / 'spam_detector_ai'
_preprocessor = Preprocessor()

_vec    = joblib.load(BASE_DIR / 'models/logistic_regression/logistic_regression_vectoriser.joblib')
_logreg = joblib.load(BASE_DIR / 'models/logistic_regression/logistic_regression_model.joblib')
_feature_names = _vec.get_feature_names_out()
_coef = _logreg.coef_[0]


def get_spam_keywords(text: str, top_n: int = 10) -> list[str]:
    processed = _preprocessor.preprocess_text(text)
    tfidf_vec = _vec.transform([processed]).toarray()[0]
    scores = _coef * tfidf_vec
    top_idx = np.argsort(scores)[::-1][:top_n]
    return [_feature_names[i] for i in top_idx if scores[i] > 0 and tfidf_vec[i] > 0]


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/predict', methods=['POST'])
@app.route('/check', methods=['POST'])
def check():
    data = request.get_json(silent=True) or {}
    text = data.get('text', '').strip()
    subject = data.get('subject', '').strip()

    if not text:
        return jsonify({
            'error': 'Vui lòng nhập nội dung cần kiểm tra.',
            'is_spam': False,
            'votes': [],
            'weighted_score': 0.0,
            'model_keywords': [],
            'highlight_terms': [],
        }), 400

    full_text = f"subject: {subject}. {text}" if subject else text

    prediction = detector.predict_with_details(full_text)
    is_spam = prediction['is_spam']
    keywords = get_spam_keywords(full_text) if is_spam else []

    return jsonify({
        'is_spam': bool(is_spam),
        'input_text': full_text,
        'votes': prediction['votes'],
        'weighted_score': float(prediction['weighted_score']),
        'model_keywords': keywords,
        'highlight_terms': keywords,
        'prediction': 'Spam' if is_spam else 'Không Spam',
        'confidence': round(float(prediction['weighted_score']) * 100, 1),
        'model': 'Weighted Voting (5 mô hình)',
    })


if __name__ == '__main__':
    print('Mo trinh duyet tai: http://localhost:5000')
    app.run(debug=False, port=5000, threaded=True)
