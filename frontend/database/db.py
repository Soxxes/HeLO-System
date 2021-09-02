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
