from abc import ABC, abstractmethod


class Recommender(ABC):
    def __init__(self, X):
        self.test_X = X

    @abstractmethod
    def train(self, train_X, train_y):
        pass

    @abstractmethod
    def recommend(self, numrecs):
        pass
