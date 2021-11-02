import urllib.request
from PIL import Image

from rand_recommender import RandRecommender
import sys
import json
import ast

  

class Feed:
    def __init__(self, userjson, recijson):
        userfile = open(userjson,)
        self.userdict = json.load(userfile)
        userfile.close()

        recifile = open(recijson,)
        self.recilist = json.loads(recifile.readline())
        recifile.close()

    def update_user_json(self, user_meta_json, rec, user_pref):
        pass

    def display(self, rec):
        print(rec)
        # ph_url = rec.get("photo_url")
        # urllib.request.urlretrieve(ph_url,"f.png")
  
        # img = Image.open("f.png")
        # img.show()

    def save_and_pickle(self, rec, user_meta_json):
        pass

    def start(self):
        print("Welcome to your favorite recipe recommender RecRec: \n" )
        
        #returns name of user_meta_json or empty if not used before
        user_meta_json = self.userdict.get(input("What is you name? \n"))
        #eg. svm, percep, nn...
        rectype = input("What kind of recommeder would you like to use? \n")
                       
        recom = RandRecommender(rectype, user_meta_json, self.recilist)

        if user_meta_json :
            print("Training your recommender from prior prefrences")
            recom.train(user_meta_json)

        print("All ready!")
        
        con = True
        while con:
            rec = recom.recommend(1) 
            self.display(rec)
            user_pref = input("Would you cook this? (y/n) : \n")
            user_meta_json = self.update_user_json(user_meta_json, rec, user_pref)
            con = not (input("Would you like to quit? (q/n) : \n") == 'q')
            recom.train(user_meta_json)
            

        print("Saving your prefrences")
        self.save_and_pickle(rec, user_meta_json)

        print("See you soon")
        

if __name__ == "__main__":
    recijson, userdb = "processed_recipes.json", "users.json"
    f = Feed(userdb, recijson)
    f.start()
