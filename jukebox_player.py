import pymongo
import random
import os

MONGO_URL = "mongodb://127.0.0.1:27017/"
DB_NAME = "jukebox"
COLLECTION_NAME = "songs"

client = pymongo.MongoClient(MONGO_URL)
db = client[DB_NAME]
collection = db[COLLECTION_NAME]

playlist = []

def search_songs():
    name = input("Name (optional): ").strip().lower()
    artist = input("Interpret (optional): ").strip().lower()
    album = input("Album (optional): ").strip().lower()
    genre = input("Genre (optional): ").strip().lower()
    query = {}
    if name:
        query["name"] = {"$regex": name, "$options": "i"}
    if artist:
        query["artist"] = {"$regex": artist, "$options": "i"}
    if album:
        query["album"] = {"$regex": album, "$options": "i"}
    if genre:
        query["genre"] = {"$regex": genre, "$options": "i"}
    songs = list(collection.find(query))
    for i, song in enumerate(songs):
        print(f"{i+1}: {song['name']} - {song['artist']}")
    return songs

def add_to_playlist():
    songs = search_songs()
    if not songs:
        print("Keine Songs gefunden.")
        return
    idx = int(input("Nummer des Songs zur Playlist hinzufügen: ")) - 1
    if idx < 0 or idx >= len(songs):
        print("Ungültige Auswahl.")
        return
    playlist.append(songs[idx])
    print("Song zur Playlist hinzugefügt.")

def play_playlist():
    if not playlist:
        # Zufälligen Song abspielen
        all_songs = list(collection.find())
        if not all_songs:
            print("Keine Songs in der Datenbank.")
            return
        song = random.choice(all_songs)
        print(f"Spiele zufälligen Song: {song['name']} - {song['artist']}")
        play_song(song)
        return
    while playlist:
        song = playlist.pop(0)
        print(f"Spiele: {song['name']} - {song['artist']}")
        play_song(song)

def play_song(song):
    file = song.get('file')
    if file and os.path.exists(file):
        try:
            from playsound import playsound
            playsound(file)
        except Exception as e:
            print(f"Fehler beim Abspielen: {e}")
    else:
        print("[Audiofile nicht vorhanden, Dummy-Wiedergabe]")

def main():
    while True:
        print("1: Song suchen und zur Playlist hinzufügen")
        print("2: Playlist abspielen")
        print("0: Beenden")
        choice = input("Auswahl: ")
        if choice == "1":
            add_to_playlist()
        elif choice == "2":
            play_playlist()
        elif choice == "0":
            break
        else:
            print("Ungültige Auswahl.")

if __name__ == "__main__":
    main()
