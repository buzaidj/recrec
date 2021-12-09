from abc import ABC, abstractmethod

class Recommender(ABC):
    def __init__(self, recilist):
        self.recipes = recilist

    @abstractmethod
    def train(self, user_prefs):
        pass
        
    @abstractmethod
    def recommend(self, numrecs):
        pass

