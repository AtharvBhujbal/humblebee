import pymongo


class Database:
    def __init__(self):
        self.client = pymongo.MongoClient("mongodb://localhost:27017/")
        self.db = self.client["humblebee"]


    def register(self, collection_name: str, data: dict) -> str:
        collection = self.db[collection_name]
        if collection.find_one({"hiveId": data["hiveId"]}):
            raise ValueError(f"Hive with ID {data['hiveId']} already exists.")
        result = collection.insert_one(data)
        return result.inserted_id
    
db = Database()