"""
A script to get the ranking of all registered teams.
"""

from pandas.core.frame import DataFrame
from pymongo import MongoClient
import pandas as pd

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

all_teams = list()
for x in coll.find({}, {"_id": 0, "name": 1, "score": 1}):
    # add whitespace for better formatting (it's ugly but it's also late while I
    # am writing this)
    all_teams.append((str(x["score"])+" ", x["name"]))

ranked = sorted(all_teams, key=lambda x: x[0], reverse=True)
df = DataFrame(ranked, columns=["score", "name"])
print(df)
df.to_csv("ranking.txt", sep="\t", mode="w")
