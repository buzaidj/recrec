from numpy.lib.function_base import append
from gui import present, recipe_steps
from recommender import Recommender
import numpy as np
import pandas as pd
from sklearn.neighbors import KNeighborsClassifier
from sklearn.preprocessing import StandardScaler

from os.path import exists

REQD_RATINGS = 15
NUM_NEIGH = 7


def cols_with_underscore(df):
    return [col for col in df.columns if col[0] == '_']


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


class Knn(Recommender):
    def __init__(self, recipes, user_prefs_loc, user_recs_loc):
        """
        initialize a random recipes
        """
        print('Reading recipes' + '\n')
        self.X = pd.read_csv(recipes)

        print('Welcome to the K-Nearest Neighbors recommender!' + '\n')

        # open file
        user_pref, prior_recs, pref_file, rec_file = open_user_files(
            user_prefs_loc, user_recs_loc)

        # testX is all the X we haven't trained on yet or presented
        self.testX = self.X.drop(user_pref.keys()).drop(prior_recs.keys())
        self.recX = self.X.loc[list(prior_recs.keys())]
        # print(user_pref.keys())

        self.stdC = StandardScaler()
        # don't use the website field
        self.trainX = self.X.loc[user_pref.keys()].drop(
            columns=cols_with_underscore(self.X)).drop(columns=['website']).to_numpy()

        print(self.trainX)

        self.trainX_std = np.array([[]])
        if self.trainX.any():
            self.stdC.partial_fit(self.trainX)
            self.trainX_std = self.stdC.transform(self.trainX) 

        self.trainy = np.array(list(user_pref.values()))


        self.neigh = KNeighborsClassifier(n_neighbors=NUM_NEIGH)

        self.user_pref = user_pref
        self.prior_recs = prior_recs
        self.pref_file = pref_file
        self.rec_file = rec_file

        self.rec_count = 0

    def train(self):
        self.neigh.fit(self.trainX_std, self.trainy)

    def description(self):
        # TODO : add a better description
        return 'A K-Nearest Neighbor classifier'

    def recommend(self, num_recs):
        testXinput = self.stdC.transform(np.array(self.testX.drop(columns=['website']).drop(
            columns=cols_with_underscore(self.testX))))
        preds = self.neigh.predict(testXinput)
        ## edge case if user has only choosen one category in training(n,n,n...) then this will fail
        probs = self.neigh.predict_proba(testXinput)[:,1]
        predsY = pd.Series(preds, index=self.testX.index)
        proby = pd.Series(probs, index=self.testX.index)
        greater_then_zero = np.array(predsY[predsY > 0].index)
        greater_then_zero_prob = np.array(proby[predsY > 0])
        inds = np.argsort(-1*greater_then_zero_prob)
        predsindex = greater_then_zero[inds]
        print(predsindex)
        return predsindex[:num_recs] 

    def present_recipe(self):
        try:
            if self.rec_count % 4 == 0:
                self.present_train(1)
            else:
                self.present_rec(1)

        except StopIteration:
            # reccomendation stats are
            print('Recommender is quitting. Current stats are:')
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

    def present_rec(self, num):
        """
        present recipes to test on, updating
        """
        self.train()
        for _ in range(num):
            lr = self.recommend(1)
            while not lr.any():
                self.present_train(1)
                lr = self.recommend(1)
                self.train()
            idx = self.recommend(1)[0]
            rec = self.testX.loc[idx]
            self.testX = self.testX.drop(idx)
            try:
                i_like = present(rec)
                if i_like:
                    recipe_steps(rec)
                y_obs = bool_map(i_like)
                self.rec_file.write(f'{idx}, {y_obs}\n')
                self.prior_recs[idx] = y_obs

            except StopIteration:
                self.rec_file.close()
                self.pref_file.close()
                raise StopIteration

    def present_train(self, num):
        """
        present recipes to train on, updating train data accordingly and removing it from test data
        """
        if len(self.user_pref) < REQD_RATINGS:
            # we want more recs, select 50 recipes

            # IF YOU ARE ACTUALLY LEARNING MAKE SURE YOU
            # REMEMBER WHICH SUBSET OF THE DATA YOU
            # SAMPLED TO LEARN PREFS
            num = REQD_RATINGS - len(self.user_pref)

        for idx, row in self.testX.sample(n=num).iterrows():
            try:
                # print(self.trainX)
                # print(row)
                i_like = present(row)
                if i_like:
                    recipe_steps(row)
                y_obs: int = bool_map(i_like)
                self.pref_file.write(f'{idx}, {y_obs}\n')
                self.user_pref[idx] = y_obs
                self.testX = self.testX.drop(idx)
                row_arr = np.array(row.drop(
                    labels=cols_with_underscore(self.testX)).drop(labels=['website']))
                self.stdC.partial_fit([row_arr])
                if self.trainX_std.size > 0 :
                    self.trainX_std = np.vstack([self.trainX_std, self.stdC.transform([row_arr])[0]])
                else:
                    self.trainX_std = np.array([self.stdC.transform([row_arr])[0]])
                # print(self.trainX)
                self.trainy = np.append(self.trainy, y_obs)
                print(self.trainX_std.shape, self.trainy)

            except StopIteration:
                # present threw an error: close files and stop iteration, then throw another StopIteration to calller
                self.pref_file.close()
                self.rec_file.close()
                raise StopIteration
