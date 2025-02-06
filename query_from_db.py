from pymongo import MongoClient
import search_tools

def connect_mongodb():
    client = MongoClient("mongodb://localhost:27017/")  # UPDATE LATER AFTER DEPLOY
    db = client["songs_db"] 
    collection = db["songs_collection"]
    return collection

def get_songs_by_ids(doc_ids):
    collection = connect_mongodb()
    
    results = collection.find({"_id": {"$in": doc_ids}}, {"_id": 1, "song_name": 1, "artist_name": 1, "lyrics": 1, "chords": 1})
    
    return list(results)

json_file = "./song_index.json" #inverted index location
user_query = input("Enter phrase to find: ")

doc_ids = search_tools.search_inverted_index(json_file, user_query)

songs = get_songs_by_ids(doc_ids)

for song in songs:
    print(f"ID: {song['_id']}")
    print(f"Title: {song['song_name']}")
    print(f"Artist: {song['artist_name']}")
    print(f"Chords: {song['chords']}")
    print(f"Lyrics: {song['lyrics'][:111]}...")  # preview 111 chars
    print("=" * 50)