from typing_extensions import TypeAlias
from process import Recommender
from typing import List
from random import choice

Recipe = dict


class RandRecommender(Recommender):
    def __init__(self, rectype, userjson, recipes: List[Recipe]):
        super().__init__(rectype, userjson, recipes)

    def train(self, user_meta_json):
        """ just selects a random recipe over all recipes, no training """
        pass

    def recommend(self, numrecs) -> Recipe:
        return choice(self.recipes, k=numrecs)
