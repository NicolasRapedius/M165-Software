import pymongo
from PIL import Image, ImageDraw

MONGO_URL = "mongodb://127.0.0.1:27017/"
DB_NAME = "Restaurants"
COLLECTION_NAME = "neighborhoods"

client = pymongo.MongoClient(MONGO_URL)
db = client[DB_NAME]
collection = db[COLLECTION_NAME]

# Hilfsfunktion zum Skalieren der Koordinaten auf Bildgröße
def scale_coords(coords, img_size):
    # coords: Liste von Polygonen (Ringen), jeder Ring ist eine Liste von [x, y]
    flat = [pt for ring in coords for pt in ring]
    # Sicherstellen, dass pt eine Liste mit 2 Elementen ist
    xs = [pt[0] for pt in flat]
    ys = [pt[1] for pt in flat]
    min_x, max_x = min(xs), max(xs)
    min_y, max_y = min(ys), max(ys)
    def scale(pt):
        x, y = pt[0], pt[1]
        sx = int((x - min_x) / (max_x - min_x) * (img_size[0] - 20) + 10) if max_x > min_x else img_size[0] // 2
        sy = int((y - min_y) / (max_y - min_y) * (img_size[1] - 20) + 10) if max_y > min_y else img_size[1] // 2
        return (sx, img_size[1] - sy)
    return [[scale(pt) for pt in ring] for ring in coords]

def draw_single_polygon():
    doc = collection.find_one()
    if not doc:
        print("No polygon found.")
        return
    coords = doc["geometry"]["coordinates"]
    img = Image.new("RGB", (400, 400), "white")
    draw = ImageDraw.Draw(img)
    scaled = scale_coords(coords, img.size)
    for ring in scaled:
        draw.polygon(ring, outline="blue", fill=None)
    img.show()

def draw_all_polygons():
    docs = list(collection.find())
    if not docs:
        print("No polygons found.")
        return
    all_coords = [ring for doc in docs for ring in doc["geometry"]["coordinates"]]
    img = Image.new("RGB", (400, 400), "white")
    draw = ImageDraw.Draw(img)
    scaled = scale_coords(all_coords, img.size)
    for ring in scaled:
        draw.polygon(ring, outline="red", fill=None)
    img.show()

if __name__ == "__main__":
    print("1: Ein Polygon zeichnen")
    print("2: Alle Polygone zeichnen")
    choice = input("Auswahl: ")
    if choice == "1":
        draw_single_polygon()
    else:
        draw_all_polygons()
