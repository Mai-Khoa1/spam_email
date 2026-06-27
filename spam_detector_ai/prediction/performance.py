# performance.py - cập nhật tự động sau khi train

class ModelAccuracy:
    NAIVE_BAYES   = 1.0
    RANDOM_FOREST = 0.9524
    SVM           = 1.0
    LOGISTIC_REG  = 0.9762
    XGB           = 0.881

    @classmethod
    def total_accuracy(cls):
        return sum([cls.NAIVE_BAYES, cls.RANDOM_FOREST, cls.SVM, cls.LOGISTIC_REG, cls.XGB])
