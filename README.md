# spam-email

![Tests](https://github.com/Mai-Khoa1/spam_email/actions/workflows/tests.yml/badge.svg)
[![Current Release Version](https://img.shields.io/github/release/Mai-Khoa1/spam_email.svg?style=flat-square&logo=github)](https://github.com/Mai-Khoa1/spam_email/releases)
[![pypi Version](https://img.shields.io/pypi/v/spam-detector-ai.svg?style=flat-square&logo=pypi&logoColor=white)](https://pypi.org/project/spam-detector-ai/)


**spam-email** là một ứng dụng web phát hiện spam email sử dụng bỏ phiếu có trọng số từ 5 mô hình Machine Learning. Ứng dụng hỗ trợ cả tiếng Anh và tiếng Việt — văn bản tiếng Việt sẽ được tự động dịch sang tiếng Anh trước khi phân tích.

## Mục lục

- [Tính năng](#tính-năng)
- [Cài đặt](#cài-đặt)
- [Chạy ứng dụng](#chạy-ứng-dụng)
- [Cách sử dụng API](#cách-sử-dụng-api)
- [Cấu trúc dự án](#cấu-trúc-dự-án)
- [Huấn luyện mô hình](#huấn-luyện-mô-hình)
- [Kiểm thử](#kiểm-thử)
- [Cách hoạt động](#cách-hoạt-động)
- [Đóng góp](#đóng-góp)
- [Giấy phép](#giấy-phép)

---

## Tính năng

- Phân tích email bằng **5 mô hình ML**: Naive Bayes, Random Forest, SVM, Logistic Regression, XGBoost
- **Bỏ phiếu có trọng số** dựa trên độ chính xác của từng mô hình
- **Hỗ trợ tiếng Việt**: tự động phát hiện và dịch văn bản tiếng Việt
- **Tô sáng từ khoá spam** trực tiếp trên văn bản gốc (kể cả tiếng Việt)
- Giao diện web kéo-thả file và lịch sử kiểm tra
- API JSON đơn giản, dễ tích hợp

---

## Cài đặt

### Yêu cầu

- Python 3.10+
- Các thư viện trong `requirements.txt`

### Các bước

```bash
# 1. Clone hoặc giải nén dự án
git clone https://github.com/Mai-Khoa1/spam_email.git
cd spam-detection-project

# 2. Tạo môi trường ảo (khuyến nghị)
python3 -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate

# 3. Cài đặt thư viện
pip install -r requirements.txt
pip install flask deep-translator

# 4. Tải dữ liệu NLTK cần thiết
python3 -c "import nltk; nltk.download('wordnet'); nltk.download('stopwords')"
```

> **Lưu ý:** Dự án đã đi kèm 5 mô hình được huấn luyện sẵn trong thư mục `spam_detector_ai/models/`. Bạn có thể bỏ qua bước huấn luyện và chạy ứng dụng ngay.

---

## Chạy ứng dụng

```bash
python3 app.py
```

Mở trình duyệt tại: **http://localhost:5000**

---

## Cách sử dụng API

Ứng dụng cung cấp một endpoint duy nhất để kiểm tra spam.

### `POST /check`

**Request body (JSON):**

| Trường    | Bắt buộc | Mô tả                          |
|-----------|----------|--------------------------------|
| `text`    | ✅        | Nội dung email cần kiểm tra    |
| `subject` | ❌        | Tiêu đề email (tuỳ chọn)       |

**Ví dụ request:**

```bash
curl -X POST http://localhost:5000/check \
  -H "Content-Type: application/json" \
  -d '{"text": "Bạn đã trúng thưởng 100 triệu đồng!", "subject": "Thông báo trúng thưởng"}'
```

**Ví dụ response:**

```json
{
  "is_spam": true,
  "votes": [
    "Spam (Weight: 0.1822)",
    "Spam (Weight: 0.2047)",
    "Spam (Weight: 0.2052)",
    "Spam (Weight: 0.2039)",
    "Spam (Weight: 0.2039)"
  ],
  "weighted_score": 1.0,
  "translated": true,
  "model_keywords": ["win", "prize", "million"],
  "highlight_terms": ["trúng thưởng", "100 triệu"]
}
```

**Giải thích các trường response:**

| Trường            | Kiểu      | Mô tả                                                              |
|-------------------|-----------|--------------------------------------------------------------------|
| `is_spam`         | `bool`    | `true` nếu email là spam                                           |
| `votes`           | `list`    | Kết quả bỏ phiếu của từng mô hình kèm trọng số                    |
| `weighted_score`  | `float`   | Tổng điểm spam có trọng số (> 0.5 tổng trọng số = spam)           |
| `translated`      | `bool`    | `true` nếu văn bản gốc là tiếng Việt và đã được dịch              |
| `model_keywords`  | `list`    | Từ khoá spam trích xuất từ Logistic Regression (tiếng Anh)         |
| `highlight_terms` | `list`    | Cụm từ cần tô sáng trong văn bản gốc (tiếng Việt nếu đã dịch)     |

**Ví dụ Python:**

```python
import requests

response = requests.post(
    "http://localhost:5000/check",
    json={
        "text": "Congratulations! You've won a $1,000 gift card. Click here to claim.",
        "subject": "You're a winner!"
    }
)

data = response.json()
print(f"Is spam: {data['is_spam']}")
print(f"Weighted score: {data['weighted_score']:.4f}")
print(f"Keywords: {data['model_keywords']}")
```

**Ví dụ JavaScript:**

```javascript
const response = await fetch("http://localhost:5000/check", {
  method: "POST",
  headers: { "Content-Type": "application/json" },
  body: JSON.stringify({
    text: "Congratulations! You've won a $1,000 gift card.",
    subject: "You're a winner!"
  })
});

const data = await response.json();
console.log("Is spam:", data.is_spam);
console.log("Score:", data.weighted_score);
```

---

## Cấu trúc dự án

```
spam-detection-project/
├── app.py                          # Flask app: routes, dịch tiếng Việt, trích keyword
├── requirements.txt
├── static/
│   └── app.js                      # Frontend: giao diện, highlight từ khoá, lịch sử
├── templates/
│   └── index.html                  # Giao diện web chính
└── spam_detector_ai/
    ├── classifiers/
    │   ├── base_classifier.py      # Lớp cơ sở (TF-IDF vectorizer + predict)
    │   ├── classifier_types.py     # Enum: NAIVE_BAYES, RANDOM_FOREST, SVM, XGB, LOGISTIC_REGRESSION
    │   ├── naive_bayes_classifier.py
    │   ├── random_forest_classifier.py
    │   ├── svm_classifier.py
    │   ├── logistic_regression_classifier.py
    │   └── xgb_classifier.py       # Lưu/tải model bằng XGBoost native JSON
    ├── loading_and_processing/
    │   ├── data_loader.py          # Tải file CSV
    │   └── preprocessor.py        # Xoá ký tự đặc biệt, lowercase, stopwords, lemmatize
    ├── models/
    │   ├── bayes/                  # naive_bayes_model.joblib + vectoriser
    │   ├── random_forest/          # random_forest_model.joblib + vectoriser
    │   ├── svm/                    # svm_model.joblib + vectoriser
    │   ├── logistic_regression/    # logistic_regression_model.joblib + vectoriser
    │   └── xgb/                   # xgb_model.json + vectoriser + label_encoder
    ├── prediction/
    │   ├── performance.py          # Độ chính xác của từng mô hình (dùng tính trọng số)
    │   └── predict.py             # SpamDetector, VotingSpamDetector
    ├── training/
    │   └── train_models.py        # ModelTrainer: load, preprocess, train, save
    ├── tuning/                    # Fine-tuning LR, SVM, XGB
    ├── tests/                     # Test scripts
    ├── data/
    │   └── spam.csv               # Dữ liệu huấn luyện (label, text, label_num)
    ├── logger_config.py
    └── trainer.py                 # Script huấn luyện tất cả mô hình
```

---

## Huấn luyện mô hình

> Dự án đã có sẵn mô hình huấn luyện sẵn. Chỉ cần huấn luyện lại nếu bạn muốn dùng dữ liệu mới.

File dữ liệu phải là CSV với 3 cột: `label` (`ham`/`spam`), `text`, `label_num` (`0`/`1`).

```bash
python3 spam_detector_ai/trainer.py
```

Lệnh này huấn luyện tất cả 5 mô hình và lưu vào các thư mục con của `spam_detector_ai/models/`.

> ⚠️ Nếu gặp lỗi `ModuleNotFoundError`, hãy chạy từ thư mục gốc của dự án hoặc dùng IDE.

---

## Kiểm thử

```bash
python3 spam_detector_ai/tests/test.py
```

### Kết quả các mô hình

#### Naive Bayes — Accuracy: 0.8679

| | Dự đoán: Ham | Dự đoán: Spam |
|---|---|---|
| **Thực tế: Ham** | 1935 (TN) | 170 (FP) |
| **Thực tế: Spam** | 221 (FN) | 633 (TP) |

| | Precision | Recall | F1 | Support |
|---|---|---|---|---|
| Ham | 0.90 | 0.92 | 0.91 | 2105 |
| Spam | 0.79 | 0.74 | 0.76 | 854 |
| **Tổng** | | | **0.87** | 2959 |

#### Random Forest — Accuracy: 0.9750

| | Dự đoán: Ham | Dự đoán: Spam |
|---|---|---|
| **Thực tế: Ham** | 2067 (TN) | 38 (FP) |
| **Thực tế: Spam** | 36 (FN) | 818 (TP) |

| | Precision | Recall | F1 | Support |
|---|---|---|---|---|
| Ham | 0.98 | 0.98 | 0.98 | 2105 |
| Spam | 0.96 | 0.96 | 0.96 | 854 |
| **Tổng** | | | **0.97** | 2959 |

#### SVM — Accuracy: 0.9774

| | Dự đoán: Ham | Dự đoán: Spam |
|---|---|---|
| **Thực tế: Ham** | 2080 (TN) | 25 (FP) |
| **Thực tế: Spam** | 41 (FN) | 813 (TP) |

| | Precision | Recall | F1 | Support |
|---|---|---|---|---|
| Ham | 0.98 | 0.99 | 0.98 | 2105 |
| Spam | 0.97 | 0.95 | 0.96 | 854 |
| **Tổng** | | | **0.98** | 2959 |

#### Logistic Regression — Accuracy: 0.9708

| | Dự đoán: Ham | Dự đoán: Spam |
|---|---|---|
| **Thực tế: Ham** | 2065 (TN) | 48 (FP) |
| **Thực tế: Spam** | 46 (FN) | 989 (TP) |

| | Precision | Recall | F1 | Support |
|---|---|---|---|---|
| Ham | 0.98 | 0.98 | 0.98 | 2113 |
| Spam | 0.95 | 0.96 | 0.95 | 1035 |
| **Tổng** | | | **0.97** | 3148 |

#### XGBoost — Accuracy: 0.9711

| | Dự đoán: Ham | Dự đoán: Spam |
|---|---|---|
| **Thực tế: Ham** | 2050 (TN) | 63 (FP) |
| **Thực tế: Spam** | 28 (FN) | 1007 (TP) |

| | Precision | Recall | F1 | Support |
|---|---|---|---|---|
| Ham | 0.99 | 0.97 | 0.98 | 2113 |
| Spam | 0.94 | 0.97 | 0.96 | 1035 |
| **Tổng** | | | **0.97** | 3148 |

---

## Cách hoạt động

### Bỏ phiếu có trọng số (`VotingSpamDetector`)

Mỗi mô hình bỏ phiếu spam/ham và được nhân với trọng số tỉ lệ thuận với độ chính xác:

| Mô hình | Accuracy | Trọng số |
|---|---|---|
| Naive Bayes | 0.8679 | 0.1822 |
| Random Forest | 0.9750 | 0.2047 |
| SVM | 0.9774 | 0.2052 |
| Logistic Regression | 0.9708 | 0.2039 |
| XGBoost | 0.9711 | 0.2039 |

Nếu tổng điểm spam có trọng số vượt quá 50% tổng trọng số → phân loại là **Spam**.

### Hỗ trợ tiếng Việt

1. Phát hiện ký tự tiếng Việt bằng regex unicode
2. Dịch toàn bộ text sang tiếng Anh qua `deep_translator.GoogleTranslator`
3. Chạy phân tích trên bản tiếng Anh
4. Nếu là spam: trích keyword từ Logistic Regression, sau đó dịch ngược từng chunk nhỏ để tìm lại cụm từ tương ứng trong văn bản tiếng Việt gốc → trả về `highlight_terms`

### Tiền xử lý văn bản (`Preprocessor`)

1. Xoá tất cả ký tự không phải chữ cái (`[^a-zA-Z]`)
2. Chuyển về chữ thường
3. Loại bỏ stopwords tiếng Anh (NLTK)
4. Lemmatize bằng `WordNetLemmatizer`

### TF-IDF Vectorizer (dùng chung cho tất cả mô hình)

```python
TfidfVectorizer(max_features=1500, min_df=5, max_df=0.7, ngram_range=(1, 2))
```

### Lưu trữ mô hình

- Tất cả mô hình dùng `joblib` để lưu (`.joblib`)
- Riêng XGBoost lưu weights bằng định dạng native JSON (`.json`) và label encoder riêng

---

## Đóng góp

Xem hướng dẫn đóng góp tại [CONTRIBUTING.md](CONTRIBUTING.md).

---

## Giấy phép

Dự án được cấp phép theo [MIT License](LICENSE).