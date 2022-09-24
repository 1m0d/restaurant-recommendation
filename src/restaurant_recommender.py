from src.state_manager import StateManager
from src.preferences import Preferences

class RestaurantRecommender:
    def __init__(self, classifier):
        self.state_manager = StateManager("")
        self.preferences = Preferences()
        self.classifier = classifier
        self.matched_preferences = []  #  TODO: remove in the end if turns out not needed
        self.recommend_restaurants = []

    def run(self):
        print("Hello, how can I help you?")

        while True:
            user_input = input().lower()
            feature_vector = self.classifier.feature_extraction([user_input])
            predicted_act = self.classifier.model.predict(feature_vector)[0].decode("utf-8")
            print(f"{predicted_act=}")

            if predicted_act == "inform":
                matched_preferences, levenshtein_used = keyword_match(user_input)
                self.matched_preferences.append(matches)
                self.preferences += matched_preferences

                if levenshtein_used:
                    predicted_act = "inform_unknown"
                else:
                    if self.preferences.is_full:
                        self.recommend_restaurants.append(recommend_restaurant())
                        self.state_manager.call("restaurant_recommended")

                    predicted_act = "inform_known"

            self.state_manager.call(predicted_act)
            self.state_to_utterance(self.state_manager.state, self.preference)

            if self.state_manager.state == "final":
                break

    def state_to_utterance(self) -> str:
        pass

def keyword_match(input_text) -> (Preferences, bool):
    pass

def recommend_restaurant(preferences) -> str:
    #  print()
    pass
