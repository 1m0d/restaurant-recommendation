import logging
from typing import Final, Optional

import pandas as pd
from src.dialog_handler import DialogHandler
from src.keyword_matching import KeywordMatcher

from src.preferences import Preferences
from src.state_manager import StateManager


DEFAULT_RESTAURANT_INFO_PATH: Final = "./datafiles/restaurant_info.csv"
DEFAULT_INFERENCE_RULES_PATH: Final = "./datafiles/inference_rules.csv"


class RestaurantRecommender:
    def __init__(
        self,
        classifier,
        restaurant_info_path: str = DEFAULT_RESTAURANT_INFO_PATH,
        inference_rules_path: str = DEFAULT_INFERENCE_RULES_PATH,
    ):
        self.restaurants = pd.read_csv(restaurant_info_path)
        self.inference_rules = pd.read_csv(inference_rules_path)
        self.state_manager = StateManager()
        self.preferences = Preferences()
        self.keyword_matcher = KeywordMatcher(restaurants_df=self.restaurants)
        self.classifier = classifier
        self.recommend_restaurants: Optional[pd.DataFrame] = None
        self.logger = logging.getLogger(__name__)
        self.last_matched_preferences = Optional[Preferences]

    def run(self):
        DialogHandler.initial()

        while self.state_manager.state != "bye":
            user_input = input().lower()
            trigger = self._input_to_trigger(user_input=user_input)
            if trigger == "inform":
                (
                    matched_preferences,
                    levenshtein_used,
                ) = self.keyword_matcher.match_keyword(user_input)
                self.preferences += matched_preferences
                self.state_manager.current_preferences = self.preferences
                self.last_matched_preferences = matched_preferences

                if matched_preferences.is_empty():
                    trigger = "inform_unknown"
                elif levenshtein_used:
                    trigger = "inform_typo"
                else:
                    trigger = "inform_known"

            self.logger.debug(f"{trigger=}")

            trigger_func = getattr(self.state_manager, trigger, None)
            if not trigger_func:
                self.logger.error(
                    f"No state transition trigger found for {trigger=}. Defaulting"
                    " to null."
                )
                trigger_func = self.state_manager.machine.null
            trigger_func()

            if (
                self.state_manager.state == "suggest_restaurant"
                and not self.recommend_restaurants
            ):
                self._find_restaurants()

            #  if self.state_manager.state == "suggestion_accepted":
            #  self.preferences += self.last_matched_preferences
            #  if self.preferences.is_full():
            #  self._find_restaurants()
            #  self.state_manager.preferences_filled()
            #  elif self.state_manager.state == "out_of_suggestions":
            #  self.preferences = Preferences()

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
                    postcode=restaurant.postcode,
                )
            else:
                self.state_manager.out_of_suggestions()
                DialogHandler.out_of_suggestions()
        elif self.state_manager.state == "suggest_other_preference":
            DialogHandler.suggest_other_keyword(str(self.last_matched_preferences))
        elif self.state_manager.state == "suggestion_denied":
            DialogHandler.suggest_other_keyword(str(self.last_matched_preferences))
        #  else:
        #  func = getattr(DialogHandler, self.state_manager.state)
        #  func()

    def _find_restaurants(self):
        self.recommend_restaurants = self.restaurants.query(
            self.preferences.to_pandas_query()
        ).itertuples()

    def infer_additional_preference(self, consequent: str):
        """
        consequent: specific preference like romantic
        filter suggestions
        """
        antedecents = self.inference_rules[
            (self.inference_rules.consequent == consequent)
        ]

        if antedecents.empty:
            return

        self.recommend_restaurants = self.recommend_restaurants.query(
            self._antedecents_to_query(antedecents)
        )

    def _antedecents_to_query(self, antedecents: pd.DataFrame) -> str:
        return " & ".join(
            f"{antedecent.column_name}"
            f"{self._wanted_to_operation(antedecent.wanted)}"
            f"'{antedecent.antedecent}'"
            for antedecent in antedecents.itertuples()
        )

    def _wanted_to_operation(self, wanted: bool) -> str:
        return "==" if wanted else "!="
