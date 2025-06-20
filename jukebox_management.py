import pymongo

MONGO_URL = "mongodb://127.0.0.1:27017/"
DB_NAME = "jukebox"
COLLECTION_NAME = "songs"

client = pymongo.MongoClient(MONGO_URL)
db = client[DB_NAME]
collection = db[COLLECTION_NAME]

class Song:
    def __init__(self, name, artist, album=None, genre=None, year=None, file=None):
        self.name = name
        self.artist = artist
        self.album = album
        self.genre = genre
        self.year = year
        self.file = file
    def to_dict(self):
        return self.__dict__

def add_song():
    name = input("Name: ")
    artist = input("Interpret: ")
    album = input("Album (optional): ") or None
    genre = input("Genre (optional): ") or None
    year = input("Jahr (optional): ") or None
    file = input("Dateipfad (optional): ") or None
    song = Song(name, artist, album, genre, year, file)
    collection.insert_one(song.to_dict())
    print("Song hinzugefügt.")

def list_songs():
    songs = list(collection.find())
    for i, song in enumerate(songs):
        print(f"{i+1}: {song['name']} - {song['artist']}")
    return songs

def update_song():
    songs = list_songs()
    idx = int(input("Nummer des zu ändernden Songs: ")) - 1
    if idx < 0 or idx >= len(songs):
        print("Ungültige Auswahl.")
        return
    song = songs[idx]
    print("Leerlassen für keine Änderung.")
    name = input(f"Name ({song['name']}): ") or song['name']
    artist = input(f"Interpret ({song['artist']}): ") or song['artist']
    album = input(f"Album ({song.get('album', '')}): ") or song.get('album')
    genre = input(f"Genre ({song.get('genre', '')}): ") or song.get('genre')
    year = input(f"Jahr ({song.get('year', '')}): ") or song.get('year')
    file = input(f"Dateipfad ({song.get('file', '')}): ") or song.get('file')
    collection.update_one({'_id': song['_id']}, {'$set': {'name': name, 'artist': artist, 'album': album, 'genre': genre, 'year': year, 'file': file}})
    print("Song geändert.")

def delete_song():
    songs = list_songs()
    idx = int(input("Nummer des zu löschenden Songs: ")) - 1
    if idx < 0 or idx >= len(songs):
        print("Ungültige Auswahl.")
        return
    song = songs[idx]
    collection.delete_one({'_id': song['_id']})
    print("Song gelöscht.")

def main():
    while True:
        print("1: Song hinzufügen")
        print("2: Song ändern")
        print("3: Song löschen")
        print("4: Songs anzeigen")
        print("0: Beenden")
        choice = input("Auswahl: ")
        if choice == "1":
            add_song()
        elif choice == "2":
            update_song()
        elif choice == "3":
            delete_song()
        elif choice == "4":
            list_songs()
        elif choice == "0":
            break
        else:
            print("Ungültige Auswahl.")

if __name__ == "__main__":
    main()
