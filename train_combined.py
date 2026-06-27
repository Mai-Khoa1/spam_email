"""
Train tất cả mô hình trên dataset song ngữ Anh-Việt.
Chạy: python train_combined.py
"""
import sys
from pathlib import Path

project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix

from spam_detector_ai.classifiers.classifier_types import ClassifierType
from spam_detector_ai.logger_config import init_logging
from spam_detector_ai.training.train_models import ModelTrainer

logger = init_logging()

DATA_PATH = str(project_root / 'spam_detector_ai' / 'data' / 'spam_combined.csv')

CONFIGS = [
    (ClassifierType.NAIVE_BAYES,         'naive_bayes_model.joblib',         'naive_bayes_vectoriser.joblib'),
    (ClassifierType.LOGISTIC_REGRESSION, 'logistic_regression_model.joblib', 'logistic_regression_vectoriser.joblib'),
    (ClassifierType.SVM,                 'svm_model.joblib',                 'svm_vectoriser.joblib'),
    (ClassifierType.RANDOM_FOREST,       'random_forest_model.joblib',       'random_forest_vectoriser.joblib'),
    (ClassifierType.XGB,                 'xgb_model.json',                   'xgb_vectoriser.joblib'),
]

accuracies = {}


def train_and_evaluate(ct, model_file, vec_file, X_train, y_train, X_test, y_test):
    logger.info(f'\n=== Training {ct.name} ===')
    trainer = ModelTrainer(data=None, classifier_type=ct, logger=logger)
    trainer.train(X_train, y_train)
    trainer.save_model(model_file, vec_file)

    y_pred = trainer.classifier.predict(X_test.tolist())
    acc = accuracy_score(y_test, y_pred)
    logger.info(f'{ct.name} Accuracy: {acc:.4f}')
    print(f'\n--- {ct.name} ---')
    print(confusion_matrix(y_test, y_pred))
    print(classification_report(y_test, y_pred))
    return acc


if __name__ == '__main__':
    logger.info(f'Loading dataset: {DATA_PATH}')
    initial = ModelTrainer(data_path=DATA_PATH, logger=logger)
    processed = initial.preprocess_data_()

    logger.info(f'Dataset size: {len(processed)} samples')
    logger.info(f'Label distribution:\n{processed["label"].value_counts()}')

    X_train, X_test, y_train, y_test = train_test_split(
        processed['processed_text'], processed['label'],
        test_size=0.2, random_state=42, stratify=processed['label']
    )
    logger.info(f'Train: {len(X_train)}, Test: {len(X_test)}')

    for ct, mf, vf in CONFIGS:
        try:
            acc = train_and_evaluate(ct, mf, vf, X_train, y_train, X_test, y_test)
            accuracies[ct.name] = round(acc, 4)
        except Exception as e:
            logger.error(f'Failed {ct.name}: {e}')
            accuracies[ct.name] = 0.0

    print('\n===== KET QUA =====')
    for name, acc in sorted(accuracies.items(), key=lambda x: x[1], reverse=True):
        print(f'{name:30s}: {acc:.4f} ({acc*100:.2f}%)')

    best = max(accuracies, key=accuracies.get)
    print(f'\nMo hinh tot nhat: {best} ({accuracies[best]*100:.2f}%)')

    # Cập nhật performance.py
    perf_path = project_root / 'spam_detector_ai' / 'prediction' / 'performance.py'
    nb  = accuracies.get('NAIVE_BAYES', 0.97)
    rf  = accuracies.get('RANDOM_FOREST', 0.97)
    svm = accuracies.get('SVM', 0.98)
    lr  = accuracies.get('LOGISTIC_REGRESSION', 0.98)
    xgb = accuracies.get('XGB', 0.96)
    perf_path.write_text(
        f"# performance.py - cap nhat tu dong sau khi train\n\n"
        f"class ModelAccuracy:\n"
        f"    NAIVE_BAYES   = {nb}\n"
        f"    RANDOM_FOREST = {rf}\n"
        f"    SVM           = {svm}\n"
        f"    LOGISTIC_REG  = {lr}\n"
        f"    XGB           = {xgb}\n\n"
        f"    @classmethod\n"
        f"    def total_accuracy(cls):\n"
        f"        return sum([cls.NAIVE_BAYES, cls.RANDOM_FOREST, cls.SVM, cls.LOGISTIC_REG, cls.XGB])\n",
        encoding='utf-8'
    )
    logger.info('performance.py updated.')
