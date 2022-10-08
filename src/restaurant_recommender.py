import logging
from typing import Final, Iterable, Optional, Tuple

import pandas as pd
from src.dialog_handler import DialogHandler
from src.keyword_matching import KeywordMatcher

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
        self.logger = logging.getLogger(__name__)

        self.classifier = classifier
        self.restaurants = pd.read_csv(restaurant_info_path)
        self.inference_rules = pd.read_csv(inference_rules_path)

        self.state_manager = StateManager()
        self.keyword_matcher = KeywordMatcher(
            restaurants_df=self.restaurants, rules_df=self.inference_rules
        )

        self._recommend_restaurants: Optional[pd.DataFrame] = None
        self.recommend_restaurants_iter: Optional[Iterable[Tuple]] = None
        self.current_restaurant: Optional[Tuple] = None

    @property
    def recommend_restaurants(self):
        return self._recommend_restaurants

    @recommend_restaurants.setter
    def recommend_restaurants(self, value: Optional[pd.DataFrame]):
        self._recommend_restaurants = value
        if value is not None:
            self.recommend_restaurants_iter = value.itertuples()

    def run(self):
        DialogHandler.initial()

        while self.state_manager.state != "bye":
            user_input = input().lower()
            trigger = self._input_to_trigger(user_input=user_input)

            trigger = self._handle_inform(user_input=user_input, trigger=trigger)
            self._handle_request(user_input=user_input, trigger=trigger)

            self.logger.debug(f"{trigger=}")

            trigger_func = getattr(self.state_manager, trigger, None)
            if not trigger_func:
                self.logger.error(
                    f"No state transition trigger found for {trigger=}. Defaulting"
                    " to null."
                )
                trigger_func = self.state_manager.null
            trigger_func()

            if (
                self.recommend_restaurants is None
                and self.state_manager.current_preferences.is_full()
            ):
                self._find_restaurants()

            if self.state_manager.state == "suggest_restaurant":
                self._suggest_restaurant()

    def _handle_inform(self, user_input: str, trigger: str):
        if trigger != "inform":
            return trigger

        if self.state_manager.state == "initial":
            (
                matched_preferences,
                levenshtein_used,
            ) = self.keyword_matcher.match_keyword(user_input)

            if not levenshtein_used:
                self.state_manager.current_preferences += matched_preferences

            self.state_manager.last_matched_preferences = matched_preferences

            if matched_preferences.is_empty():
                trigger = "inform_unknown"
            elif levenshtein_used:
                trigger = "inform_typo"
            else:
                trigger = "inform_known"
        elif self.state_manager.state == "additional_requirements":
            (
                matched_requirement,
                levenshtein_used,
            ) = self.keyword_matcher.match_additional_preference(user_input)

            if not matched_requirement:
                trigger = "inform_unknown"
                # TODO
            elif levenshtein_used:
                trigger = "inform_typo"
            else:
                trigger = "inform_known"
                self._infer_additional_preference(consequent=matched_requirement)

        return trigger

    def _handle_request(self, user_input: str, trigger: str):
        if trigger != "request":
            return

        matched_request = self.keyword_matcher.match_additional_information(user_input)
        if matched_request:
            DialogHandler.return_requested_info(
                info_type=matched_request,
                restaurant=self.current_restaurant.restaurantname,
                info=getattr(self.current_restaurant, matched_request),
            )

    def _input_to_trigger(self, user_input) -> str:
        feature_vector = self.classifier.feature_extraction([user_input])
        trigger = self.classifier.model.predict(feature_vector)[0].decode("utf-8")
        self.logger.debug(f"classified input as {trigger}")

        return trigger

    def _suggest_restaurant(self):
        self.current_restaurant = next(self.recommend_restaurants_iter, None)
        if self.current_restaurant:
            DialogHandler.suggest_restaurant(
                restaurant=self.current_restaurant.restaurantname,
                price_range=self.current_restaurant.pricerange,
                area=self.current_restaurant.area,
                food_type=self.current_restaurant.food,
            )
        else:
            self.state_manager.out_of_suggestions()
            self.recommend_restaurants = None

    def _find_restaurants(self):
        self.recommend_restaurants = self.restaurants.query(
            self.state_manager.current_preferences.to_pandas_query()
        )

    def _infer_additional_preference(self, consequent: str):
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
