import os
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()

MONGO_URL = os.getenv("MONGO_URL", "mongodb://localhost:27017")
client = MongoClient(MONGO_URL)
db = client['bot_server_db']

users_collection = db['users']
categories_collection = db['subcategories']
errors_collection = db['errors']
