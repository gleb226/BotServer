import sqlite3
from app.common.config import CATEGORIES_DB_PATH


class categories_database:
    def __init__(self):
        self.conn = sqlite3.connect(CATEGORIES_DB_PATH, check_same_thread=False)
        self.cursor = self.conn.cursor()
        self.create_table()

    def create_table(self):
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

    def add_subcategory(self, user_id, category, subcategory, parent_subcategory=None):
        try:
            self.cursor.execute('''
                                INSERT INTO subcategories (user_id, category, subcategory, parent_subcategory)
                                VALUES (?, ?, ?, ?)
                                ''', (user_id, category, subcategory, parent_subcategory))
            self.conn.commit()
            return True
        except sqlite3.IntegrityError:
            return False

    def delete_subcategory(self, user_id, category, subcategory, parent_subcategory=None):
        self.cursor.execute('''
                            DELETE FROM subcategories
                            WHERE user_id = ? AND category = ? AND subcategory = ? AND parent_subcategory IS ?
                            ''', (user_id, category, subcategory, parent_subcategory))

        self.cursor.execute('''
                            DELETE FROM subcategories
                            WHERE user_id = ? AND category = ? AND parent_subcategory = ?
                            ''', (user_id, category, subcategory))

        self.conn.commit()

    def get_subcategories(self, user_id, category, parent_subcategory=None):
        self.cursor.execute('''
                            SELECT subcategory FROM subcategories
                            WHERE user_id = ? AND category = ? AND parent_subcategory IS ?
                            ORDER BY subcategory
                            ''', (user_id, category, parent_subcategory))
        return [row[0] for row in self.cursor.fetchall()]

    def subcategory_exists(self, user_id, category, subcategory, parent_subcategory=None):
        self.cursor.execute('''
                            SELECT COUNT(*) FROM subcategories
                            WHERE user_id = ? AND category = ? AND subcategory = ? AND parent_subcategory IS ?
                            ''', (user_id, category, subcategory, parent_subcategory))
        return self.cursor.fetchone()[0] > 0

    def close(self):
        self.conn.close()