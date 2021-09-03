from pymongo import MongoClient, collection
from pymongo.errors import OperationFailure

CLUSTER = "cluster0"
DB_NAME = "gettingStarted"
COLLECTION = "scores"


class AuthError(Exception):
    msg = "Auth failed: authentication code is incorrect"
    
    def __init__(self, *args: object) -> None:
        super().__init__(*args)

    def __str__(self) -> str:
        return self.msg


class DB:

    def __init__(self, user, pw):
        self.user = user
        self.pw = pw
        self.client = MongoClient(f"mongodb+srv://{self.user}:{self.pw}@{CLUSTER}.t145g.mongodb.net/{DB_NAME}?retryWrites=true&w=majority")
        self.db = self.client[DB_NAME]
        self.collection = self.db[COLLECTION]

    def get_score(self, name):
        try:
            result = self.collection.find_one({"name": name})
            # if result is None, no document were found
            if result is not None:
                return result["score"], None
            else:
                return None, f"No document named {name} found in data base."
        except OperationFailure as e:
            return None, "User doesn't exist or isn't allowed to to perform that operation."

    def update(self, name, auth, new_score):
        # check if auth is correct
        result = self.collection.find_one({"name": name})
        if result["auth"] == auth:
            # filter
            f = {"name": name}
            # set new value
            new_value = {"$set": {"score": new_score}}
            try:
                # update document
                self.collection.update_one(f, new_value)
                return None
            except OperationFailure as e:
                return e
        else:
            return AuthError()

    def update_scores(self, name1, name2, auth, new_score1, new_score2):
        try:
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
                return None
            else:
                return AuthError()
        except OperationFailure as e:
            return "User doesn't exist or isn't allowed to to perform that operation."
 
    def check_superuser(self, auth):
        result = self.collection.find_one({"auth": auth})
        if result is None:
            return AuthError()
