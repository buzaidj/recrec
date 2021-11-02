from abc import ABC, abstractmethod

class Recommender(ABC):
    def __init__(self, rectype, userjson, recilist):
        self.rectype = rectype
        self.userdb = userjson
        self.recipes = recilist

    @abstractmethod
    def train(self, user_meta_json):
        pass
        
    @abstractmethod
    def recommend(self, numrecs):
        pass

