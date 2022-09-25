import logging
from typing import Iterable, Tuple

import pandas as pd
from src.dialog_handler import DialogHandler

from src.preferences import Preferences
from src.state_manager import StateManager


class RestaurantRecommender:
    def __init__(self, classifier, csv_path: str = "./restaurant_info.csv"):
        self.state_manager = StateManager()
        self.preferences = Preferences()
        self.classifier = classifier
        self.recommend_restaurants: Iterable[str] = []
        self.restaurants = pd.read_csv(csv_path)
        self.logger = logging.getLogger(__name__)

    def run(self):
        DialogHandler.initial()

        while self.state_manager.state != "final":
            user_input = input().lower()
            trigger = self._input_to_trigger(user_input=user_input)
            if trigger == "inform":
                matched_preferences, levenshtein_used = keyword_match(user_input)
                self.preferences += matched_preferences
                self.state_manager.current_preferences = self.preferences

                if levenshtein_used:
                    trigger = "inform_unknown"
                else:
                    trigger = "inform_known"

                    if self.preferences.is_full():
                        self._find_restaurants()
                        trigger = "restaurant_recommend"

            self.logger.debug(f"{trigger=}")

            trigger_func = getattr(self.state_manager, trigger, None)
            if not trigger_func:
                self.logger.error(
                    f"No state transition trigger found for {trigger=}. Defaulting"
                    " to null."
                )
                trigger_func = self.state_manager.machine.null
            trigger_func()

            self._state_to_utterance()

    def _input_to_trigger(self, user_input) -> str:
        feature_vector = self.classifier.feature_extraction([user_input])
        trigger = self.classifier.model.predict(feature_vector)[0].decode("utf-8")
        self.logger.debug(f"classified input as {trigger}")

        return trigger

    def _state_to_utterance(self):
        """WIP"""
        if self.state_manager.state == "request_missing_info":
            DialogHandler.request_missing_info(
                missing_keyword=self.preferences.missing_preferences()[0]
            )
        else:
            func = getattr(DialogHandler, self.state_manager.state)
            func()

    def _find_restaurants(self):
        self.recommend_restaurants = self.restaurants.query(
            self.preferences.to_pandas_query()
        )


def keyword_match(input_text) -> Tuple[Preferences, bool]:
    return Preferences(), False
