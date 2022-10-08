import logging


def score_input_majority_class(_input_text):
    return "inform"


def evaluate_majority_class(test_dataset):
    """
    Calculate accuracy for majority class model
    """
    correct = 0
    incorrect = 0

    for input_text, label in test_dataset:
        prediction = score_input_majority_class(input_text)
        if prediction == label:
            correct += 1
        else:
            incorrect += 1

    accuracy = correct / (correct + incorrect)
    logging.info(f"Accuracy for majority class model: {(accuracy * 100):.2f}%")
