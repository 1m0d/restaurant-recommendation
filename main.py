import argparse
import logging
import pathlib
from datetime import datetime
from src.data_handler import create_dataset, process_data

from src.evaluate_models import evaluate_models
from src.models.logistic_regression_model import LogisticRegressionModel
from src.restaurant_recommender import RestaurantRecommender


def main():
    _setup_logging()
    args = _parse_arguments()

    if args.objective == "evaluate":
        evaluate_models(dataset_path=args.dataset_path)
    elif args.objective == "recommend":
        dataset = create_dataset(args.dataset_path)
        train_dataset, test_dataset = process_data(dataset)

        train_inputs = list(train_dataset.map(lambda _input, _: _input).as_numpy_iterator())
        train_labels = list(train_dataset.map(lambda _, label: label).as_numpy_iterator())
        test_inputs = list(test_dataset.map(lambda _input, _: _input).as_numpy_iterator())
        test_labels = list(test_dataset.map(lambda _, label: label).as_numpy_iterator())
        inputs = train_inputs + test_inputs
        labels = train_labels + test_labels

        classifier = LogisticRegressionModel(inputs, labels)
        RestaurantRecommender(classifier=classifier).run()


def _parse_arguments():
    parser = argparse.ArgumentParser(description="text classification")
    parser.add_argument(
        "objective",
        default='recommend',
        const='recommend',
        nargs='?',
        choices=['evaluate', 'recommend'],
        help="main objective of program run, defaults to recommend restaurant"
    )
    parser.add_argument(
        "--dataset_path",
        type=pathlib.Path,
        help="Path to dialog classification dataset",
        default="./dialog_acts.dat",
    )
    args = parser.parse_args()

    if not args.dataset_path.is_file():
        raise Exception(f"dialog dataset not found, {args.dataset_path=}")

    return args

def _setup_logging():
    logdir = "experiment_logs"
    pathlib.Path(logdir).mkdir(parents=True, exist_ok=True)
    date_time = datetime.now().strftime("%Y_%m_%d-%H_%M_%S")
    logging.basicConfig(
        handlers=[
            logging.FileHandler(f"{logdir}/experiment_{date_time}.log"),
            logging.StreamHandler(),
        ],
        encoding="utf-8",
        level=logging.INFO,
        format="[%(asctime)s] [%(levelname)s] %(message)s",
    )


if __name__ == "__main__":
    main()
