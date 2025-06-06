import pymongo
import gridfs
import os

MONGO_URL = os.environ.get("MONGO_URL", "mongodb://127.0.0.1:27017/")
DB_NAME = "photo_album"

client = pymongo.MongoClient(MONGO_URL)
db = client[DB_NAME]
fs = gridfs.GridFS(db)

def upload_photo(file_path, album_name):
    with open(file_path, "rb") as f:
        data = f.read()
        filename = os.path.basename(file_path)
        file_id = fs.put(data, filename=filename, album=album_name)
        print(f"Foto '{filename}' wurde dem Album '{album_name}' hinzugefügt. (ID: {file_id})")

def download_photos(album_name, download_dir):
    os.makedirs(download_dir, exist_ok=True)
    for grid_out in fs.find({"album": album_name}):
        out_path = os.path.join(download_dir, grid_out.filename)
        with open(out_path, "wb") as f:
            f.write(grid_out.read())
        print(f"Foto '{grid_out.filename}' aus Album '{album_name}' gespeichert unter {out_path}")

def list_albums():
    albums = db.fs.files.distinct("album")
    print("Verfügbare Alben:")
    for a in albums:
        print(f"- {a}")

def main():
    while True:
        print("\n1) Foto hochladen")
        print("2) Fotos eines Albums herunterladen")
        print("3) Alben anzeigen")
        print("0) Beenden")
        choice = input("Auswahl: ").strip()
        if choice == "1":
            file_path = input("Pfad zum Bild: ").strip()
            album = input("Album-Name: ").strip()
            upload_photo(file_path, album)
        elif choice == "2":
            album = input("Album-Name: ").strip()
            download_dir = input("Zielordner: ").strip()
            download_photos(album, download_dir)
        elif choice == "3":
            list_albums()
        elif choice == "0":
            break
        else:
            print("Ungültige Auswahl.")

if __name__ == "__main__":
    main()
