import logging
from datetime import datetime
from src.data_handler import create_dataset, process_data
from src.decision_tree import DecisionTreeModel
from src.majority_class_model import evaluate_majority_class
from src.logistic_regression_model import LogisticRegressionModel
from src.rule_based_matching.rule_matcher import RuleMatcher
import sklearn.metrics


def main():
    date_time = datetime.now().strftime("%Y_%m_%d-%H_%M_%S")
    logging.basicConfig(
        handlers=[
            logging.FileHandler(f"experiment_logs/experiment_{date_time}.log"),
            logging.StreamHandler(),
        ],
        encoding="utf-8",
        level=logging.INFO,
        format="[%(asctime)s] [%(levelname)s] %(message)s",
    )

    dataset = create_dataset("../dialog_acts(1).dat")
    train_dataset, test_dataset = process_data(dataset)

    evaluate_majority_class(test_dataset)

    rule_matcher = RuleMatcher()
    test_input = list(test_dataset.map(lambda _input, _: _input).as_numpy_iterator())

    test_labels = list(test_dataset.map(lambda _, label: label).as_numpy_iterator())
    test_labels = [label.decode("utf-8") for label in test_labels]

    predicted_labels = rule_matcher.predict(test_input)

    logging.info("Classification Report for Rule Based Matching")
    logging.info("\n" + sklearn.metrics.classification_report(test_labels, predicted_labels))

    # logregression

    train_inputs = list(train_dataset.map(lambda _input, _: _input).as_numpy_iterator())
    train_labels = list(train_dataset.map(lambda _, label: label).as_numpy_iterator())

    log_regression_model = LogisticRegressionModel(train_inputs=train_inputs)
    train_features = log_regression_model.feature_extraction(dataset=train_inputs)
    log_regression_model.model.fit(train_features, train_labels)

    test_features = log_regression_model.feature_extraction(dataset=test_input)
    predicted_labels = log_regression_model.model.predict(test_features)
    predicted_labels = [label.decode("utf-8") for label in predicted_labels]

    logging.info("Classification Report for LogisticRegressionModel")
    logging.info("\n" + sklearn.metrics.classification_report(test_labels, predicted_labels))

    # decision tree

    decision_tree_model = DecisionTreeModel(train_inputs=train_inputs, train_labels=train_labels)
    train_features = decision_tree_model.feature_extraction(dataset=train_inputs)

    test_features = decision_tree_model.feature_extraction(dataset=test_input)
    predicted_labels = decision_tree_model.model.predict(test_features)
    predicted_labels = [label.decode("utf-8") for label in predicted_labels]

    logging.info("Classification Report for DecisionTreeModel")
    logging.info("\n" + sklearn.metrics.classification_report(test_labels, predicted_labels))

if __name__ == '__main__':
    main()
