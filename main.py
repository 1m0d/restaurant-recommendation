import argparse
import logging
import pathlib
from datetime import datetime

from src.evaluate_models import evaluate_models


def main():
    _setup_logging()
    args = _parse_arguments()

    if args.objective == "evaluate":
        evaluate_models(dataset_path=args.dataset_path)
    elif args.objective == "recommend":
        pass


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
