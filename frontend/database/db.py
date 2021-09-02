from pymongo import MongoClient, collection

CLUSTER = "cluster0"
DB_NAME = "gettingStarted"
COLLECTION = "scores"

class DB:

    def __init__(self, user, pw):
        self.user = user
        self.pw = pw
        self.client = MongoClient(f"mongodb+srv://{self.user}:{self.pw}@{CLUSTER}.t145g.mongodb.net/{DB_NAME}?retryWrites=true&w=majority")
        self.db = self.client[DB_NAME]
        self.collection = self.db[COLLECTION]

    def get_score(self, name):
        result = self.collection.find_one({"name": name})
        return result["score"]

    def update(self, name, auth, new_score):
        # check if auth is correct
        result = self.collection.find_one({"name": name})
        if result["auth"] == auth:
            # filter
            f = {"name": name}
            # set new value
            new_value = {"$set": {"score": new_score}}
            # update document
            self.collection.update_one(f, new_value)
            return True
        else:
            return False

    def update_scores(self, name1, name2, auth, new_score1, new_score2):
        # auth must match with auth of name1's team
        result = self.collection.find_one({"name": name1})
        if result["auth"] == auth:
            # filters
            f1 = {"name": name1}
            f2 = {"name": name2}
            # new values
            new_value1 = {"$set": {"score": new_score1}}
            new_value2 = {"$set": {"score": new_score2}}
            # update documents
            self.collection.update_one(f1, new_value1)
            self.collection.update_one(f2, new_value2)
            return True
        else:
            return False
 