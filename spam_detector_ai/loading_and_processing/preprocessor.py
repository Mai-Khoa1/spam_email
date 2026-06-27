# spam_detector_ai/loading_and_processing/preprocessor.py
import re
import unicodedata

VIETNAMESE_STOPWORDS = {
    'và', 'của', 'là', 'cho', 'với', 'có', 'trong', 'này', 'được', 'không',
    'đã', 'về', 'các', 'để', 'từ', 'tôi', 'bạn', 'anh', 'chị', 'em', 'ơi',
    'chúng', 'họ', 'đó', 'đây', 'thì', 'mà', 'nhưng', 'hay', 'hoặc', 'nếu',
    'khi', 'vì', 'nên', 'rằng', 'cũng', 'vẫn', 'sẽ', 'đang', 'rất', 'hơn',
    'nhất', 'như', 'theo', 'qua', 'tại', 'trên', 'dưới', 'sau', 'trước',
    'giữa', 'ngoài', 'bên', 'một', 'hai', 'ba', 'bốn', 'năm', 'sáu', 'bảy',
    'tám', 'chín', 'mười', 'thứ', 'cái', 'con', 'những', 'mọi', 'tất', 'cả',
    'nhiều', 'ít', 'vài', 'mấy', 'hãy', 'đừng', 'cần', 'phải', 'ạ', 'nhé',
    'nha', 'á', 'ừ', 'vâng', 'dạ', 'đến', 'lên', 'xuống', 'ra', 'vào', 'đi',
    'lại', 'còn', 'rồi', 'thôi', 'vậy', 'thế', 'được', 'bị', 'do', 'tự',
    'mình', 'ta', 'chúng', 'ta', 'ông', 'bà', 'cô', 'chú', 'bác', 'thầy',
    'cô', 'sẽ', 'đã', 'đang', 'sắp', 'vừa', 'mới', 'cũng', 'lại', 'còn',
}

ENGLISH_STOPWORDS = {
    'i', 'me', 'my', 'myself', 'we', 'our', 'ours', 'ourselves', 'you',
    'your', 'yours', 'yourself', 'yourselves', 'he', 'him', 'his', 'himself',
    'she', 'her', 'hers', 'herself', 'it', 'its', 'itself', 'they', 'them',
    'their', 'theirs', 'themselves', 'what', 'which', 'who', 'whom', 'this',
    'that', 'these', 'those', 'am', 'is', 'are', 'was', 'were', 'be', 'been',
    'being', 'have', 'has', 'had', 'having', 'do', 'does', 'did', 'doing',
    'a', 'an', 'the', 'and', 'but', 'if', 'or', 'because', 'as', 'until',
    'while', 'of', 'at', 'by', 'for', 'with', 'about', 'against', 'between',
    'into', 'through', 'during', 'before', 'after', 'above', 'below', 'to',
    'from', 'up', 'down', 'in', 'out', 'on', 'off', 'over', 'under', 'again',
    'further', 'then', 'once', 'here', 'there', 'when', 'where', 'why', 'how',
    'all', 'both', 'each', 'few', 'more', 'most', 'other', 'some', 'such',
    'no', 'nor', 'not', 'only', 'own', 'same', 'so', 'than', 'too', 'very',
    's', 't', 'can', 'will', 'just', 'should', 'now', 'd', 'll', 'm', 're',
    've', 'ain', 'also', 'would', 'could', 'may', 'might', 'shall', 'must',
    'need', 'dare', 'ought', 'used', 'like', 'get', 'got', 'let', 'go',
    'come', 'came', 'know', 'think', 'see', 'make', 'take', 'want', 'say',
    'said', 'hi', 'hello', 'dear', 'regards', 'sincerely', 'subject',
}

ALL_STOPWORDS = VIETNAMESE_STOPWORDS | ENGLISH_STOPWORDS

_URL_RE = re.compile(r'https?://\S+|www\.\S+', re.IGNORECASE)
_HTML_RE = re.compile(r'<[^>]+>')
_EMAIL_RE = re.compile(r'\S+@\S+\.\S+')
_PHONE_RE = re.compile(r'\b\d[\d\s\-\.]{7,}\d\b')
_SPECIAL_RE = re.compile(
    r'[^\w\sàáâãèéêìíòóôõùúýăđơưạảấầẩẫậắặẵẻẽếềệỉịọỏốồổỗộớờởỡợụủứừửữựỳỷỹ'
    r'ÀÁÂÃÈÉÊÌÍÒÓÔÕÙÚÝĂĐƠƯ]',
    re.UNICODE,
)
_MULTI_SPACE_RE = re.compile(r'\s+')


class Preprocessor:
    def preprocess_text(self, text: str) -> str:
        if not text or not text.strip():
            return ''
        text = unicodedata.normalize('NFC', text)
        text = _HTML_RE.sub(' ', text)
        text = _URL_RE.sub(' url ', text)
        text = _EMAIL_RE.sub(' email ', text)
        text = _PHONE_RE.sub(' phone ', text)
        text = text.lower()
        text = _SPECIAL_RE.sub(' ', text)
        tokens = text.split()
        tokens = [t for t in tokens if t not in ALL_STOPWORDS and len(t) > 1]
        return _MULTI_SPACE_RE.sub(' ', ' '.join(tokens)).strip()

    def preprocess(self, data):
        if 'text' not in data.columns:
            raise ValueError("DataFrame must contain a 'text' column")
        data = data.copy()
        data['processed_text'] = data['text'].apply(self.preprocess_text)
        return data
