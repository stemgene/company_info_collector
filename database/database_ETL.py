from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from dotenv import load_dotenv
import os
import json

class DatabaseManager:
    def __init__(self):
        self.db_name = "company_info_db"
        self.collection_name = "companies"

        load_dotenv()
        mongodb_username = os.getenv("MONGODB_USERNAME")
        mongodb_password = os.getenv("MONGODB_PASSWORD")
        uri = f"mongodb+srv://{mongodb_username}:{mongodb_password}@mynosqlserver.1ev6o.mongodb.net/?retryWrites=true&w=majority&appName=MyNoSQLServer"

        # Create a new client and connect to the server
        self.client = MongoClient(uri, server_api=ServerApi('1'))
        # Send a ping to confirm a successful connection
        try:
            self.client.admin.command('ping')
            print("Successfully connected to MongoDB!")
        except Exception as e:
            print(e)
    
    def insert_data(self, db_name: str, collection_name: str, data: dict):
        db = self.client[self.db_name]
        collection = db[collection_name]
        collection.insert_one(data)
        print(f"Data inserted into {collection_name} collection in {db_name} database.")

    def fetch_data(self, 
                   query: dict
                   ):
        db = self.client[self.db_name]
        collection = db[self.collection_name]
        return list(collection.find(query))
    
    def upsert_data(self, query: dict, data: dict):
        """
        插入或更新数据
        """
        db = self.client[self.db_name]
        collection = db[self.collection_name]
        existing_record = collection.find_one(query)
        if existing_record:
            collection.update_one(query, {"$set": data})
            print(f"Data in {self.collection_name} collection in {self.db_name} database updated.")
        else:
            collection.insert_one(data)
            print(f"Data inserted into {self.collection_name} collection in {self.db_name} database.")
    
    def close_connection(self):
        self.client.close()


if __name__ == "__main__":
    manager = DatabaseManager()
    
    # 创建数据库
    db = manager.create_database("company_info_db")
    
    # 插入数据
    company_info = {
        "id": 1,
        "company_name": "NETSCOUT",
        "URL": "https://netscoutrccorp.peoplefluent.com/res_joblist.html",
        "website_type": "static_HTML",
        "parameters": {
            "tag": "h3",
            "attribute": {
                "class": "title"
            },
            "index_num": 0
        },
        "filters": [],
        "is_local": True,
        "position": [42.55309863630028, -71.44162944490446],
        "category": "Tech",
        "available": "True"
    }
    manager.insert_data("company_info_db", "companies", company_info)

    data = manager.fetch_data("company_info_db", "companies")
    print(data)