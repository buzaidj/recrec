from matplotlib.colors import Normalize
from sklearn import tree
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.neighbors import KNeighborsClassifier
import pandas as pd
import numpy as np
from sklearn import preprocessing

import matplotlib.pyplot as plt

std_scaler = preprocessing.StandardScaler()


def cols_with_title_ingr(df):
    return [col for col in df.columns if '::' in col]


def cols_with_underscores(df):
    return [col for col in df.columns if col[0] == '_']


def cols_to_drop(df):
    return cols_with_underscores(df) + cols_with_title_ingr(df)


"""
Goal to train first on 20, then 30, then 40, and so forth and see how accuracy imporves
"""
user = 'greg_test'
name = 'KNN'

models_to_run = [
    (DecisionTreeClassifier(
        random_state=0, ccp_alpha=0.030), 'Decision Tree [alpha = 0.030]', False),
    (DecisionTreeClassifier(
        random_state=0, ccp_alpha=0.015), 'Decision Tree [alpha = 0.015]', False),
    (DecisionTreeClassifier(
        random_state=0, ccp_alpha=0.000), 'Decision Tree [alpha = 0.000]', False),
    (KNeighborsClassifier(
        n_neighbors=11), 'KNeighbors Classifier [neighbors = 11]', True),
    (KNeighborsClassifier(
        n_neighbors=5), 'KNeighbors Classifier [neighbors = 5]', True),
    (KNeighborsClassifier(
        n_neighbors=3), 'KNeighbors Classifier [neighbors = 3]', True),
    (KNeighborsClassifier(
        n_neighbors=1), 'KNeighbors Classifier [neighbors = 1]', True),
]


def parse_user_csv(file_name):
    # print('reading csv from ' + file_name)
    try:
        df = pd.read_csv(file_name, index_col=0, header=None)
    except Exception as e:
        print(e)
        return dict()
    d = {}
    for k, v in df.T.to_dict('list').items():
        d[k] = v[0]
    return d


curr_prefs = parse_user_csv('users/user_' + user + '.csv')
data = pd.read_csv('data.csv')


def random_classify(train_y, test_y):
    # try to predict test_y randomly
    pct_pos = len(train_y[np.where(train_y == 1)]) / len(train_y)

    # how to calculate expected number of correct guesses

    expected_correct = 0
    for y in test_y:
        if y == 1:
            expected_correct += pct_pos
        else:
            expected_correct += (1 - pct_pos)

    return expected_correct / len(test_y)


def train(clf, train_X, train_y):

    return clf.fit(train_X, train_y)


for clf, name, to_normalize in models_to_run:
    observed = data.loc[curr_prefs.keys()]
    ys = pd.Series(curr_prefs)

    observed = observed.drop(
        columns=cols_to_drop(observed)).drop(columns=['website'])

    accuracy_measurements = {}
    rand_accuracy = {}

    idx = 20, 40, 60, 80, 100, 120, 140, 160

    for i in idx:
        train_X = observed.iloc[:i].to_numpy()
        train_y = ys.iloc[:i].to_numpy()

        test_X = observed.iloc[i:i+50].to_numpy()
        test_y = ys.iloc[i:i+50].to_numpy()

        if to_normalize:
            train_X = std_scaler.fit_transform(train_X)
            test_X = std_scaler.transform(test_X)

        clf = train(clf, train_X, train_y)
        actual_acc = clf.score(test_X, test_y)
        expected_random_acc = random_classify(train_y, test_y)

        accuracy_measurements[i] = actual_acc
        rand_accuracy[i] = expected_random_acc

    accuracy_measurements = pd.Series(accuracy_measurements)
    rand_accuracy = pd.Series(rand_accuracy)

    fig = plt.figure()
    ax1 = fig.add_subplot(111)

    acc = list(accuracy_measurements)
    rand_acc = list(rand_accuracy)
    idx = idx

    ax1.scatter(idx, rand_acc, s=10, c='b',
                marker='s', label='Random accuracy')
    ax1.scatter(idx, acc, s=10, c='r', marker="o", label='Model accuracy')
    plt.title(name)
    plt.legend(loc='upper left')
    # plt.show()
    fig.savefig('graphs/' + name + '.png', dpi=150)

    if to_normalize == False:
        fig = plt.figure(figsize=(50, 40))
        plt.title(name)
        _ = tree.plot_tree(clf,
                           feature_names=list(data.columns),
                           class_names=['No', 'Yes'],
                           filled=True)

        fig.savefig('trees/' + name + '.png')
