from collections.abc import Iterable
import csv
import os
import re
from typing import Final, Union

from tensorflow.python.util.lazy_loader import logging

from src.majority_class_model import score_input_majority_class

dirname = os.path.dirname(__file__)


class RuleMatcher:
    WHITESPACE_REGEX: Final = re.compile(r"\s")
    LETTER_SUB_REGEX: Final = re.compile(r"[^a-zA-z]")

    def __init__(self):
        self.rules = {}

        self.load_rules()

    def load_rules(self):
        csv_path = os.path.join(dirname, "rules.csv")

        with open(csv_path, encoding="utf-8") as csvfile:
            reader = csv.DictReader(csvfile)
            for line in reader:
                for label, rule in line.items():
                    if not rule:
                        continue

                    self.rules[rule] = label

    def classify(self, input_text: Union[bytes, str]) -> str:
        if isinstance(input_text, bytes):
            input_text = input_text.decode("utf-8")

        tokens = re.split(self.WHITESPACE_REGEX, input_text)
        words = [re.sub(self.LETTER_SUB_REGEX, "", token) for token in tokens]

        for word in words:
            if label := self.rules.get(word):
                logging.debug(f"{label=} for {word=}")
                return label

        return score_input_majority_class(input_text)

    def predict(self, features: Iterable):
        return [self.classify(feature) for feature in features]
