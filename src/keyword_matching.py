import re
from typing import Iterable, Optional, Pattern, Tuple

import Levenshtein
import numpy as np
import pandas as pd
from src.preferences import Preferences


class KeywordMatcher:
    def __init__(self):
        self.table = pd.read_csv("restaurant_info.csv")
        self._compile_regex_patterns()

    def match_keyword(self, string: str) -> Tuple[Preferences, bool]:
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

    def _compile_regex_patterns(self):
        self.known_areas = self.table.area.unique()[:-1]
        area_regexes = [
            r"((?<=in\sthe\s)\w+)",
            r"(\w+(?= (part)?\s+of\s+(the)?(town|city)))",
            r"(\w) area"
        ]
        area_patterns = np.concatenate([self.known_areas, area_regexes])
        self.area_pattern = re.compile("|".join(area_patterns))

        self.known_foods = self.table.food.unique()
        food_regexes = [r"((?<=serves\s)\w+)", r"(\w+(?= restaurant))", r"(\w+) food"]
        food_patterns = np.concatenate([self.known_foods, food_regexes])
        self.food_pattern = re.compile("|".join(food_patterns))

        self.known_price_ranges = self.table.pricerange.unique()
        price_regexes = [r"(\w+(?= price(d)?))", r"(\w+(?= cost(ing)?))"]
        price_patterns = np.concatenate([self.known_price_ranges, price_regexes])
        self.price_pattern = re.compile("|".join(price_patterns))

    @classmethod
    def _matcher(
        cls, keyword_pattern: Pattern, known_keywords: Iterable[str], string: str
    ) -> Tuple[Optional[str], bool]:
        try:
            match = keyword_pattern.search(string).group()
        except AttributeError:
            return (None, False)

        if match in known_keywords:
            return (match, False)

        return (cls._levenshtein(match, known_keywords, cls.distance), True)

    @classmethod
    def _levenshtein(cls, item, table, distance):
        distances = [(x, Levenshtein.distance(item, x)) for x in table]
        distances.sort(key=lambda x: x[1])
        if distances[0][1] > distance:
            return "random"
        return distances[0][0]
