import pymongo
from src.error import IS_ERROR


class Database:
    def __init__(self):
        self.client = pymongo.MongoClient("mongodb://localhost:27017/")
        self.db = self.client["humblebee"]


    def register(self, collection_name: str, data: dict, is_hive: bool = False) -> str:
        collection = self.db[collection_name]
        if is_hive and collection.find_one({"hiveId": data["hiveId"]}):
            raise ValueError(IS_ERROR["HIVE_ALREADY_EXISTS"]["message"])
        result = collection.insert_one(data)
        return result.inserted_id
    
    def get_all(self, collection_name: str) -> list:
        collection = self.db[collection_name]
        return list(collection.find({}, {"_id": 0}))
    
db = Database()