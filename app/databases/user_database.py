import sqlite3
from datetime import datetime
from tabulate import tabulate
from app.common.config import USERS_DB_PATH

class user_database:
    def __init__(self):
        self.db_name = USERS_DB_PATH
        self.last_error = None
        self._init_database()

    def _execute(self, query, params=(), fetchone=False, fetchall=False):
        try:
            with sqlite3.connect(self.db_name) as conn:
                cursor = conn.cursor()
                cursor.execute(query, params)
                conn.commit()
                if fetchone:
                    return cursor.fetchone()
                if fetchall:
                    return cursor.fetchall()
        except sqlite3.Error as e:
            self.last_error = f"Database error: {e}"
        except Exception as e:
            self.last_error = f"Unexpected error: {e}"
        return None

    def _init_database(self):
        query = '''
                CREATE TABLE IF NOT EXISTS users (
                                                     user_id INTEGER PRIMARY KEY,
                                                     first_name TEXT,
                                                     last_name TEXT,
                                                     username TEXT,
                                                     language_code TEXT,
                                                     is_premium BOOLEAN,
                                                     chat_id INTEGER,
                                                     chat_type TEXT,
                                                     joined_at TEXT DEFAULT CURRENT_TIMESTAMP
                ); \
                '''
        self._execute(query)

    def add_user(self, user_id: int, first_name: str, last_name: str, username: str,
                 language_code: str, is_premium: bool, chat_id: int, chat_type: str):
        if self._execute("SELECT user_id FROM users WHERE user_id = ?", (user_id,), fetchone=True):
            return
        query = '''
                INSERT INTO users (user_id, first_name, last_name, username, language_code, is_premium, chat_id, chat_type, joined_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?) \
                '''
        self._execute(query, (user_id, first_name, last_name, username, language_code,
                              int(bool(is_premium)), chat_id, chat_type,
                              datetime.now().strftime("%Y-%m-%d %H:%M:%S")))

    def get_users_table(self):
        users = self._execute("SELECT * FROM users", fetchall=True)
        headers = ["User ID", "First Name", "Last Name", "Username", "Language", "Premium", "Chat ID", "Chat Type",
                   "Joined At"]
        return tabulate(users, headers=headers, tablefmt="grid") if users else "No users found."

    def get_user(self, user_id: int):
        return self._execute("SELECT * FROM users WHERE user_id = ?", (user_id,), fetchone=True)

    def delete_user(self, user_id: int):
        if self._execute("SELECT user_id FROM users WHERE user_id = ?", (user_id,), fetchone=True):
            self._execute("DELETE FROM users WHERE user_id = ?", (user_id,))
        else:
            self.last_error = f"User {user_id} not found."

    def count_users(self):
        count = self._execute("SELECT COUNT(*) FROM users", fetchone=True)
        return count[0] if count else 0

db = user_database()
