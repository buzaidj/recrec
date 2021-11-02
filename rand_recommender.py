from recommender import Recommender
from typing import List
from random import choices

Recipe = dict

class RandRecommender(Recommender):
    def __init__(self, userjson, recipes: List[Recipe]):
        super().__init__(userjson, recipes)

    def train(self, user_meta_json):
        """ just selects a random recipe over all recipes, no training """
        pass

    def recommend(self, numrecs) -> Recipe:
        return choices(self.recipes, k=numrecs)