import pymongo
from bson import ObjectId
from datetime import datetime

def print_districts(neighborhoods_collection):
    districts = neighborhoods_collection.distinct("borough")
    if not districts:
        print("Keine Stadtbezirke gefunden. Beispiel-Dokument aus 'neighborhoods':")
        beispiel = neighborhoods_collection.find_one()
        print(beispiel)
        return
    print("Stadtbezirke:")
    for d in districts:
        print(f" - {d}")

def print_top3_restaurants(collection):
    pipeline = [
        {"$unwind": "$grades"},
        {"$group": {
            "_id": "$_id",
            "name": {"$first": "$name"},
            "avgScore": {"$avg": "$grades.score"}
        }},
        {"$sort": {"avgScore": -1}},
        {"$limit": 3}
    ]
    print("Top 3 Restaurants nach Durchschnitts-Score:")
    for r in collection.aggregate(pipeline):
        print(f"{r['name']} (Ø Score: {r['avgScore']:.2f})")

def find_nearest_restaurant(collection):
    le_perigord = collection.find_one({"name": "Le Perigord"})
    if not le_perigord or not le_perigord.get("address") or not le_perigord["address"].get("coord"):
        print("Le Perigord oder Koordinaten nicht gefunden.")
        return
    coords = le_perigord["address"]["coord"]
    nearest = collection.find({
        "address.coord": {
            "$near": {
                "$geometry": {
                    "type": "Point",
                    "coordinates": coords
                }
            }
        },
        "name": {"$ne": "Le Perigord"}
    }).limit(1)
    print("Nächstgelegenes Restaurant zu Le Perigord:")
    for r in nearest:
        print(f"{r['name']} ({r['address']['coord']})")

def search_restaurants(collection):
    name = input("Name (optional): ").strip()
    cuisine = input("Küche (optional): ").strip()
    query = {}
    if name:
        query["name"] = {"$regex": name, "$options": "i"}
    if cuisine:
        query["cuisine"] = {"$regex": cuisine, "$options": "i"}
    results = list(collection.find(query))
    if not results:
        print("Keine Restaurants gefunden.")
        return None
    print("Suchergebnisse:")
    for idx, r in enumerate(results):
        print(f"{idx+1}: {r['name']} ({r['cuisine']}) - ID: {r['_id']}")
    if len(results) == 1:
        return results[0]["_id"]
    sel = input("Nummer des Restaurants für Bewertung auswählen (Enter für Abbruch): ").strip()
    if sel.isdigit() and 1 <= int(sel) <= len(results):
        return results[int(sel)-1]["_id"]
    return None

def add_rating(collection, rest_id):
    try:
        score = int(input("Score (0-10): "))
        if not (0 <= score <= 10):
            print("Ungültiger Score.")
            return
    except ValueError:
        print("Ungültige Eingabe.")
        return
    grade = {
        "date": datetime.now(),
        "score": score
    }
    result = collection.update_one(
        {"_id": rest_id},
        {"$push": {"grades": grade}}
    )
    if result.modified_count:
        print("Bewertung hinzugefügt.")
    else:
        print("Fehler beim Hinzufügen der Bewertung.")

def main():
    client = pymongo.MongoClient("mongodb://127.0.0.1:27017/")
    db = client["Restaurants"]  # Datenbankname angepasst
    restaurants_collection = db["restaurants"]
    neighborhoods_collection = db["neighborhoods"]

    while True:
        print("\n1) Stadtbezirke anzeigen")
        print("2) Top 3 Restaurants")
        print("3) Nächstgelegenes Restaurant zu Le Perigord")
        print("4) Restaurant suchen und bewerten")
        print("0) Beenden")
        choice = input("Auswahl: ").strip()
        if choice == "1":
            print_districts(neighborhoods_collection)
        elif choice == "2":
            print_top3_restaurants(restaurants_collection)
        elif choice == "3":
            find_nearest_restaurant(restaurants_collection)
        elif choice == "4":
            rest_id = search_restaurants(restaurants_collection)
            if rest_id:
                add_rating(restaurants_collection, rest_id)
        elif choice == "0":
            break
        else:
            print("Ungültige Auswahl.")

if __name__ == "__main__":
    main()
