from typing import Final


class DialogHandler:
    MACHINE_DIALOGS: Final = {
        "initial": "Welcome to this restaurant recommendation system. You can ask for restaurants by type of food, area, or price range. How can I help you today?",
        "neutral": "Remember, you can ask for restaurants by type of food, area, or price range.",
        "suggest_restaurant": "{restaurant} is a {price_range} priced restaurant, located in {area}, that serves {food_type} food. Address: {postcode} {address}. Is this okay?",
        "request_missing_info": "What should the {missing_keyword} of the restaurant be?",
        "say_bye_exit": "Thank you for using this restaurant recommendation system. Have a nice day!",
        "return_requested_info": "The {info_type} of {restaurant} is {info}",
        "youre_welcome": "You're welcome.",
        "greet": "Hello!",
        "suggest_to_replace": [
            "Would you like to search for restaurants in the {area} area?",
            "Would you like to search for restaurants with {food_type} food?",
            "Would you like to search for restaurants in the {price_range} price range?",
        ],
        "suggest_other_keyword": "Did you mean {suggested_keyword}?",
        "suggestion_accepted": "Added it to your prefences.",
        "suggestion_denied": "Sorry, I don't know any restaurants where you can find {prefences}",
        "out_of_suggestions": "Sorry I don't know any restaurants like that. Do you want to start over?",
        "unknown_restaurant": "Sorry, I do not know any such restaurant.",
        "additional_requirement": "Do you have an additional requirement?",
        "additional_requirement_question": "What is your additional requirement?",
        "do_not_understand": "Sorry, I do not understand.",
    }

    BLUE: Final = "\033[94m"
    END_COLOR: Final = "\033[0m"

    last_text = ""

    @classmethod
    def _print(cls, string: str):
        cls.last_text = string
        print(cls.BLUE + string + cls.END_COLOR)

    @classmethod
    def initial(cls):
        cls._print(cls.MACHINE_DIALOGS["initial"])

    @classmethod
    def neutral(cls):
        cls._print(cls.MACHINE_DIALOGS["neutral"])

    @classmethod
    def suggest_restaurant(
        cls,
        restaurant: str,
        price_range: str,
        area: str,
        food_type: str,
        address: str,
        postcode: str,
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

    @classmethod
    def suggestion_accepted(cls):
        cls._print(cls.MACHINE_DIALOGS["suggestion_accepted"])

    @classmethod
    def suggestion_denied(cls, preferences: str):
        cls._print(cls.MACHINE_DIALOGS["suggestion_denied"].format(**locals()))

    @classmethod
    def repeat_text(cls):
        cls._print(cls.last_text)

    @classmethod
    def out_of_suggestions(cls):
        cls._print(cls.MACHINE_DIALOGS["out_of_suggestions"])

    @classmethod
    def unknown_restaurant(cls):
        cls._print(cls.MACHINE_DIALOGS["unknown_restaurant"])

    @classmethod
    def additional_requirement(cls):
        cls._print(cls.MACHINE_DIALOGS["additional_requirement"])

    @classmethod
    def additional_requirement_question(cls):
        cls._print(cls.MACHINE_DIALOGS["additional_requirement_question"])

    @classmethod
    def do_not_understand(cls):
        cls._print(cls.MACHINE_DIALOGS["do_not_understand"])
