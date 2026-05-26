import sqlite3
from app.common.config import DATABASE_TYPE, CATEGORIES_DB_PATH

class categories_database:
    def __init__(self):
        if DATABASE_TYPE == "sqlite":
            self.conn = sqlite3.connect(CATEGORIES_DB_PATH)
            self.cursor = self.conn.cursor()
            self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS subcategories (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER NOT NULL,
                    category TEXT NOT NULL,
                    subcategory TEXT NOT NULL,
                    parent_subcategory TEXT DEFAULT NULL,
                    UNIQUE(user_id, category, subcategory, parent_subcategory)
                )
            ''')
            self.conn.commit()
        else:
            from app.databases.mongodb_client import categories_collection
            self.collection = categories_collection
            self.collection.create_index(
                [("user_id", 1), ("category", 1), ("subcategory", 1), ("parent_subcategory", 1)],
                unique=True
            )

    def add_subcategory(self, user_id, category, subcategory, parent_subcategory=None):
        try:
            if DATABASE_TYPE == "sqlite":
                self.cursor.execute('''
                    INSERT INTO subcategories (user_id, category, subcategory, parent_subcategory)
                    VALUES (?, ?, ?, ?)
                ''', (user_id, category, subcategory, parent_subcategory))
                self.conn.commit()
                return True
            else:
                subcategory_data = {
                    "user_id": user_id,
                    "category": category,
                    "subcategory": subcategory,
                    "parent_subcategory": parent_subcategory
                }
                self.collection.insert_one(subcategory_data)
                return True
        except Exception:
            return False

    def delete_subcategory(self, user_id, category, subcategory, parent_subcategory=None):
        if DATABASE_TYPE == "sqlite":
            self.cursor.execute('''
                DELETE FROM subcategories 
                WHERE user_id = ? AND category = ? AND subcategory = ? AND parent_subcategory = ?
            ''', (user_id, category, subcategory, parent_subcategory))
            self.cursor.execute('''
                DELETE FROM subcategories 
                WHERE user_id = ? AND category = ? AND parent_subcategory = ?
            ''', (user_id, category, subcategory))
            self.conn.commit()
        else:
            self.collection.delete_one({
                "user_id": user_id,
                "category": category,
                "subcategory": subcategory,
                "parent_subcategory": parent_subcategory
            })
            self.collection.delete_many({
                "user_id": user_id,
                "category": category,
                "parent_subcategory": subcategory
            })

    def get_subcategories(self, user_id, category, parent_subcategory=None):
        if DATABASE_TYPE == "sqlite":
            if parent_subcategory:
                self.cursor.execute('''
                    SELECT subcategory FROM subcategories 
                    WHERE user_id = ? AND category = ? AND parent_subcategory = ?
                    ORDER BY subcategory ASC
                ''', (user_id, category, parent_subcategory))
            else:
                self.cursor.execute('''
                    SELECT subcategory FROM subcategories 
                    WHERE user_id = ? AND category = ? AND parent_subcategory IS NULL
                    ORDER BY subcategory ASC
                ''', (user_id, category))
            results = self.cursor.fetchall()
            return [res[0] for res in results]
        else:
            results = self.collection.find({
                "user_id": user_id,
                "category": category,
                "parent_subcategory": parent_subcategory
            }).sort("subcategory", 1)
            return [doc["subcategory"] for doc in results]

    def subcategory_exists(self, user_id, category, subcategory, parent_subcategory=None):
        if DATABASE_TYPE == "sqlite":
            if parent_subcategory:
                self.cursor.execute('''
                    SELECT COUNT(*) FROM subcategories 
                    WHERE user_id = ? AND category = ? AND subcategory = ? AND parent_subcategory = ?
                ''', (user_id, category, subcategory, parent_subcategory))
            else:
                self.cursor.execute('''
                    SELECT COUNT(*) FROM subcategories 
                    WHERE user_id = ? AND category = ? AND subcategory = ? AND parent_subcategory IS NULL
                ''', (user_id, category, subcategory))
            return self.cursor.fetchone()[0] > 0
        else:
            count = self.collection.count_documents({
                "user_id": user_id,
                "category": category,
                "subcategory": subcategory,
                "parent_subcategory": parent_subcategory
            })
            return count > 0

    def close(self):
        if DATABASE_TYPE == "sqlite":
            self.conn.close()
