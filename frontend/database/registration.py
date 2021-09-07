from pymongo import MongoClient, collection
import random

# document information
NAME = "GOF"   # *
AUTH = "c7349"  # *
SCORE = 600
GAMES = 0
HISTORY = []
CHECKSUM = random.randrange(10000, 100000)
SCORE_HISTORY = []

# db information
USER = "Superuser"
PASSWORD = "u9fLzS3kD07"
DB = "HeLO_Scores"
CLUSTER = "Cluster0"
COLLECTION = "scores"

# create client
client = MongoClient(f"mongodb+srv://{USER}:{PASSWORD}@{CLUSTER}.t145g.mongodb.net/{DB}?retryWrites=true&w=majority")
# connect to data base
db = client[DB]
# connect to collection
coll = db[COLLECTION]

# create team document
doc = {
    "name": NAME,
    "auth": AUTH,
    "score": SCORE,
    "games": GAMES,
    "history": HISTORY,
    "checksum": CHECKSUM,
    "score_history": SCORE_HISTORY
}

# insert doc to collection
coll.insert_one(doc)
