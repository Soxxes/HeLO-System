from pymongo import MongoClient, collection, results
from pymongo.errors import OperationFailure
import random

CLUSTER = "cluster0"
DB_NAME = "gettingStarted"
COLLECTION = "scores"


class AuthError(Exception):
    msg = "Auth failed: authentication code is incorrect"
    
    def __init__(self, *args: object) -> None:
        super().__init__(*args)

    def __str__(self) -> str:
        return self.msg

class ChecksumError(Exception):
    msg = "Incorrect Checksum"
    
    def __init__(self, *args: object) -> None:
        super().__init__(*args)

    def __str__(self) -> str:
        return self.msg

class TeamExistenceError(Exception):
    msg = f"Team doesn't exist. Maybe you misspelled the name."

    def __init__(self, *args: object) -> None:
        super().__init__(*args)

    def __str__(self) -> str:
        return self.msg


class DB:

    # by default, the test data base will be choosed
    def __init__(self, user, pw, cluster=CLUSTER, db=DB_NAME, coll=COLLECTION):
        self.user = user
        self.pw = pw
        self.client = MongoClient(f"mongodb+srv://{self.user}:{self.pw}@{cluster}.t145g.mongodb.net/{db}?retryWrites=true&w=majority")
        self.db = self.client[db]
        self.collection = self.db[coll]

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

    def update(self, name1, name2, auth, new_score1, new_score2, checksum):
        try:
            # auth must match with auth of name1's team
            team1 = self.collection.find_one({"name": name1})
            # oppenent's document
            opp = self.collection.find_one({"name": name2})
            # if checksums don't match return ChecksumError()
            if opp["checksum"] != checksum:
                return ChecksumError()
            if team1["auth"] == auth:
                # -- update documents --
                # update scores
                # team1 update
                f1 = {"name": name1}
                # all "set" updates
                self.collection.update_one(
                    f1,
                    {"$set": {
                        "score": new_score1,
                        "history": self._update_history(name1, name2),
                        "score_history": self._update_score_history(name1)
                    }},
                )
                # increment updates
                self.collection.update_one(
                    f1,
                    {"$inc":
                        {
                            "games": 1
                        }
                    }
                )
                # opponent (team2) update
                f2 = {"name": name2}
                # all "set" updates
                self.collection.update_one(
                    f2,
                    {"$set": {
                        "score": new_score2,
                        "history": self._update_history(name2, name1),
                        "score_history": self._update_score_history(name2)
                    }},
                )
                # increment updates
                self.collection.update_one(
                    f2,
                    {"$inc":
                        {
                            "games": 1
                        }
                    }
                )
                # change opponents checksum
                self._update_checksum(name2)
                return None
            else:
                return AuthError()
        except OperationFailure as e:
            return "User doesn't exist or isn't allowed to to perform that operation."
 
    def check_superuser(self, auth):
        result = self.collection.find_one({"auth": auth})
        if result is None:
            return AuthError()

    def check_auth(self, name, auth):
        result = self.collection.find_one({"name": name})
        if result["auth"] == auth:
            return True
        else:
            return False
    
    def check_coop_checksums(self, names, checksums):
        print("names and checksums:", names, checksums)
        for name, checksum in zip(names, checksums):
            f = {"name": name}
            result = self.collection.find_one(f)
            print(name, checksum)
            print(result["checksum"])
            if result is None or result["checksum"] != int(checksum):
                return False
        return True

    def check_team(self, name):
        result = self.collection.find_one({"name": name})
        if result is None:
            # team doesn't exist
            return False
        else:
            return True

    def get_checksum(self, auth):
        result = self.collection.find_one({"auth": auth})
        return result["checksum"]
        # no AuthError() should be raised here, because this method
        # only gets called when check_superuser() were survived

    def _update_checksum(self, name):
        new_checksum = random.randrange(10000, 100000)
        f = {"name": name}
        self.collection.update_one(f, {"$set": {"checksum": new_checksum}})

    def get_number_of_games(self, name):
        if self.check_team(name):
            result = self.collection.find_one({"name": name})
            return result["games"], None
        return None, TeamExistenceError()

    def _update_number_of_games(self, name):
        f = {"name": name}
        new_val = {"$inc": {"games": 1}}
        self.collection.update_one(f, new_val)

    def get_history(self, name):
        result = self.collection.find_one({"name": name})
        return result["history"]

    def _update_history(self, name, opp_name):
        his = self.get_history(name)
        his.append(opp_name)
        return his

    def get_score_history(self, name):
        result = self.collection.find_one({"name": name})
        return result["score_history"]

    def _update_score_history(self, name):
        score, _ = self.get_score(name)
        his = self.get_score_history(name)
        his.append(score)
        return his

    def update_single(self, name, new_score, opponents):
        # make opponents list to one string
        opps = ", ".join(opponents)
        print("opps: ", opps)
        try:
            f = {"name": name}
            # all "set" updates
            self.collection.update_one(
                f,
                {"$set": {
                    "score": new_score,
                    "history": self._update_history(name, opps),
                    "score_history": self._update_score_history(name)
                }},
            )
            # increment updates
            self.collection.update_one(
                f,
                {"$inc":
                    {
                        "games": 1
                    }
                }
            )
            # change opponents checksums
            for opponent in opponents:
                self._update_checksum(opponent)
            return None
        except OperationFailure as e:
            return "User doesn't exist or isn't allowed to to perform that operation."
 