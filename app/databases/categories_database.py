from app.databases.mongodb_client import categories_collection


class categories_database:
    def __init__(self):
        self.collection = categories_collection
        self.collection.create_index(
            [("user_id", 1), ("category", 1), ("subcategory", 1), ("parent_subcategory", 1)],
            unique=True
        )

    def add_subcategory(self, user_id, category, subcategory, parent_subcategory=None):
        try:
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
        results = self.collection.find({
            "user_id": user_id,
            "category": category,
            "parent_subcategory": parent_subcategory
        }).sort("subcategory", 1)
        
        return [doc["subcategory"] for doc in results]

    def subcategory_exists(self, user_id, category, subcategory, parent_subcategory=None):
        count = self.collection.count_documents({
            "user_id": user_id,
            "category": category,
            "subcategory": subcategory,
            "parent_subcategory": parent_subcategory
        })
        return count > 0

    def close(self):
        pass
