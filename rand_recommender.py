from recommender import Recommender
from typing import List
from random import choices

Recipe = dict

class RandRecommender(Recommender):
    def __init__(self, recipes: List[Recipe]):
        super().__init__(recipes)

    def train(self, user_pref):
        """ just selects a random recipe over all recipes, no training """
        pass

    def recommend(self, numrecs) -> Recipe:
        return choices(self.recipes, k=numrecs)