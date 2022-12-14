import logging

import sklearn.metrics

from src.data_handler import create_dataset, process_data
from src.models.decision_tree import DecisionTreeModel
from src.models.logistic_regression_model import LogisticRegressionModel
from src.models.majority_class_model import evaluate_majority_class
from src.models.rule_based_matching.rule_matcher import RuleMatcher


def evaluate_models(dataset_path: str):
    """Evaluate classifier models and log the results"""
    dataset = create_dataset(dataset_path)
    train_dataset, test_dataset = process_data(dataset)

    evaluate_majority_class(test_dataset)

    rule_matcher = RuleMatcher()
    test_input = list(test_dataset.map(lambda _input, _: _input).as_numpy_iterator())

    test_labels = list(test_dataset.map(lambda _, label: label).as_numpy_iterator())
    test_labels = [label.decode("utf-8") for label in test_labels]

    predicted_labels = rule_matcher.predict(test_input)

    logging.info("Classification Report for Rule Based Matching")
    logging.info(
        "\n" + sklearn.metrics.classification_report(test_labels, predicted_labels)
    )

    # logregression

    train_inputs = list(train_dataset.map(lambda _input, _: _input).as_numpy_iterator())
    train_labels = list(train_dataset.map(lambda _, label: label).as_numpy_iterator())

    log_regression_model = LogisticRegressionModel(
        train_inputs=train_inputs, train_labels=train_labels
    )

    test_features = log_regression_model.feature_extraction(dataset=test_input)
    predicted_labels = log_regression_model.model.predict(test_features)
    predicted_labels = [label.decode("utf-8") for label in predicted_labels]

    logging.info("Classification Report for LogisticRegressionModel")
    logging.info(
        "\n" + sklearn.metrics.classification_report(test_labels, predicted_labels)
    )

    # decision tree

    decision_tree_model = DecisionTreeModel(
        train_inputs=train_inputs, train_labels=train_labels
    )
    train_features = decision_tree_model.feature_extraction(dataset=train_inputs)

    test_features = decision_tree_model.feature_extraction(dataset=test_input)
    predicted_labels = decision_tree_model.model.predict(test_features)
    predicted_labels = [label.decode("utf-8") for label in predicted_labels]

    logging.info("Classification Report for DecisionTreeModel")
    logging.info(
        "\n" + sklearn.metrics.classification_report(test_labels, predicted_labels)
    )
