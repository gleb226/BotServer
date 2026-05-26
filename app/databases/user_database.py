import sqlite3
from datetime import datetime
from tabulate import tabulate
from app.common.config import DATABASE_TYPE, SQLITE_DB_PATH

class user_database:
    def __init__(self):
        if DATABASE_TYPE == "sqlite":
            self.conn = sqlite3.connect(SQLITE_DB_PATH)
            self.cursor = self.conn.cursor()
            self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS users (
                    user_id INTEGER PRIMARY KEY,
                    first_name TEXT,
                    last_name TEXT,
                    username TEXT,
                    language_code TEXT,
                    language TEXT DEFAULT 'English',
                    is_premium BOOLEAN,
                    chat_id INTEGER,
                    chat_type TEXT,
                    joined_at TEXT
                )
            ''')
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
            ''', (user_id, first_name, last_name, username, language_code, bool(is_premium), chat_id, chat_type, datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
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
                "language": "English",
                "is_premium": bool(is_premium),
                "chat_id": chat_id,
                "chat_type": chat_type,
                "joined_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
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
            return res[0] if res else "English"
        else:
            user = self.collection.find_one({"user_id": user_id})
            return user.get("language", "English") if user else "English"

    def get_users_table(self):
        if DATABASE_TYPE == "sqlite":
            self.cursor.execute("SELECT * FROM users")
            users = self.cursor.fetchall()
            if not users:
                return "No users found."
            headers = ["User ID", "First Name", "Last Name", "Username", "Language Code", "Language", "Premium", "Chat ID", "Chat Type", "Joined At"]
            return tabulate(users, headers=headers, tablefmt="grid")
        else:
            users = list(self.collection.find())
            if not users:
                return "No users found."
            data = [[u.get("user_id"), u.get("first_name"), u.get("last_name"), u.get("username"), u.get("language_code"), u.get("language"), u.get("is_premium"), u.get("chat_id"), u.get("chat_type"), u.get("joined_at")] for u in users]
            headers = ["User ID", "First Name", "Last Name", "Username", "Language Code", "Selected Language", "Premium", "Chat ID", "Chat Type", "Joined At"]
            return tabulate(data, headers=headers, tablefmt="grid")

    def get_user(self, user_id: int):
        if DATABASE_TYPE == "sqlite":
            self.cursor.execute("SELECT * FROM users WHERE user_id = ?", (user_id,))
            res = self.cursor.fetchone()
            if res:
                columns = [column[0] for column in self.cursor.description]
                return dict(zip(columns, res))
            return None
        else:
            return self.collection.find_one({"user_id": user_id})

    def delete_user(self, user_id: int):
        if DATABASE_TYPE == "sqlite":
            self.cursor.execute("DELETE FROM users WHERE user_id = ?", (user_id,))
            self.conn.commit()
        else:
            self.collection.delete_one({"user_id": user_id})

    def count_users(self):
        if DATABASE_TYPE == "sqlite":
            self.cursor.execute("SELECT COUNT(*) FROM users")
            return self.cursor.fetchone()[0]
        else:
            return self.collection.count_documents({})

db = user_database()
