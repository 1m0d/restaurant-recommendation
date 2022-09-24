from dataclasses import dataclass
from typing import List, Optional

@dataclass
class Preferences:
    food_type: Optional[str] = None
    area: Optional[str] = None
    price_range: Optional[str] = None

    def missing_preferences(self) -> List:
        return [field_name for field_name, value in self.__dict__.items() if not value]

    def is_full(self) -> bool:
        return all(self.__dict__)

    def __add__(self, other):
        """merge preferences"""
