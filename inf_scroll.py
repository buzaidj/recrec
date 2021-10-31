import urllib.request
from PIL import Image
from abc import ABC, abstractmethod
  

class Feed:
    def __init__(self, userdb, recidb):
        self.userdb = userdb
        self.recidb = recidb

    def update_user_json(self, user_meta_json, rec, user_pref):
        pass

    def display(self, rec):
        ph_url = rec.get("photo_url")
        urllib.request.urlretrieve(ph_url,"f.png")
  
        img = Image.open("f.png")
        img.show()

    def save_and_pickle(self, rec, user_meta_json):
        pass

    def start(self):
        print("Welcome to your favorite recipe recommender RecRec: \n" )
        
        #returns name of user_meta_json or empty if not used before
        user_meta_json = self.userdb.get(input("What is you name? \n"))
        #eg. svm, percep, nn...
        rectype = input("What kind of recommeder would you like to use? \n")
                       
        recom = Recommender(rectype, user_meta_json, bool(user_meta_json), self.recidb)

        if user_meta_json :
            print("Training your recommender from prior prefrences")
            recom.train(self, user_meta_json)

        print("All ready!")
        
        con = True
        while con:
            rec = recom.recommend(1) 
            self.display(rec)
            user_pref = input("Would you cook this? y/n")
            user_meta_json = self.update_user_json(user_meta_json, rec, user_pref)
            con = not (input("Would you like to quit? q") == 'q')
            recom.train(self, user_meta_json)
            

        print("Saving your prefrences")
        self.save_and_pickle(rec, user_meta_json)

        print("See you soon")
        


class Recommender(ABC):
    def __init__(self, rectype, userjson, recjson):
        self.rectype = rectype
        self.userdb = userjson
        self.recidb = recjson

    @abstractmethod
    def train(self, user_meta_json):
        pass
        
    @abstractmethod
    def recommend(self, numrecs):
        pass
