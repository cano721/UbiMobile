from pymongo import MongoClient

# mongo_uri = "mongodb://192.168.200.198:27017"
# client = MongoClient(mongo_uri)
client = MongoClient("192.168.200.127", 27017)
print(client.list_database_names())

db = client["mydb"]
print(db.list_collection_names())

my_collection = db["exam"]
print(my_collection.name)

result = my_collection.find_one()
print(result)
