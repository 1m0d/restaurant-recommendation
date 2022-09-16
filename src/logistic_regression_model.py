from typing import Iterable

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.linear_model import LogisticRegression


class LogisticRegressionModel:
    def __init__(self, train_inputs: Iterable):
        self.model = LogisticRegression()
        self.count_vectorizer = CountVectorizer()
        self.count_vectorizer.fit(train_inputs)

    def feature_extraction(self, dataset: Iterable):
        return self.count_vectorizer.transform(dataset)
