class Feed:
    def __init__(self, userdb, recidb):
        self.userdb = userdb
        self.recidb = recidb

    def update_user_json(user_meta_json, rec, user_pref):
        pass

    def display(self, rec):
        pass

    def save_and_pickle(self, user_meta_json):
        pass


    def start(self, p, d):
        print("Welcome to your favorite recipe recommender RecRec: \n" )

        
        #returns name of user_meta_json or empty if not used before
        user_meta_json = self.userdb.get(input("What is you name? \n"))
        rectype = input("What kind of recommeder would you like to use? \n")
                
        
        recom = Recommender(rectype, user_meta_json, bool(user_meta_json), self.recidb)

        if(bool(ubool(user_meta_json))):
            print("Training your recommender from prior prefrences")
            recom.train(self, numrecs, user_meta_json)

        print("All ready!")
        
        con = True
        while con
            rec = recom.recommend(1) 
            self.display(rec)
            user_res = input("Would you cook this? y/n")
            user_meta_json = self.update_user_json(user_meta_json, rec, user_pref)
            con = not (input("Would you like to quit? q") == 'q')
            recom.train(self, user_meta_json)
            

        print("Saving your prefrences")
        self.save_and_pickle(rec)

        print("See you soon")
        


class Recommender:
    def __init__(self, rectype, userjson, hasjson):
        self.rectype = rectype
        self.userdb = userdb
        self.recidb = recidb

    @abstractmethod
    def train(self, user_meta_json):
        pass
        
    @abstractmethod
    def recommend(self, numrecs):
        pass
