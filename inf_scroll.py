import urllib.request
from PIL import Image

from rand_recommender import RandRecommender
from os.path import exists
from sys import exit

import os

import pandas as pd

from recommender import Recommender

RECIPE_CSV = 'recipes_with_nutritional_info_prices_time.csv'


class Feed:
    def __init__(self, recipes_filename):
        self.reci_df = pd.read_csv(recipes_filename)

    def display(self, rec):
        raise NotImplemented
        # print(rec["title"])

        # # print("Cook time in minutes: " + str(rec["total_time_minutes"]))

        # print("You will need, ingredients:")
        # for ing in rec["ingredients"]:
        #     print(ing["text"])

        # print("Instructions:")
        # for ins in rec["instructions"]:
        #     print(ins["text"])

        # # ph_url = rec.get("photo_url")
        # # urllib.request.urlretrieve(ph_url,"f.png")

        # # img = Image.open("f.png")
        # # img.show()

    def get_recommender(self, name,  model_type, recipes) -> Recommender:
        """
        return a Recommender from the inputted [model_type] string
        """
        user_file_name = os.path.join('users', 'user_' + name + '.csv')
        recs_file_name = os.path.join(
            'recs', 'recs_' + model_type + '_' + name + '.csv')

        if model_type == 'rand':
            print('hello')
            return RandRecommender(recipes, user_file_name, recs_file_name)

        if model_type == 'dtree':
            # TODO: implement dtree class
            user_file_name = name + '_'
            pass
        # TODO: add other model types here

    def run(self):
        name = input("What is your name? \n").strip().lower()
        user_pref_file_name = "user_" + name + ".csv"

        model_type = input(
            'Which model would you like to use? See readme.txt for a list of model types. \n').strip().lower()

        # recommender may ask a new user to rate 50-100 recipies to get an idea of their preferences
        try:
            recommender = self.get_recommender(name, model_type, RECIPE_CSV)
        except StopIteration:
            print('I hope you found good recipes!')
            exit()

        print()
        print('You chose recommender: ' + recommender.description())
        print()
        print('I will now begin recommending recipes and occasionally present random ones to get a better understanding of your tastes. Type q to quit and stop recommending.')

        # loop and present recipes until user quits
        while True:
            try:
                recommender.present_recipe()
            except StopIteration:
                break

        print('I hope you found good recipes!')

    def start(self):
        print("Welcome to your favorite recipe recommender RecRec: \n")
        self.run()


if __name__ == "__main__":
    recis = "recipes_with_nutritional_info_prices_time.csv"
    f = Feed(recis)
    f.start()
