from abc import ABC, abstractmethod

MIN_PREFS = 100


class Recommender(ABC):
    def __init__(self, X, user_prefs, recs):
        self.X = X

    def train(self, user_prefs):
        if len(user_prefs) < MIN_PREFS:
            initiali

    @abstractmethod
    def recommend(self, numrecs):
        train_data = self.X

    @abstractmethod
    def update_model(new_pref_row, new_pref_obs):
