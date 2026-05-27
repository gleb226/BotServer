import os
from app.common.config import DATABASE_TYPE

def get_mongodb_collections():
    if DATABASE_TYPE != "mongodb":
        return None, None, None

    from pymongo import MongoClient
    from dotenv import load_dotenv

    load_dotenv()

    MONGO_URL = os.getenv("MONGO_URL", "mongodb://localhost:27017")
    client = MongoClient(MONGO_URL)
    db = client['bot_server_db']

    return db['users'], db['subcategories'], db['errors']

users_collection, categories_collection, errors_collection = get_mongodb_collections()