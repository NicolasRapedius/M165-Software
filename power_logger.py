import time
import pymongo
from Power import Power

MONGO_URL = "mongodb://127.0.0.1:27017/"
DB_NAME = "Restaurants"
COLLECTION_NAME = "power_logs"
MAX_LOGS = 10000

client = pymongo.MongoClient(MONGO_URL)
db = client[DB_NAME]
collection = db[COLLECTION_NAME]

def maintain_log_limit():
    count = collection.count_documents({})
    if count > MAX_LOGS:
        to_delete = count - MAX_LOGS
        oldest = collection.find().sort("timestamp", 1).limit(to_delete)
        ids = [doc["_id"] for doc in oldest]
        collection.delete_many({"_id": {"$in": ids}})

def main():
    while True:
        power = Power()
        collection.insert_one(power.to_dict())
        maintain_log_limit()
        time.sleep(1)

if __name__ == "__main__":
    main()
