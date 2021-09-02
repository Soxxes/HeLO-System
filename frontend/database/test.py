from pymongo import MongoClient
import certifi

#client = MongoClient("mongodb+srv://Marc:<password>@cluster0.t145g.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
#client = MongoClient("mongodb+srv://Marc:jK5%oWq@cluster0.t145g.mongodb.net/gettingStarted?retryWrites=true&w=majority", tlsCAFile=certifi.where())
client = MongoClient("mongodb+srv://Marc:jK5%oWq@cluster0.t145g.mongodb.net/gettingStarted?retryWrites=true&w=majority")
# creates a new database on the cluster
db = client.gettingStarted

# creates a new collection
scores = db.scores

# first document to insert into the collection
# first_doc = {
#     "name": "CoRe",
#     "auth": "235711",
#     "score": 847
# }

# insert doc to collection
# scores.insert_one(first_doc)

# access docs
for doc in db.scores.find():
    print(doc["name"])
