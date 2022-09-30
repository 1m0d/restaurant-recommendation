import logging
from typing import Iterable, Optional

import pandas as pd
from src.dialog_handler import DialogHandler
from src.keyword_matching import KeywordMatcher

from src.preferences import Preferences
from src.state_manager import StateManager


class RestaurantRecommender:
    def __init__(self, classifier, csv_path: str = "./restaurant_info.csv"):
        self.state_manager = StateManager()
        self.preferences = Preferences()
        self.keyword_matcher = KeywordMatcher()
        self.classifier = classifier
        self.recommend_restaurants: Iterable[str] = []
        self.restaurants = pd.read_csv(csv_path)
        self.logger = logging.getLogger(__name__)
        self.last_matched_preferences = Optional[Preferences]

    def run(self):
        DialogHandler.initial()

        while self.state_manager.state != "say_bye_exit":
            user_input = input().lower()
            trigger = self._input_to_trigger(user_input=user_input)
            if trigger == "inform":
                (
                    matched_preferences,
                    levenshtein_used,
                ) = self.keyword_matcher.match_keyword(user_input)
                __import__('ipdb').set_trace()
                self.preferences += matched_preferences
                self.last_matched_preferences = matched_preferences

                if matched_preferences.is_empty():
                    trigger = "inform_unknown"
                elif levenshtein_used:
                    trigger = "inform_typo"
                else:
                    trigger = "inform_known"

                    if self.preferences.is_full():
                        self._find_restaurants()
                        trigger = "preferences_filled"

            self.logger.debug(f"{trigger=}")

            trigger_func = getattr(self.state_manager, trigger, None)
            if not trigger_func:
                self.logger.error(
                    f"No state transition trigger found for {trigger=}. Defaulting"
                    " to null."
                )
                trigger_func = self.state_manager.machine.null
            trigger_func()

            if self.state_manager.state == "suggestion_accepted":
                self.preferences += self.last_matched_preferences
                if self.preferences.is_full():
                    self._find_restaurants()
                    self.state_manager.preferences_filled()

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
        elif self.state_manager.state == "suggest_restaurant":
            restaurant = next(self.recommend_restaurants, None)
            if restaurant:
                DialogHandler.suggest_restaurant(
                    restaurant=restaurant.restaurantname,
                    price_range=restaurant.pricerange,
                    area=restaurant.area,
                    food_type=restaurant.food,
                    address=restaurant.addr,
                    postcode=restaurant.postcode
                )
            else:
                self.state_manager.out_of_suggestions()
        elif self.state_manager.state == "suggest_other_keyword":
            DialogHandler.suggest_other_keyword(str(self.last_matched_preferences))
        elif self.state_manager.state == "suggestion_denied":
            DialogHandler.suggest_other_keyword(str(self.last_matched_preferences))
        else:
            func = getattr(DialogHandler, self.state_manager.state)
            func()

    def _find_restaurants(self):
        self.recommend_restaurants = self.restaurants.query(
            self.preferences.to_pandas_query()
        ).itertuples()
