import logging
import os
import pathlib
from typing import Final

os.environ["TF_CPP_MIN_LOG_LEVEL"] = "3"
import tensorflow as tf

DATASET_SIZE: Final = 25501

SEED = 42
TRAIN_SPLIT = 0.85


def create_dataset(path: pathlib.Path):
    """create tensorflow dataset instance from path"""

    dataset = tf.data.TextLineDataset(
        path,
        compression_type=None,
        buffer_size=None,
        num_parallel_reads=None,
        name=None,
    )

    def separate_data(line):
        split_line = tf.strings.split(line, " ", maxsplit=1)
        label = split_line[0]
        input_text = split_line[1]
        return input_text, label

    return dataset.map(separate_data)


def _lowercase_input(input_text, label):
    return tf.strings.lower(input_text), label


def process_data(dataset):
    """Preprocess data before training"""

    logging.info(f"{SEED=}")
    logging.info(f"{TRAIN_SPLIT=}")

    dataset = dataset.map(_lowercase_input)

    # for some reason shuffle messes up label-data pairs
    #  dataset = dataset.shuffle(DATASET_SIZE, seed=SEED)

    train_dataset_size = int(TRAIN_SPLIT * DATASET_SIZE)
    test_dataset_size = DATASET_SIZE - train_dataset_size
    train_dataset = dataset.take(train_dataset_size)
    test_dataset = dataset.skip(train_dataset_size).take(test_dataset_size)

    return train_dataset, test_dataset
