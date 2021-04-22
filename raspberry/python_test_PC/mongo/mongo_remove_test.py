from pymongo import MongoClient

# mongo_uri = "mongodb://192.168.200.198:27017"
# client = MongoClient(mongo_uri)
client = MongoClient("192.168.200.127", 27017)
print(client.list_database_names())

db = client["mydb"]
my_collection = db["exam"]

result = my_collection.remove({"java": {"$gt": 90}})
print(result)
