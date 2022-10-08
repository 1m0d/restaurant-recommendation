import re
from typing import Iterable, Optional, Pattern, Tuple

import Levenshtein
import numpy as np
import pandas as pd

from src.preferences import Preferences


class KeywordMatcher:
    """
    Provide methods for extracting key information from input string.
    """

    distance: int

    def __init__(self, restaurants_df: pd.DataFrame, rules_df: pd.DataFrame):
        self.restaurants_table = restaurants_df
        self.rules_table = rules_df
        self._compile_regex_patterns()

    def match_keyword(self, string: str) -> Tuple[Preferences, bool]:
        """
        Extract restaurant preferences from input string.

        returns: Tuple where first element is the matched preferences
            and the second element is a boolean showing whether Levenshtein
            distance was used to find preferences
        """
        matched_preferences = Preferences()
        (matched_preferences.area, bool1) = self._matcher(
            self.area_pattern, self.known_areas, string
        )
        (matched_preferences.food_type, bool2) = self._matcher(
            self.food_pattern, self.known_foods, string
        )
        (matched_preferences.price_range, bool3) = self._matcher(
            self.price_pattern, self.known_price_ranges, string
        )

        levenshtein_used = bool1 or bool2 or bool3

        return (matched_preferences, levenshtein_used)

    def match_additional_preference(self, string: str) -> Tuple[Optional[str], bool]:
        """
        Extract additional preferences from input string.

        returns: Tuple where first element is the matched preference
            and the second element is a boolean showing whether Levenshtein
            distance was used to find preferences
        """
        return self._matcher(
            self.consequent_pattern, self.known_consequents, string=string
        )

    def match_additional_information(self, string: str) -> Optional[str]:
        """
        Extract additional information from input string.
        If found convert it to restaurants_table column name.
        """
        if "address" in string:
            return "addr"

        if "postcode" in string or "post code" in string:
            return "postcode"

        if "phone" in string:
            return "phone"

        return None

    def _compile_regex_patterns(self):
        self.known_areas = self.restaurants_table.area.unique()[:-1]
        area_regexes = [
            r"((?<=in\sthe\s)\w+)",
            r"(\w+(?= (part)?\s+of\s+(the)?(town|city)))",
            r"(\w) area",
        ]
        area_patterns = np.concatenate([self.known_areas, area_regexes])
        self.area_pattern = re.compile("|".join(area_patterns))

        self.known_foods = self.restaurants_table.food.unique()
        food_regexes = [r"serves\s(\w+)", r"(\w+)\srestaurant", r"(\w+)\sfood"]
        food_patterns = np.concatenate([self.known_foods, food_regexes])
        self.food_pattern = re.compile("|".join(food_patterns))

        self.known_price_ranges = self.restaurants_table.pricerange.unique()
        price_regexes = [r"(\w+)\sprice(d)?", r"(\w+)\scost(ing)?"]
        price_patterns = np.concatenate([self.known_price_ranges, price_regexes])
        self.price_pattern = re.compile("|".join(price_patterns))

        self.known_consequents = self.rules_table.consequent.unique()
        consequent_regexes = [r"(\w+)\srestaurant"]
        consequent_patterns = np.concatenate(
            [self.known_consequents, consequent_regexes]
        )
        self.consequent_pattern = re.compile("|".join(consequent_patterns))

    @classmethod
    def _matcher(
        cls, keyword_pattern: Pattern, known_keywords: Iterable[str], string: str
    ) -> Tuple[Optional[str], bool]:
        match = keyword_pattern.search(string)
        if not match or not match.group():
            return (None, False)

        if match.group() in known_keywords:
            return (match.group(), False)

        if any(match.groups()):
            pattern_match = next(group for group in match.groups() if group)
            if pattern_match:
                return (cls._levenshtein(pattern_match, known_keywords), True)

        # should not reach this
        return (match.group(), False)

    @classmethod
    def _levenshtein(cls, item, table) -> Optional[str]:
        distances = [(x, Levenshtein.distance(item, x)) for x in table]
        distances.sort(key=lambda x: x[1])
        if distances[0][1] > cls.distance:
            return None
        return distances[0][0]
