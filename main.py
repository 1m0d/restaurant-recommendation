from typing import Final
import tensorflow as tf


DATASET_SIZE: Final = 25501

SEED: Final = 42
TRAIN_SPLIT: Final = 0.85


def load_data(path: str):
    dataset = tf.data.TextLineDataset(
        path,
        compression_type=None,
        buffer_size=None,
        num_parallel_reads=None,
        name=None
    )

    def separate_data(line):
        split_line = tf.strings.split(line, " ", maxsplit=1)
        label = split_line[0]
        input_text = split_line[1]
        return input_text, label

    return dataset.map(separate_data)

def lowercase_input(input_text, label):
    return tf.strings.lower(input_text), label

def process_data(dataset):
    dataset = dataset.map(lowercase_input)
    dataset = dataset.shuffle(DATASET_SIZE, seed=SEED)

    train_dataset_size = int(TRAIN_SPLIT * DATASET_SIZE)
    test_dataset_size = DATASET_SIZE - train_dataset_size
    train_dataset = dataset.take(train_dataset_size)
    test_dataset = dataset.skip(train_dataset_size).take(test_dataset_size)

    return train_dataset, test_dataset


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


dataset = load_data("../dialog_acts(1).dat")
train_dataset, test_dataset = process_data(dataset)
evaluate_majority_class(test_dataset)
