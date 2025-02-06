import json
from pymongo import MongoClient

# connect to local mongo
client = MongoClient("mongodb://localhost:27017/") 
db = client["songs_db"]
collection = db["songs_collection"]

with open("for_db.json", "r") as file:
    data = json.load(file)

for key, record in data.items():
    record["_id"] = key 
    collection.insert_one(record)

print("JSON data successfully loaded")