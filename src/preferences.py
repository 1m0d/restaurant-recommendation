from dataclasses import dataclass
from typing import ClassVar, List, Optional


@dataclass
class Preferences:
    """Handle restaurants_table preferences of users"""

    food_type: Optional[str] = None
    area: Optional[str] = None
    price_range: Optional[str] = None

    CSV_ALIASES: ClassVar = {
        "food_type": "food",
        "area": "area",
        "price_range": "pricerange",
    }

    def missing_preferences(self) -> List:
        """Return preference field names that haven't been set yet"""
        return [field_name for field_name, value in self.__dict__.items() if not value]

    def is_full(self) -> bool:
        """Have all preferences been set?"""
        return all(self.__dict__.values())

    def is_empty(self) -> bool:
        """Have none of the preferences been set?"""
        return not any(self.__dict__.values())

    def __iadd__(self, other):
        """Merges preferences, if value set in both instances {other} has preference"""
        for key, value in other.__dict__.items():
            if value:
                setattr(self, key, value)

        return self

    def to_pandas_query(self) -> str:
        """Generate pandas query based on existing preferences"""
        return " & ".join(
            [
                f"{self.CSV_ALIASES[key]} == '{value}'"
                for key, value in self.__dict__.items()
            ]
        )

    def __str__(self) -> str:
        output = ""
        if self.price_range:
            output += f"{self.price_range} priced "
        if self.food_type:
            output += f"{self.food_type} food "
        if self.area:
            output += f"in {self.area}"

        return output
