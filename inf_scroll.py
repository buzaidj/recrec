import urllib.request
from PIL import Image

from rand_recommender import RandRecommender
from os.path import exists

import pandas as pd

import sys
import csv
import json
import ast

  

class Feed:
    def __init__(self, recis):
        self.reci_file = recis

    def update_user_pref(self, user_pref_file_name, rec, pref):
        with open(user_pref_file_name, 'w', newline='') as csvfile:
            

    def display(self, rec):
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

    def rectype_to_rec(self, rectype, user_pref):
        return RandRecommender(user_pref, self.recilist)

    def save(self, user_file, userpref):
        with open(user_file, 'w') as f:
            f.write()

    def user_pref(self):
        pref = input("Would you cook this? (y/n) : \n").lower()
        while not (pref == "y" or pref == "n"):
            print("Please make sure your input is valid")
            pref = input("Would you cook this? (y/n) : \n").lower()
        return pref

    def parse_user_csv(self, user_pref_file_name):

    def start(self):
        print("Welcome to your favorite recipe recommender RecRec: \n" )
        
        name = input("What is your name? \n").strip().lower()
        user_pref_file_name = "user_" + name + ".csv"

        file_exists = exists(user_pref_file_name)
        if file_exists:
            user_pref = parse_user_csv(user_pref_file_name)
        else:
            user_pref = []

        #eg. svm, percep, nn...
        rectype = input("What kind of recommeder would you like to use? \n")
                       
        recom = self.rectype_to_rec(rectype, user_pref)

        print("Training your recommender from prior prefrences")
        recom.train(user_pref)

        print("All ready!")
        
        con = True
        while con:
            rec = recom.recommend(1) 
            self.display(rec[0])
            pref = self.user_pref()
            userpref = self.update_user_pref(user_pref_file_name, rec[0], pref)
            con = not (input("Would you like to quit? (q/n) : \n") == 'q')
            recom.train(userpref)
            

        print("Saving your prefrences")
        self.save(user_pref_file_name, userpref)

        print("See you soon")
        

if __name__ == "__main__":
    recis  = "recipes_with_nutritional_info_prices_time.csv"
    f = Feed(recis)
    f.start()
