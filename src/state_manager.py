from functools import partial
import logging
from typing import Final

from transitions import Machine

from src.preferences import Preferences

from src.dialog_handler import DialogHandler


class StateManager:
    STATES: Final = [
        "initial",
        "suggest_other_preference",
        "additional_requirements",
        "suggest_other_consequent",
        "suggest_restaurant",
        "additional_info",
        "bye",
    ]

    def __init__(self, loglevel=logging.WARNING, machine_cls=Machine):
        logging.getLogger("transitions").setLevel(loglevel)

        self.state: str

        self.current_preferences = Preferences()

        self.machine = machine_cls(
            model=self,
            states=self.STATES,
            initial="initial",
            ignore_invalid_triggers=True,
        )

        # callbacks
        self.machine.on_enter_additional_requirements(
            DialogHandler.additional_requirements
        )
        self.machine.on_enter_initial(self.request_missing_info)
        self.machine.on_enter_bye(DialogHandler.say_bye_exit)

        # initial
        self.machine.add_transition(
            trigger="inform_unknown",
            source="initial",
            dest="initial",
            before=DialogHandler.unknown_restaurant,
        )
        self.machine.add_transition(
            trigger="inform_known",
            source="initial",
            dest="additional_requirements",
            conditions="preferences_filled",
        )
        self.machine.add_transition(
            trigger="inform_known",
            source="initial",
            dest="initial",
            unless="preferences_filled",
        )
        self.machine.add_transition(
            trigger="inform_typo", source="initial", dest="suggest_other_preference"
        )

        # suggest_other_preference
        self.machine.add_transition(
            trigger="deny",
            source="suggest_other_preference",
            dest="initial",
            before=DialogHandler.unknown_restaurant,
        )
        self.machine.add_transition(
            trigger="affirm",
            source="suggest_other_preference",
            dest="additional_requirements",
            conditions="preferences_filled",
        )
        self.machine.add_transition(
            trigger="affirm",
            source="suggest_other_preference",
            dest="initial",
            unless="preferences_filled",
        )

        # additional_requirements
        self.machine.add_transition(
            trigger="deny", source="additional_requirements", dest="suggest_restaurant"
        )
        self.machine.add_transition(
            trigger="inform_known",
            source="additional_requirements",
            dest="suggest_restaurant",
        )
        self.machine.add_transition(
            trigger="inform_unknown",
            source="additional_requirements",
            dest="suggest_restaurant",
        )
        self.machine.add_transition(
            trigger="inform_typo",
            source="additional_requirements",
            dest="suggest_other_consequent",
        )

        # suggest_other_consequent
        self.machine.add_transition(
            trigger="affirm",
            source="suggest_other_consequent",
            dest="suggest_restaurant",
        )
        self.machine.add_transition(
            trigger="deny",
            source="suggest_other_consequent",
            dest="suggest_restaurant",
            before=DialogHandler.unknown_restaurant,
        )

        # suggest_restaurant
        self.machine.add_transition(
            trigger="deny",
            source="suggest_restaurant",
            dest="suggest_restaurant",
        )
        self.machine.add_transition(
            trigger="reqmore",
            source="suggest_restaurant",
            dest="suggest_restaurant",
        )
        self.machine.add_transition(
            trigger="request",
            source="suggest_restaurant",
            dest="additional_info",
        )
        self.machine.add_transition(
            trigger="affirm",
            source="suggest_restaurant",
            dest="bye",
        )
        self.machine.add_transition(
            trigger="thankyou",
            source="suggest_restaurant",
            dest="bye",
        )

        # additional_info
        self.machine.add_transition(
            trigger="bye",
            source="additional_info",
            dest="bye",
        )
        self.machine.add_transition(
            trigger="affirm",
            source="additional_info",
            dest="bye",
        )
        self.machine.add_transition(
            trigger="thankyou",
            source="additional_info",
            dest="bye",
        )

        # global
        self.machine.add_transition(
            trigger="bye",
            source="*",
            dest="bye",
        )
        self.machine.add_transition(
            trigger="restart", source="*", dest="initial", before="reset_preferences"
        )

    def preferences_filled(self) -> bool:
        return self.current_preferences.is_full()

    def negate(self):
        """make negate alias for deny"""
        self.deny()

    def hello(self):
        DialogHandler.greet()

    def repeat(self):
        DialogHandler.repeat_text()

    def thankyou(self):
        DialogHandler.youre_welcome()

    def null(self):
        DialogHandler.do_not_understand()

    def reset_preferences(self):
        self.current_preferences = Preferences()

    def request_missing_info(self):
        DialogHandler.request_missing_info(
            missing_keyword=self.current_preferences.missing_preferences()[0]
        )

    # TODO: should handle this
    def out_of_suggestions(self):
        self.bye()
