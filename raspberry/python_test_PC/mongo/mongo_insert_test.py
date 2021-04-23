from pymongo import MongoClient

# mongo_uri = "mongodb://192.168.200.198:27017"
# client = MongoClient(mongo_uri)
client = MongoClient("192.168.200.127", 27017)
print(client.list_database_names())

db = client["mydb"]
my_collection = db["exam"]

# result = my_collection.insert_one({"name": "장동건", "age": 40, "subject": ["java", "python"]})
my_data = [
    {"name": "이민호", "age": 40, "subject": ["java", "python"]},
    {"name": "김어준", "age": 40, "subject": ["raspberry", "python"]},
    {"name": "장동건", "age": 40, "subject": ["mongo", "python"]},
]
result = my_collection.insert_many(my_data)
print(result)
