from flask import Flask, request, jsonify, render_template
from spam_detector_ai.prediction.predict import VotingSpamDetector
import re
import joblib
import numpy as np
from pathlib import Path
from functools import lru_cache
from time import monotonic

app = Flask(__name__)
detector = VotingSpamDetector()

# Load logistic regression model và vectorizer để trích keyword
BASE_DIR = Path(__file__).parent / 'spam_detector_ai'
vec = joblib.load(BASE_DIR / 'models/logistic_regression/logistic_regression_vectoriser.joblib')
logreg = joblib.load(BASE_DIR / 'models/logistic_regression/logistic_regression_model.joblib')
feature_names = vec.get_feature_names_out()
coef = logreg.coef_[0]


def get_spam_keywords(text, top_n=10):
    """Trích top keyword spam từ text dựa trên Logistic Regression coef."""
    from spam_detector_ai.loading_and_processing.preprocessor import Preprocessor
    processed = Preprocessor().preprocess_text(text)
    tfidf_vec = vec.transform([processed]).toarray()[0]

    # Tính điểm = coef * tfidf_value cho từng từ
    scores = coef * tfidf_vec
    top_idx = np.argsort(scores)[::-1][:top_n]

    keywords = []
    for i in top_idx:
        if scores[i] > 0 and tfidf_vec[i] > 0:
            keywords.append(feature_names[i])

    return keywords


def translate_if_needed(text):
    """Chỉ dịch nếu phát hiện tiếng Việt."""
    vietnamese_pattern = re.compile(r'[àáâãèéêìíòóôõùúýăđơưạảấầẩẫậắặẵẻẽếềệỉịọỏốồổỗộớờởỡợụủứừửữựỳỷỹÀÁÂÃÈÉÊÌÍÒÓÔÕÙÚÝĂĐƠƯ]')
    if not vietnamese_pattern.search(text):
        return text, False

    try:
        return translate_cached(text, source='vi', target='en'), True
    except Exception:
        return text, False


@lru_cache(maxsize=256)
def translate_cached(text, source='vi', target='en'):
    from deep_translator import GoogleTranslator
    return GoogleTranslator(source=source, target=target).translate(text)


def build_alignment_chunks(text, window_sizes=(5, 3), max_chunks=12):
    """Create short original-language chunks so translated spam keywords can be mapped back."""
    chunks = []
    seen = set()

    for part in re.split(r'[.!?;:\n]+', text):
        words = list(re.finditer(r'\w+', part, flags=re.UNICODE))
        if not words:
            continue

        if len(words) <= max(window_sizes):
            start = words[0].start()
            end = words[-1].end()
            chunk = part[start:end].strip()
            key = chunk.lower()
            if chunk and key not in seen:
                chunks.append(chunk)
                seen.add(key)
            continue

        for window_size in window_sizes:
            if len(words) < window_size:
                continue
            for i in range(0, len(words) - window_size + 1):
                group = words[i:i + window_size]
                start = group[0].start()
                end = group[-1].end()
                chunk = part[start:end].strip()
                key = chunk.lower()
                if chunk and key not in seen:
                    chunks.append(chunk)
                    seen.add(key)
                if len(chunks) >= max_chunks:
                    return chunks

    return chunks


def reduce_overlapping_terms(terms, max_terms=5):
    selected = []

    for term in sorted(terms, key=lambda value: len(value), reverse=True):
        normalized = re.sub(r'\s+', ' ', term.lower()).strip()
        tokens = set(re.findall(r'\w+', normalized, flags=re.UNICODE))
        if not normalized:
            continue

        has_overlap = False
        for existing in selected:
            existing_normalized = re.sub(r'\s+', ' ', existing.lower()).strip()
            existing_tokens = set(re.findall(r'\w+', existing_normalized, flags=re.UNICODE))
            overlap_ratio = 0
            if tokens and existing_tokens:
                overlap_ratio = len(tokens.intersection(existing_tokens)) / min(len(tokens), len(existing_tokens))
            if normalized in existing_normalized or existing_normalized in normalized:
                has_overlap = True
                break
            if overlap_ratio >= 0.6:
                has_overlap = True
                break

        if not has_overlap:
            selected.append(term)

        if len(selected) >= max_terms:
            break

    return sorted(selected, key=lambda value: terms.index(value))


def align_keywords_to_original_text(original_text, english_keywords, time_budget=4.0):
    if not original_text or not english_keywords:
        return []

    highlight_terms = []
    seen_terms = set()
    keyword_tokens = set()

    for keyword in english_keywords:
        for token in re.findall(r'\w+', keyword.lower()):
            if len(token) > 2:
                keyword_tokens.add(token)

    if not keyword_tokens:
        return []

    deadline = monotonic() + time_budget
    for chunk in build_alignment_chunks(original_text):
        if monotonic() >= deadline or len(highlight_terms) >= 4:
            break

        try:
            translated_chunk = translate_cached(chunk).lower()
        except Exception:
            continue

        translated_tokens = set(re.findall(r'\w+', translated_chunk))
        if keyword_tokens.intersection(translated_tokens):
            key = chunk.lower()
            if key not in seen_terms:
                highlight_terms.append(chunk)
                seen_terms.add(key)

    return reduce_overlapping_terms(highlight_terms)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/check', methods=['POST'])
def check():
    data = request.get_json(silent=True) or {}
    text = data.get('text', '')
    subject = data.get('subject', '')
    if not text.strip():
        return jsonify({
            'error': 'Email text is required.',
            'is_spam': False,
            'votes': [],
            'weighted_score': 0.0,
            'translated': False,
            'model_keywords': [],
            'highlight_terms': [],
        }), 400

    translated_text, was_translated = translate_if_needed(text)
    translated_subject, _ = translate_if_needed(subject) if subject else (subject, False)

    full_text = f"subject: {translated_subject}. {translated_text}" if translated_subject else translated_text

    prediction = detector.predict_with_details(full_text)
    result = prediction['is_spam']
    votes = prediction['votes']
    weighted_score = prediction['weighted_score']

    # Trích keyword spam nếu là spam
    keywords = []
    highlight_terms = []
    if result:
        keywords = get_spam_keywords(full_text)
        if was_translated:
            highlight_terms = align_keywords_to_original_text(text, keywords)
        else:
            highlight_terms = keywords

    return jsonify({
        'is_spam': bool(result),
        'votes': votes,
        'weighted_score': float(weighted_score),
        'translated': was_translated,
        'model_keywords': keywords,
        'highlight_terms': highlight_terms,
    })


if __name__ == '__main__':
    print("Mo trinh duyet tai: http://localhost:5000")
    app.run(debug=False, port=5000, threaded=True)
