import sqlite3
from datetime import datetime
from app.common.config import DATABASE_TYPE, SQLITE_DB_PATH
class user_database:
    def __init__(self):
        if DATABASE_TYPE == "sqlite":
            self.conn = sqlite3.connect(SQLITE_DB_PATH, check_same_thread=False)
            self.cursor = self.conn.cursor()
            self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS users (
                    user_id INTEGER PRIMARY KEY,
                    first_name TEXT,
                    last_name TEXT,
                    username TEXT,
                    language_code TEXT,
                    language TEXT,
                    is_premium BOOLEAN,
                    chat_id INTEGER,
                    chat_type TEXT,
                    storage_limit_gb REAL DEFAULT 2.0,
                    joined_at TEXT,
                    last_payment_date TEXT,
                    pending_order_id TEXT,
                    pending_plan_id TEXT
                )
            '''
               )
            self.conn.commit()
        else:
            from app.databases.mongodb_client import users_collection
            self.collection = users_collection
    def add_user(self, user_id: int, first_name: str, last_name: str, username: str,
                 language_code: str, is_premium: bool, chat_id: int, chat_type: str):
        if DATABASE_TYPE == "sqlite":
            self.cursor.execute("SELECT user_id FROM users WHERE user_id = ?", (user_id,))
            if self.cursor.fetchone():
                return
            self.cursor.execute('''
                INSERT INTO users (user_id, first_name, last_name, username, language_code, is_premium, chat_id, chat_type, joined_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            '''
               , (user_id, first_name, last_name, username, language_code, bool(is_premium), chat_id, chat_type, datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
            self.conn.commit()
        else:
            if self.collection.find_one({"user_id": user_id}):
                return
            user_data = {
                "user_id": user_id,
                "first_name": first_name,
                "last_name": last_name,
                "username": username,
                "language_code": language_code,
                "language": None,
                "is_premium": bool(is_premium),
                "chat_id": chat_id,
                "chat_type": chat_type,
                "storage_limit_gb": 2.0,
                "joined_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "last_payment_date": None,
                "pending_order_id": None,
                "pending_plan_id": None
            }
            self.collection.insert_one(user_data)
    def set_language(self, user_id: int, language: str):
        if DATABASE_TYPE == "sqlite":
            self.cursor.execute("UPDATE users SET language = ? WHERE user_id = ?", (language, user_id))
            self.conn.commit()
        else:
            self.collection.update_one({"user_id": user_id}, {"$set": {"language": language}})
    def get_language(self, user_id: int):
        if DATABASE_TYPE == "sqlite":
            self.cursor.execute("SELECT language FROM users WHERE user_id = ?", (user_id,))
            res = self.cursor.fetchone()
            return res[0] if res else None
        else:
            user = self.collection.find_one({"user_id": user_id})
            return user.get("language") if user else None
    def get_storage_limit(self, user_id: int):
        if DATABASE_TYPE == "sqlite":
            self.cursor.execute("SELECT storage_limit_gb FROM users WHERE user_id = ?", (user_id,))
            res = self.cursor.fetchone()
            return res[0] if res else 2.0
        else:
            user = self.collection.find_one({"user_id": user_id})
            return user.get("storage_limit_gb", 2.0) if user else 2.0
    def set_storage_limit(self, user_id: int, limit: float):
        if DATABASE_TYPE == "sqlite":
            self.cursor.execute("UPDATE users SET storage_limit_gb = ?, last_payment_date = ? WHERE user_id = ?",
                                (limit, datetime.now().strftime("%Y-%m-%d"), user_id))
            self.conn.commit()
        else:
            self.collection.update_one({"user_id": user_id}, {
                "$set": {
                    "storage_limit_gb": limit,
                    "last_payment_date": datetime.now().strftime("%Y-%m-%d")
                }
            })
    def set_pending_payment(self, user_id: int, order_id: str, plan_id: str):
        if DATABASE_TYPE == "sqlite":
            self.cursor.execute("UPDATE users SET pending_order_id = ?, pending_plan_id = ? WHERE user_id = ?", (order_id, plan_id, user_id))
            self.conn.commit()
        else:
            self.collection.update_one({"user_id": user_id}, {"$set": {"pending_order_id": order_id, "pending_plan_id": plan_id}})
    def get_pending_payments(self):
        if DATABASE_TYPE == "sqlite":
            self.cursor.execute("SELECT user_id, pending_order_id, pending_plan_id FROM users WHERE pending_order_id IS NOT NULL")
            return self.cursor.fetchall()
        else:
            return list(self.collection.find({"pending_order_id": {"$ne": None}}, {"user_id": 1, "pending_order_id": 1, "pending_plan_id": 1}))
    def clear_pending_payment(self, user_id: int):
        if DATABASE_TYPE == "sqlite":
            self.cursor.execute("UPDATE users SET pending_order_id = NULL, pending_plan_id = NULL WHERE user_id = ?", (user_id,))
            self.conn.commit()
        else:
            self.collection.update_one({"user_id": user_id}, {"$set": {"pending_order_id": None, "pending_plan_id": None}})
    def get_all_users_with_subscription(self):
        if DATABASE_TYPE == "sqlite":
            self.cursor.execute("SELECT user_id, last_payment_date, storage_limit_gb, language FROM users WHERE storage_limit_gb > 2.0")
            return self.cursor.fetchall()
        else:
            return list(self.collection.find({"storage_limit_gb": {"$gt": 2.0}}))
db = user_database()
