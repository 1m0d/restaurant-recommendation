import logging
from typing import Final

from transitions import Machine

from src.preferences import Preferences


class StateManager:
    """
    NOTE: that you cannot immediately pass the dialog act into this.
    To call the right state trigger, you need to take into account the following:
    Inform is split into inform_known and inform_unknown, to account for people asking for keywords we don't know.
    There is a trigger do_check_table which needs to be called when state check_table is entered.

    NOTE: that the functions at the end each have an argument other than self. IDK how this works implementation wise... maybe they should just be defined outside this class.
    """

    STATES: Final = [
        "neutral",  # 0 - This should lead to maybe 2-3 variations in text responses:
        # Such as repeating info about a recently recommended restaurant
        # or asking again "how can I help you further?"
        "suggest_restaurant",  # 1
        "request_missing_info",  # 2
        "say_bye_exit",  # 3
        "return_requested_info",  # 4
        "youre_welcome",  # 5
        "greet",  # 6
        "suggest_to_replace",  # 7
        "repeat_statement",  # 8
        "suggest_other_keyword",  # 9
        "check_table",  # 10
    ]

    def __init__(self, loglevel=logging.WARNING):
        logging.getLogger("transitions").setLevel(loglevel)

        self.last_text = ""
        self.current_preferences = Preferences()

        self.machine = Machine(model=self, states=self.STATES, initial="neutral")

        # The universal path for negate
        self.machine.add_transition(trigger="negate", source="*", dest="neutral")

        # The paths for ack and null are boring so far
        self.machine.add_transition(trigger="ack", source="*", dest="neutral")
        self.machine.add_transition(
            trigger="null", source="*", dest="neutral"
        )  # might need to change

        # Restart will always lead you to the initial text again (minus the welcome), stating your options
        self.machine.add_transition(
            trigger="restart", source="*", dest="neutral", after="restate_options"
        )

        # In the following cases, affirm should do something then lead to neutral
        self.machine.add_transition(
            trigger="affirm",
            source="suggest_to_replace",
            dest="check_table",
        )
        self.machine.add_transition(
            trigger="affirm",
            source="suggest_other_keyword",
            dest="check_table",
        )

        # In neutral/unknown cases, these will all repeat the most recent message (in similar or the same wording)
        self.machine.add_transition(trigger="repeat", source="*", dest="repeat_text")
        self.machine.add_transition(trigger="affirm", source="*", dest="repeat_text")

        self.machine.add_transition(
            trigger="inform_known",
            source="*",
            dest="request_missing_info",
        )

        # These are straightforward
        self.machine.add_transition(
            trigger="inform_unknown", source="*", dest="suggest_other_keyword"
        )
        self.machine.add_transition(trigger="hello", source="*", dest="greet")
        self.machine.add_transition(
            trigger="bye", source="*", dest="say_bye_exit", after="say_goodbye"
        )
        self.machine.add_transition(
            trigger="reqalts", source="*", dest="suggest_to_replace"
        )
        self.machine.add_transition(
            trigger="thankyou", source="*", dest="youre_welcome"
        )

        # When deny is detected with some keyword, we label it as !thatkeyword, as a preference AGAINST
        self.machine.add_transition(trigger="deny", source="*", dest="neutral")
        # DONT USE FOR NOW self.machine.add_transition(trigger='deny_w_info', source='*', dest='check_table', before='override_slot')

        # For now, these do the same thing(like in most example cases)
        self.machine.add_transition(
            trigger="confirm", source="*", dest="return_requested_info"
        )
        self.machine.add_transition(
            trigger="request", source="*", dest="return_requested_info"
        )

        # CHANGE LATER: make sure it's either a new restaurant or note that there are no other restaurants
        self.machine.add_transition(
            trigger="reqmore", source="*", dest="suggest_restaurant"
        )

        self.machine.add_transition(  # should comes from source "check_table", but put "*" for good measure
            trigger="missing_info", source="*", dest="request_missing_info"
        )

        self.machine.add_transition(
            trigger="preferences_filled", source="*", dest="suggest_restaurant"
        )

        self.machine.add_transition(
            trigger="affirm",
            source="suggest_restaurant",
            dest="final",
        )

        self.machine.add_transition(
            trigger="deny",
            source="suggest_restaurant",
            dest="suggest_restaurant",
        )

        # TODO: what to do when out out of suggestions
        self.machine.add_transition(
            trigger="out_of_suggestions",
            source="*",
            dest="final",
        )

    def say_hello(self):
        print("Hello!")

    def say_goodbye(self):
        print("Thank you for using this restaurant recommendation system! Goodbye!")

    def repeat_text(self):
        print(self.last_text)

    def restate_options(self):
        print("SOME LINE SHOWING AN OVERVIEW OF WHAT YOU CAN ASK THE MACHINE")

    def youre_welcome(self):
        print("You're welcome.")
