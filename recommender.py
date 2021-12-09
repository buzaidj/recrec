from abc import ABC, abstractmethod


class Recommender(ABC):
    @abstractmethod
    def __init__(self, recipes, user_prefs, user_recs):
        """
        recipes is the file name with all recipes
        user prefs is the file name with all prefs so far
        user recs is the file name wiith all recs so far
        """
        pass

    @abstractmethod
    def train(self):
        """
        train the model
        """
        pass

    @abstractmethod
    def recommend(self, num_recs):
        """
        Reccomend num_recs recipes
        """

    @abstractmethod
    def present_recipe(self):
        """
        Present a recipe to the user, either a recommendation or an observation

        Record the users response in their user files
        """
