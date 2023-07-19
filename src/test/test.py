from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

uri = "mongodb://localhost:27017/?retryWrites=true&w=majority"
client = MongoClient(uri, server_api=ServerApi('1'))
database = client["OpenAlexEnvironmental"]
collection = database["journals"]

print(f"Total number of Articles: {collection.count_documents({})}")
