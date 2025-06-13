import pymongo
import os

MONGO_URL = "mongodb://127.0.0.1:27017/"
client = pymongo.MongoClient(MONGO_URL)

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def wait_for_key():
    input("\nPress any button to return...")

def list_databases():
    dbs = client.list_database_names()
    if not dbs:
        print("No Database")
        wait_for_key()
        return None
    print("Databases")
    for db in dbs:
        print(f" - {db}")
    return dbs

def list_collections(db_name):
    db = client[db_name]
    cols = db.list_collection_names()
    if not cols:
        print("No Collection")
        wait_for_key()
        return None
    print(f"\n{db_name}\n")
    print("Collections")
    for col in cols:
        print(f" - {col}")
    return cols

def list_documents(db_name, col_name):
    col = client[db_name][col_name]
    docs = list(col.find({}, {"_id": 1}))
    if not docs:
        print("No Document")
        wait_for_key()
        return None
    print(f"\n{db_name}.{col_name}\n")
    print("Documents")
    for doc in docs:
        print(f" - {str(doc['_id'])[:7]}")
    return docs

def show_document(db_name, col_name, doc_id):
    col = client[db_name][col_name]
    from bson.objectid import ObjectId
    try:
        doc = col.find_one({"_id": ObjectId(doc_id)})
    except Exception:
        doc = None
    print(f"\n{db_name}.{col_name}.{doc_id}\n")
    if not doc:
        print("No Document")
        wait_for_key()
        return
    for k, v in doc.items():
        print(f"{k}: {v}")
    wait_for_key()

def main():
    while True:
        clear_screen()
        dbs = list_databases()
        if not dbs:
            continue
        db_name = input("\nSelect Database: ")
        if db_name not in dbs:
            print("Database not found!")
            wait_for_key()
            continue
        clear_screen()
        cols = list_collections(db_name)
        if not cols:
            continue
        col_name = input("\nSelect Collection: ")
        if col_name not in cols:
            print("Collection not found!")
            wait_for_key()
            continue
        clear_screen()
        docs = list_documents(db_name, col_name)
        if not docs:
            continue
        doc_id = input("\nSelect Document (ID): ")
        # Try to match by prefix
        match = [d for d in docs if str(d['_id']).startswith(doc_id)]
        if not match:
            print("Document not found!")
            wait_for_key()
            continue
        show_document(db_name, col_name, str(match[0]['_id']))

if __name__ == "__main__":
    main()
