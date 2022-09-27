from dataclasses import dataclass
from typing import ClassVar, List, Optional


@dataclass
class Preferences:
    food_type: Optional[str] = None
    area: Optional[str] = None
    price_range: Optional[str] = None

    CSV_ALIASES: ClassVar = {
        "food_type": "food",
        "area": "area",
        "price_range": "pricerange",
    }

    def missing_preferences(self) -> List:
        return [field_name for field_name, value in self.__dict__.items() if not value]

    def is_full(self) -> bool:
        return all(self.__dict__.values())

    def __iadd__(self, other):
        """Merges preferences, if value set in both instances {other} has preference"""
        for key, value in other.__dict__.items():
            if value:
                setattr(self, key, value)

        return self

    def to_pandas_query(self) -> str:
        return " & ".join(
            [
                f"{self.CSV_ALIASES[key]} == '{value}'"
                for key, value in self.__dict__.items()
            ]
        )
