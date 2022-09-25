from typing import Final


class DialogHandler:
    # TODO: ADD A STATE to the state manager called initial. It should not ever be a dest, but in self.machine set initial="initial"
    # Substitute the references to variables in this dict with the appropriate variable names (see anything in curly brackets {})
    # " TODO: repeat_statement" should just restate the most recently triggered dialog.
    # "check_table" is a state without dialog, as it should immediately call upon other states, not allow for a set of machine/user dialog yet.
    MACHINE_DIALOGS: Final = {
        "initial": "Welcome to this restaurant recommendation system. You can ask for restaurants by type of food, area, or price range. How can I help you today?",
        "neutral": [
            "Remember, you can ask for restaurants by type of food, area, or price range.",
            #  "{restaurant} is a {price_range} priced restaurant, located in {area}, that serves {food_type} food.", #  TODO: implement random restaurant suggestion
            "",
        ],
        "suggest_restaurant": "{restaurant} is a {price_range} priced restaurant, located in {area}, that serves {food_type} food.",
        "request_missing_info": "What should the {missing_keyword} of the restaurant be?",  # missing_keyword should say "food type", "area", or "price range"
        #  "request_missing_info": [
        #  "What should the {missing_keyword} of the restaurant be?",  # missing_keyword should say "food type", "area", or "price range"
        #  "What kind of food do you prefer?",  # TODO: We can either use the missing_keyword implementation here, or implement that the code specifies which question is asked based on what is missing.
        #  "What part of town do you prefer?",
        #  "Would you prefer a restaurant in the cheap, moderate, or expensive price range?",
        #  ],
        "say_bye_exit": "Thank you for using this restaurant recommendation system. Have a nice day!",
        "return_requested_info": "The {info_type} of {restaurant} is {info}",  # info_type is either phone, post code, or address, I believe. info should be the actual info.
        "youre_welcome": "You're welcome.",
        "greet": "Hello!",
        "suggest_to_replace": [
            "Would you like to search for restaurants in the {area} area?",
            "Would you like to search for restaurants with {food_type} food?",
            "Would you like to search for restaurants in the {price_range} price range?",
        ],
        "suggest_other_keyword": "Did you mean {suggested_keyword}?",
    }

    BLUE: Final = "\033[94m"
    END_COLOR: Final = "\033[0m"

    @classmethod
    def _print(cls, string: str):
        print(cls.BLUE + string + cls.END_COLOR)

    @classmethod
    def initial(cls):
        cls._print(cls.MACHINE_DIALOGS["initial"])

    @classmethod
    def neutral(cls):
        cls._print(cls.MACHINE_DIALOGS["neutral"])

    @classmethod
    def suggest_restaurant(
        cls, restaurant: str, price_range: str, area: str, food_type: str
    ):
        cls._print(cls.MACHINE_DIALOGS["suggest_restaurant"].format(**locals()))

    @classmethod
    def request_missing_info(cls, missing_keyword: str):
        cls._print(cls.MACHINE_DIALOGS["request_missing_info"].format(**locals()))

    @classmethod
    def say_bye_exit(cls):
        cls._print(cls.MACHINE_DIALOGS["say_bye_exit"])

    @classmethod
    def return_requested_info(cls, info_type: str, restaurant: str, info: str):
        cls._print(cls.MACHINE_DIALOGS["return_requested_info"].format(**locals()))

    @classmethod
    def youre_welcome(cls):
        cls._print(cls.MACHINE_DIALOGS["youre_welcome"])

    @classmethod
    def greet(cls):
        cls._print(cls.MACHINE_DIALOGS["greet"])

    @classmethod
    def suggest_to_replace(cls):
        pass
        #  cls._print(cls.MACHINE_DIALOGS["suggest_to_replace"])

    @classmethod
    def suggest_other_keyword(cls, suggested_keyword: str):
        cls._print(cls.MACHINE_DIALOGS["suggest_other_keyword"].format(**locals()))