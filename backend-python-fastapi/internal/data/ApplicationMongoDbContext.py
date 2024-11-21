from pymongo import MongoClient
import os

DATABASE_MONGO_URL = os.getenv("DATABASE_MONGO_URL", "mongodb://localhost:27017/")

class ApplicationMongoDbContext(object):
    
    def __init__(self) -> None:
        self.__client = MongoClient(DATABASE_MONGO_URL)

    def get_database(self):
        return self.__client['mai_master_degree_system_analysis_lab']
    
    def close(self) -> None:
        self.__client.close()