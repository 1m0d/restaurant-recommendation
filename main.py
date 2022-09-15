from src.data_handler import create_dataset, process_data
from src.majority_class_model import evaluate_majority_class


dataset = create_dataset("../dialog_acts(1).dat")
train_dataset, test_dataset = process_data(dataset)

evaluate_majority_class(test_dataset)
