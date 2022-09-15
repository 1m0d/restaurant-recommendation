from src.data_handler import create_dataset, process_data


def score_input_majority_class(_input_text):
    return "inform"


def evaluate_majority_class(test_dataset):
    correct = 0
    incorrect = 0

    for input_text, label in test_dataset:
        prediction = score_input_majority_class(input_text)
        if prediction == label:
            correct += 1
        else:
            incorrect += 1

    accuracy = correct / (correct + incorrect)
    print(f"Accuracy for majority class model: {(accuracy * 100):.2f}%")


dataset = create_dataset("../dialog_acts(1).dat")
train_dataset, test_dataset = process_data(dataset)
evaluate_majority_class(test_dataset)
