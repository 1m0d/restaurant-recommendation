import argparse
import logging

import pathlib
from datetime import datetime

from src.data_handler import create_dataset, process_data
from src.dialog_handler import DialogHandler
from src.evaluate_models import evaluate_models
from src.keyword_matching import KeywordMatcher
from src.models.logistic_regression_model import LogisticRegressionModel
from src.models.decision_tree import DecisionTreeModel
from src.models.rule_based_matching.rule_matcher import RuleMatcher
from src.restaurant_recommender import RestaurantRecommender


def main():
    args = _parse_arguments()
    _setup_logging(is_debug=args.debug)
    if args.objective == "evaluate":
        evaluate_models(dataset_path=args.dataset_path)
    elif args.objective == "recommend":
        dataset = create_dataset(args.dataset_path)
        train_dataset, test_dataset = process_data(dataset)
        logging.info("Loading dataset")
        train_inputs = list(
            train_dataset.map(lambda _input, _: _input).as_numpy_iterator()
        )
        train_labels = list(
            train_dataset.map(lambda _, label: label).as_numpy_iterator()
        )
        test_inputs = list(
            test_dataset.map(lambda _input, _: _input).as_numpy_iterator()
        )
        test_labels = list(test_dataset.map(lambda _, label: label).as_numpy_iterator())
        inputs = train_inputs + test_inputs
        labels = train_labels + test_labels

        if args.classifier == "logregression" :
            classifier = LogisticRegressionModel(inputs, labels)
        elif args.classifier == "decisiontree":
            classifier = DecisionTreeModel(inputs, labels)
        elif args.classifier == "rulebased":
            classifier = RuleMatcher()
        
        DialogHandler.caps = args.capslock
        DialogHandler.delay = args.delay
        KeywordMatcher.distance = args.levenshtein

        RestaurantRecommender(classifier=classifier).run()


def _parse_arguments():
    parser = argparse.ArgumentParser(description="text classification")
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
        default="./dialog_acts.dat",
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
        choices=["logregression","decisiontree","rulebased"],
        help="set the dialog act classifier",
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


if __name__ == "__main__":
    main()
