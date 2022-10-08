import logging
from typing import Iterable

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.linear_model import LogisticRegression


class LogisticRegressionModel:
    def __init__(self, train_inputs: Iterable, train_labels: Iterable):
        logging.info("Training Logistic Regression Model")
        self.model = LogisticRegression(max_iter=150)
        self.count_vectorizer = CountVectorizer()
        self.count_vectorizer.fit(train_inputs)

        train_features = self.feature_extraction(dataset=train_inputs)
        self.model.fit(train_features, train_labels)

    def feature_extraction(self, dataset: Iterable):
        """Extract features for scoring"""
        return self.count_vectorizer.transform(dataset)

    def predict(self, feature_vector):
        """Predict class of featurized dialog input"""
        return self.model.predict(feature_vector)
