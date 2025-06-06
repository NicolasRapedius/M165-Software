import pymongo
from bson import ObjectId

class Dao_joke:
    def __init__(self, db_url="mongodb://127.0.0.1:27017/", db_name="jokes_db"):
        self.client = pymongo.MongoClient(db_url)
        self.db = self.client[db_name]
        self.collection = self.db["jokes"]

    def insert(self, text, category, author):
        joke = {
            "text": text,
            "category": category,  # expects a list
            "author": author
        }
        return self.collection.insert_one(joke).inserted_id

    def get_category(self, category):
        return list(self.collection.find({"category": category}))

    def delete(self, joke_id):
        return self.collection.delete_one({"_id": ObjectId(joke_id)}).deleted_count

    def update(self, joke_id, text=None, category=None, author=None):
        update_fields = {}
        if text is not None:
            update_fields["text"] = text
        if category is not None:
            update_fields["category"] = category
        if author is not None:
            update_fields["author"] = author
        if update_fields:
            return self.collection.update_one({"_id": ObjectId(joke_id)}, {"$set": update_fields}).modified_count
        return 0
