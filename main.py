import logging
from datetime import datetime
from src.data_handler import create_dataset, process_data
from src.majority_class_model import evaluate_majority_class


def main():
    date_time = datetime.now().strftime("%Y_%m_%d-%H_%M_%S")
    logging.basicConfig(
        filename=f'experiment_logs/experiment_{date_time}.log',
        encoding='utf-8',
        level=logging.INFO,
        format="[%(asctime)s] [%(levelname)s] %(message)s",
    )

    dataset = create_dataset("../dialog_acts(1).dat")
    train_dataset, test_dataset = process_data(dataset)

    evaluate_majority_class(test_dataset)

if __name__ == '__main__':
    main()
