import pymongo
import matplotlib.pyplot as plt
from datetime import datetime, timedelta

MONGO_URL = "mongodb://127.0.0.1:27017/"
DB_NAME = "Restaurants"
COLLECTION_NAME = "power_logs"

client = pymongo.MongoClient(MONGO_URL)
db = client[DB_NAME]
collection = db[COLLECTION_NAME]

def fetch_logs():
    today = datetime.now().date()
    start = datetime.combine(today, datetime.min.time())
    end = datetime.combine(today, datetime.max.time())
    logs = list(collection.find({"timestamp": {"$gte": start, "$lte": end}}).sort("timestamp", 1))
    times = [log["timestamp"] for log in logs]
    cpu = [log["cpu"] for log in logs]
    ram_used = [log["ram_used"] / (1024**3) for log in logs]  # in GB
    ram_total = [log["ram_total"] / (1024**3) for log in logs]  # in GB
    return times, cpu, ram_used, ram_total

def plot_stats():
    times, cpu, ram_used, ram_total = fetch_logs()
    plt.figure(figsize=(12, 6))
    plt.subplot(2, 1, 1)
    plt.plot(times, cpu, label="CPU (%)")
    plt.ylabel("CPU (%)")
    plt.legend()
    plt.subplot(2, 1, 2)
    plt.plot(times, ram_used, label="RAM Used (GB)")
    plt.plot(times, ram_total, label="RAM Total (GB)")
    plt.ylabel("RAM (GB)")
    plt.xlabel("Zeit")
    plt.legend()
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    plot_stats()
