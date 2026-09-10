from pymongo import MongoClient

mongo_client: MongoClient = MongoClient(
    "mongodb://admin:admin@mongo:27017")
