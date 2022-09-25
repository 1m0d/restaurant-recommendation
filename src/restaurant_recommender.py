import logging
from typing import Iterable, Tuple

import pandas as pd

from src.preferences import Preferences
from src.state_manager import StateManager


class RestaurantRecommender:
    def __init__(self, classifier, csv_path: str = "./restaurant_info.csv"):
        self.state_manager = StateManager("")
        self.preferences = Preferences()
        self.classifier = classifier
        self.recommend_restaurants: Iterable[str] = []
        self.restaurants = pd.read_csv(csv_path)
        self.logger = logging.getLogger(__name__)

    def run(self):
        print("Hello, how can I help you?")

        while True:
            user_input = input().lower()
            feature_vector = self.classifier.feature_extraction([user_input])
            trigger = self.classifier.model.predict(feature_vector)[0].decode("utf-8")
            print(f"{trigger=}")

            if trigger == "inform":
                matched_preferences, levenshtein_used = keyword_match(user_input)
                self.preferences += matched_preferences

                if levenshtein_used:
                    trigger = "inform_unknown"
                else:
                    trigger = "inform_known"

                    if self.preferences.is_full:
                        self._find_restaurants()
                        trigger = "restaurant_recommend"

            trigger_func = getattr(self.state_manager, trigger)
            if not trigger_func:
                self.logger.error(
                    f"No state transition trigger found for {trigger_func=}. Defaulting"
                    " to null."
                )
                trigger_func = self.state_manager.null
            trigger_func()

            self._state_to_utterance()

            if self.state_manager.state == "final":
                break

    def _state_to_utterance(self) -> str:
        pass

    def _find_restaurants(self):
        self.recommend_restaurants = self.restaurants.query(
            self.preferences.to_pandas_query()
        )


def keyword_match(input_text) -> Tuple[Preferences, bool]:
    return Preferences(), False
