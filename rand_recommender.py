from gui import present
from recommender import Recommender
import numpy as np
import pandas as pd

from os.path import exists


def parse_user_csv(file_name):
    # print('reading csv from ' + file_name)
    try:
        df = pd.read_csv(file_name, index_col=0, header=None)
    except:
        return dict()
    d = {}
    for k, v in df.T.to_dict('list').items():
        d[k] = v[0]
    return d


def open_user_files(user_pref_file_name, recs_file_name):
    file_exists = exists(user_pref_file_name) and exists(recs_file_name)
    if file_exists:
        user_pref = parse_user_csv(user_pref_file_name)
        prior_recs = parse_user_csv(recs_file_name)
    else:
        user_pref = {}
        prior_recs = {}

    pref_file = open(user_pref_file_name, 'a')
    rec_file = open(recs_file_name, 'a')

    return user_pref, prior_recs, pref_file, rec_file


def bool_map(x: bool):
    return 1 if x else -1


class RandRecommender(Recommender):
    def __init__(self, recipes, user_prefs_loc, user_recs_loc):
        """
        initialize a random recipes
        """
        print('Reading recipes')
        print()
        self.data = pd.read_csv(recipes)

        print('Welcome to the random recommender!')
        print()

        # open file
        user_pref, prior_recs, pref_file, rec_file = open_user_files(
            user_prefs_loc, user_recs_loc)

        if len(user_pref) < 50:
            # we want more recs, select 50 recipes

            # IF YOU ARE ACTUALLY LEARNING MAKE SURE YOU
            # REMEMBER WHICH SUBSET OF THE DATA YOU
            # SAMPLED TO LEARN PREFS
            for idx, row in self.data.sample(n=50 - len(user_pref)).iterrows():
                try:
                    print()
                    i_like = present(row)
                    # y_obs is -1, 1
                    y_obs: int = bool_map(i_like)
                    pref_file.write(f'{idx}, {y_obs}\n')
                    user_pref[i_like] = y_obs

                except StopIteration:
                    # present threw an error: close files and stop iteration, then throw another StopIteration to calller
                    pref_file.close()
                    rec_file.close()
                    raise StopIteration

        self.user_pref = user_pref
        self.prior_recs = prior_recs
        self.pref_file = pref_file
        self.rec_file = rec_file
        self.rec_count = 0
        self.rec_queue = []

    def train(self):
        pass

    def description(self):
        return 'A random reccomender.'

    def recommend(self, num_recs):
        return self.data.sample(n=num_recs).iterrows()

    def pop_rec(self):
        NUM_RECS = 20
        if len(self.rec_queue) == 0:
            self.rec_queue = list(self.recommend(NUM_RECS))

        return self.rec_queue.pop(-1)

    def present_recipe(self):
        if self.rec_count % 4 == 0:
            random = True
            idx, row = next(self.data.sample(n=1).iterrows())
        else:
            random = False
            idx, row = self.pop_rec()

        try:
            print()
            i_like = present(row)
            # y_obs is -1, 1
            y_obs: int = bool_map(i_like)
            if random:
                self.pref_file.write(f'{idx}, {y_obs}\n')
                self.user_pref[i_like] = y_obs
            else:
                self.rec_file.write(f'{idx}, {y_obs}\n')
                self.prior_recs[i_like] = y_obs

        except StopIteration:
            # present threw an error: close files and stop iteration, then throw another StopIteration to calller
            self.pref_file.close()
            self.rec_file.close()

            # reccomendation stats are
            print('Rand recommender is quitting. Current stats are:')
            num_yes = 0
            num_total = 0
            for v in self.prior_recs.values():
                num_total += 1
                if v == 1:
                    num_yes += 1

            print(f'Correct recommendations: {num_yes}')
            print(f'Total recommendations: {num_total}')
            print(
                f'Accuracy rate: {num_yes / num_total if num_total > 0 else 0}')

            raise StopIteration

        self.rec_count += 1
