from typing import Iterable

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.tree import DecisionTreeClassifier


class DecisionTreeModel:
    def __init__(self, train_inputs: Iterable, train_labels: Iterable):
        self.count_vectorizer = CountVectorizer()
        self.count_vectorizer.fit(train_inputs)
        vectorized_inputs = self.count_vectorizer.transform(train_inputs)

        self.model = DecisionTreeClassifier().fit(vectorized_inputs, train_labels)

    def feature_extraction(self, dataset: Iterable):
        """Extract features for scoring"""
        return self.count_vectorizer.transform(dataset)

    def predict(self, feature_vector):
        """Predict class of featurized dialog input"""
        return self.model.predict(feature_vector)
