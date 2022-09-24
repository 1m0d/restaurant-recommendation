from dataclasses import dataclass
from typing import List, Optional
from src.models.logistic_regression_model import LogisticRegressionModel
from src.state_manager import StateManager


@dataclass
class Preferences:
    food_type: Optional[str] = None
    area: Optional[str] = None
    price_range: Optional[str] = None

    def missing_preferences(self) -> List:
        return [field_name for field_name, value in self.__dict__.items() if not value]

    def is_full(self) -> bool:
        return all(self.__dict__)


class RestaurantRecommender:
    def __init__(self, classifier):
        self.state_manager = StateManager("")
        self.preferences = Preferences()
        self.classifier = classifier

    def run(self):
        print("Hello, how can I help you?")

        while True:
            user_input = input().lower()
            feature_vector = self.classifier.feature_extraction([user_input])
            predicted_act = self.classifier.model.predict(feature_vector)[0].decode("utf-8")
            print(f"{predicted_act=}")

            if predicted_act == "inform":
                preferences = keyword_match(user_input)

def keyword_match(input_text):
    pass
