# Hướng dẫn đóng góp cho spam-email

Cảm ơn bạn đã quan tâm đến việc đóng góp cho dự án! Mọi đóng góp — dù lớn hay nhỏ — đều được chào đón và đánh giá cao.

Vui lòng đọc kỹ hướng dẫn này trước khi bắt đầu.

## Quy tắc ứng xử

Khi tham gia dự án, bạn đồng ý tuân thủ [Quy tắc ứng xử](./CODE_OF_CONDUCT.md).

---

## Bắt đầu

### 1. Fork và clone

```bash
# Fork repository trên GitHub, sau đó clone về máy
git clone https://github.com/<tên-của-bạn>/spam_email.git
cd spam-detection-project

# Thêm remote upstream để theo dõi repo gốc
git remote add upstream https://github.com/Mai-Khoa1/spam_email.git
```

### 2. Cài đặt môi trường

```bash
python3 -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate

pip install -r requirements.txt
pip install flask deep-translator

python3 -c "import nltk; nltk.download('wordnet'); nltk.download('stopwords')"
```

### 3. Chạy ứng dụng để kiểm tra

```bash
python3 app.py
# Mở http://localhost:5000
```

---

## Quy trình đóng góp

### 1. Đồng bộ với repo gốc

```bash
git fetch upstream
git checkout main
git merge upstream/main
```

### 2. Tạo branch mới

```bash
git checkout -b ten-tinh-nang-hoac-fix
```

Đặt tên branch rõ ràng, ví dụ:
- `feature/support-english-subject-detection`
- `fix/highlight-overlap-bug`
- `refactor/preprocessor-cleanup`

### 3. Thực hiện thay đổi

Xem phần [Hướng dẫn code](#hướng-dẫn-code) bên dưới.

### 4. Kiểm thử

```bash
# Chạy test
python3 spam_detector_ai/tests/test.py

# Kiểm tra API thủ công
python3 app.py &
curl -X POST http://localhost:5000/check \
  -H "Content-Type: application/json" \
  -d '{"text": "Congratulations you won a prize", "subject": "Winner"}'
```

### 5. Commit và push

```bash
git add .
git commit -m "Mô tả ngắn gọn thay đổi"
git push origin ten-tinh-nang-hoac-fix
```

### 6. Tạo Pull Request

Vào [trang repo gốc](https://github.com/Mai-Khoa1/spam_email) và nhấn **New pull request**.

---

## Hướng dẫn code

### Cấu trúc chính cần nắm

| File | Vai trò |
|---|---|
| `app.py` | Flask routes, dịch tiếng Việt, trích keyword |
| `spam_detector_ai/prediction/predict.py` | `SpamDetector`, `VotingSpamDetector` |
| `spam_detector_ai/classifiers/base_classifier.py` | Lớp cơ sở cho tất cả classifier |
| `spam_detector_ai/loading_and_processing/preprocessor.py` | Tiền xử lý văn bản |
| `spam_detector_ai/prediction/performance.py` | Accuracy của từng mô hình (tính trọng số) |
| `static/app.js` | Frontend JavaScript |

### Thêm classifier mới

1. Tạo file trong `spam_detector_ai/classifiers/`, kế thừa `BaseClassifier`
2. Implement method `train(self, X_train, y_train)`
3. Thêm giá trị mới vào `ClassifierType` enum trong `classifier_types.py`
4. Đăng ký trong `VotingSpamDetector.__init__()` tại `predict.py` với accuracy tương ứng
5. Thêm accuracy vào `ModelAccuracy` trong `performance.py`
6. Thêm đường dẫn model vào `get_model_path()` trong `predict.py`

### Quy tắc code

- Tuân theo [PEP 8](https://pep8.org/)
- Docstring cho mọi class và method public
- Không commit file `.pyc`, model `.joblib`/`.json`, hay file log

### Cập nhật model

Nếu bạn huấn luyện lại model với dữ liệu mới:
- Cập nhật accuracy trong `spam_detector_ai/prediction/performance.py`
- Ghi lại kết quả confusion matrix và metrics trong README
- Không commit file model vào repository (chúng quá lớn)

---

## Báo cáo lỗi

Tạo issue trên GitHub với thông tin:

- **Mô tả lỗi**: Chuyện gì xảy ra?
- **Các bước tái hiện**: Làm thế nào để tái hiện lỗi?
- **Kết quả mong đợi**: Nên xảy ra điều gì?
- **Môi trường**: Python version, OS, các package liên quan

---

## Đề xuất tính năng

Tạo issue với nhãn `feature request`, mô tả:

- Tính năng là gì?
- Tại sao nó hữu ích?
- Cách triển khai đề xuất (nếu có)

---

## Cảm ơn!

Mọi đóng góp của bạn đều giúp dự án tốt hơn. Cảm ơn vì đã dành thời gian!