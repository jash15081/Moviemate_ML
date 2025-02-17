from pymongo import MongoClient

client = MongoClient("mongodb+srv://chintan:chintan123@cluster0.i5cai.mongodb.net")
db = client["moviemate"]
movies_collection = db["movies"]
ratings_collection = db["reviews"]
users_collection = db["users"]
