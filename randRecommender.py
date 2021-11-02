class RandRecommender(Recommender):
    def __init__(self, rectype, userjson, recjson):
        super().__init__(rectype, userjson, recjson)

    def train(self, user_meta_json):
        pass
        
    def recommend(self, numrecs):
        self.recjson
        pass