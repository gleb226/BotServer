from datetime import datetime
from tabulate import tabulate
from app.databases.mongodb_client import users_collection

class user_database:
    def __init__(self):
        self.collection = users_collection

    def add_user(self, user_id: int, first_name: str, last_name: str, username: str,
                 language_code: str, is_premium: bool, chat_id: int, chat_type: str):
        
        if self.collection.find_one({"user_id": user_id}):
            return
            
        user_data = {
            "user_id": user_id,
            "first_name": first_name,
            "last_name": last_name,
            "username": username,
            "language_code": language_code,
            "is_premium": bool(is_premium),
            "chat_id": chat_id,
            "chat_type": chat_type,
            "joined_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        self.collection.insert_one(user_data)

    def get_users_table(self):
        users = list(self.collection.find())
        if not users:
            return "No users found."
            
        data = []
        for u in users:
            data.append([
                u.get("user_id"), 
                u.get("first_name"), 
                u.get("last_name"), 
                u.get("username"), 
                u.get("language_code"), 
                u.get("is_premium"), 
                u.get("chat_id"), 
                u.get("chat_type"),
                u.get("joined_at")
            ])
            
        headers = ["User ID", "First Name", "Last Name", "Username", "Language", "Premium", "Chat ID", "Chat Type", "Joined At"]
        return tabulate(data, headers=headers, tablefmt="grid")

    def get_user(self, user_id: int):
        return self.collection.find_one({"user_id": user_id})

    def delete_user(self, user_id: int):
        self.collection.delete_one({"user_id": user_id})

    def count_users(self):
        return self.collection.count_documents({})

db = user_database()
