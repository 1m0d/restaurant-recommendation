import argparse
import logging
import pathlib
import pickle
from datetime import datetime

from src.data_handler import create_dataset, process_data
from src.dialog_handler import DialogHandler
from src.evaluate_models import evaluate_models
from src.keyword_matching import KeywordMatcher
from src.models.decision_tree import DecisionTreeModel
from src.models.logistic_regression_model import LogisticRegressionModel
from src.models.rule_based_matching.rule_matcher import RuleMatcher
from src.restaurant_recommender import RestaurantRecommender


def main():
    args = _parse_arguments()
    _setup_logging(is_debug=args.debug)
    if args.objective == "evaluate":
        evaluate_models(dataset_path=args.dataset_path)
    elif args.objective == "recommend":
        classifier = _train_classifier_model(
            dataset_path=args.dataset_path,
            pretrained_model_path=args.pretrained_model_path,
            classifier_type=args.classifier,
            save_model_path=args.save_model_path,
        )
        DialogHandler.caps = args.capslock
        DialogHandler.delay = args.delay
        KeywordMatcher.distance = args.levenshtein

        RestaurantRecommender(classifier=classifier).run()


def _parse_arguments():
    parser = argparse.ArgumentParser(
        description="Restaurant Recommendation System",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument(
        "objective",
        default="recommend",
        const="recommend",
        nargs="?",
        choices=["evaluate", "recommend"],
        help="main objective of program run, defaults to recommend restaurant",
    )
    parser.add_argument(
        "--dataset_path",
        type=pathlib.Path,
        help="path to dialog classification dataset",
        default="./datafiles/dialog_acts.dat",
    )
    parser.add_argument(
        "--debug",
        const="debug",
        help="set loglevel to Debug",
        nargs="?",
    )
    parser.add_argument(
        "--capslock",
        const=True,
        default=False,
        help="print all system utterances in uppercase",
        nargs="?",
    )
    parser.add_argument(
        "--delay",
        const=True,
        default=False,
        help="enable variable system delay",
        nargs="?",
    )
    parser.add_argument(
        "--levenshtein",
        type=int,
        help="set the levenshtein distance",
        default=3,
    )
    parser.add_argument(
        "--classifier",
        default="logregression",
        const="logregression",
        nargs="?",
        choices=["logregression", "decisiontree", "rulebased"],
        help="set the dialog act classifier",
    )
    parser.add_argument(
        "--pretrained_model_path",
        type=pathlib.Path,
        help=("path to pretrained model, to use for restaurant recommendation"),
    )
    parser.add_argument(
        "--save_model_path",
        type=pathlib.Path,
        help="path to save classification model after training",
    )
    args = parser.parse_args()

    if not args.dataset_path.is_file():
        raise Exception(f"dialog dataset not found, {args.dataset_path=}")

    return args


def _setup_logging(is_debug=False):
    if is_debug:
        loglevel = logging.DEBUG
    else:
        loglevel = logging.INFO

    logdir = "experiment_logs"
    pathlib.Path(logdir).mkdir(parents=True, exist_ok=True)
    date_time = datetime.now().strftime("%Y_%m_%d-%H_%M_%S")
    logging.basicConfig(
        handlers=[
            logging.FileHandler(f"{logdir}/experiment_{date_time}.log"),
            logging.StreamHandler(),
        ],
        encoding="utf-8",
        level=loglevel,
        format="[%(asctime)s] [%(levelname)s] %(message)s",
    )


def _train_classifier_model(
    dataset_path: pathlib.Path,
    pretrained_model_path: pathlib.Path,
    classifier_type: str,
    save_model_path: pathlib.Path,
):

    if pretrained_model_path and pretrained_model_path.is_file():
        with open(pretrained_model_path, "rb") as file:
            classifier = pickle.load(file)

        return classifier

    dataset = create_dataset(dataset_path)
    train_dataset, test_dataset = process_data(dataset)
    logging.info("Loading dataset")
    train_inputs = list(train_dataset.map(lambda _input, _: _input).as_numpy_iterator())
    train_labels = list(train_dataset.map(lambda _, label: label).as_numpy_iterator())
    test_inputs = list(test_dataset.map(lambda _input, _: _input).as_numpy_iterator())
    test_labels = list(test_dataset.map(lambda _, label: label).as_numpy_iterator())
    inputs = train_inputs + test_inputs
    labels = train_labels + test_labels

    if classifier_type == "logregression":
        classifier = LogisticRegressionModel(inputs, labels)
    elif classifier_type == "decisiontree":
        classifier = DecisionTreeModel(inputs, labels)
    elif classifier_type == "rulebased":
        classifier = RuleMatcher()
    else:
        raise Exception(f"Unknown classifier type set. {classifier_type=}")

    if save_model_path:
        with open(save_model_path, "wb") as file:
            pickle.dump(classifier, file)

    return classifier


if __name__ == "__main__":
    main()
