import urllib.request
from PIL import Image

from rand_recommender import RandRecommender
import sys
import json
import ast

  

class Feed:
    def __init__(self, userjson, recijson):
        self.userjson = userjson
        userfile = open(userjson,)
        self.userdict = json.load(userfile)
        userfile.close()

        recifile = open(recijson,)
        self.recilist = json.loads(recifile.readline())
        recifile.close()

    def update_user_json(self, userpref, rec, pref):
        print(userpref)
        if userpref:
            recipes = userpref["recipes"]
            recipes["titles"] += [rec["title"]]
            recipes["authors"] += [rec["author"]]
            userpref["prefrences"] += pref
        else:
            recipes = {}
            recipes["titles"] = [rec["title"]]
            recipes["authors"] = [rec["author"]]
            userpref["prefrences"] = pref
            
        userpref["recipes"] = recipes 
        print(userpref)
        return userpref

    def display(self, rec):
        print(rec)
        ph_url = rec[0].get("photo_url")
        urllib.request.urlretrieve(ph_url,"f.png")
  
        img = Image.open("f.png")
        img.show()

    def rectype_to_rec(self, rectype, user_meta_json):
        return RandRecommender(user_meta_json, self.recilist)

    def save(self, user_file, userpref):
        with open(user_file, 'w') as f:
            f.write(json.dumps(userpref))

    def start(self):
        print("Welcome to your favorite recipe recommender RecRec: \n" )
        
        #returns name of user_meta_json or empty if not used before
        name = input("What is you name? \n").strip().lower()
        user_pref_file_name = self.userdict.get(name)

        if user_pref_file_name:
            userfile = open(user_pref_file_name,)
            userpref = json.load(userfile)
            userfile.close()
            
        else:
            user_pref_file_name = "user_" + name + ".json"
            self.userdict[name] = user_pref_file_name
            with open(self.userjson, 'w') as f:
                f.write(json.dumps(self.userdict))
            userpref = {}

        #eg. svm, percep, nn...
        rectype = input("What kind of recommeder would you like to use? \n")
                       
        recom = self.rectype_to_rec(rectype, userpref)
        print("Training your recommender from prior prefrences")
        recom.train(userpref)

        print("All ready!")
        
        con = True
        while con:
            rec = recom.recommend(1) 
            self.display(rec)
            pref = input("Would you cook this? (y/n) : \n")
            userpref = self.update_user_json(userpref, rec[0], pref)
            con = not (input("Would you like to quit? (q/n) : \n") == 'q')
            recom.train(userpref)
            

        print("Saving your prefrences")
        self.save(user_pref_file_name, userpref)

        print("See you soon")
        

if __name__ == "__main__":
    recijson, userdb = "processed_recipes.json", "users.json"
    f = Feed(userdb, recijson)
    f.start()
