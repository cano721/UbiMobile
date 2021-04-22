from pymongo import MongoClient

# mongo_uri = "mongodb://192.168.200.198:27017"
# client = MongoClient(mongo_uri)
client = MongoClient("192.168.200.127", 27017)
print(client.list_database_names())

db = client["mydb"]
my_collection = db["exam"]

print("==================================================")
list_data = my_collection.find()
for my_doc in list_data:
    print(my_doc)

print("==================================================")
list_data = my_collection.find().sort("name", 1)
for my_doc in list_data:
    print(my_doc)

print("==================================================")
my_query = {"java": {"$gt": 90}}
list_data = my_collection.find(my_query)
for my_doc in list_data:
    print(my_doc)

print("==================================================")
my_query = {"addr": "인천"}
list_data = my_collection.find(my_query)
for my_doc in list_data:
    print(my_doc)
