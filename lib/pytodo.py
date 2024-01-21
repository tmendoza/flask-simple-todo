from pymongo import MongoClient
from datetime import datetime

import uuid

# MongoDB Connection Setup
client = MongoClient('mongodb://localhost:27017/')
db = client.todo_database

class TodoItem:
    def __init__(self, id, title, description, due_date, status, category=None):
        self.id = id
        self.title = title
        self.description = description
        self.due_date = datetime.strptime(due_date, '%Y-%m-%d') if isinstance(due_date, str) else due_date
        self.status = status
        self.category = category

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "due_date": self.due_date,
            "status": self.status,
            "category": self.category
        }

    @staticmethod
    def from_dict(data):
        return TodoItem(
            id=data.get("id"),
            title=data.get("title"),
            description=data.get("description"),
            due_date=data.get("due_date"),
            status=data.get("status"),
            category=data.get("category")
        )

    def update_status(self, new_status):
        self.status = new_status

    def update_details(self, title=None, description=None, due_date=None):
        if title is not None:
            self.title = title
        if description is not None:
            self.description = description
        if due_date is not None:
            self.due_date = due_date

class TodoList:
    def __init__(self):
        self.collection = db.todo_items

    def add_item(self, item):
        if self.collection.find_one({"id": item.id}):
            raise ValueError("Item with this ID already exists.")
        self.collection.insert_one(item.to_dict())

    def remove_item(self, item_id):
        result = self.collection.delete_one({"id": item_id})
        if result.deleted_count == 0:
            raise ValueError("Item not found.")

    def get_item(self, item_id):
        item_data = self.collection.find_one({"id": item_id})
        return TodoItem.from_dict(item_data) if item_data else None

    def update_item(self, item_id, **kwargs):
        if 'due_date' in kwargs:
            kwargs['due_date'] = datetime.strptime(kwargs['due_date'], '%Y-%m-%d')
        update_data = {"$set": kwargs}
        result = self.collection.update_one({"id": item_id}, update_data)
        if result.matched_count == 0:
            raise ValueError("Item not found.")

    def list_items(self):
        return [TodoItem.from_dict(item) for item in self.collection.find()]

    def clear_all_items(self):
        self.collection.delete_many({})

    # Additional methods can be added as per future requirements.

if __name__ == "__main__":
    # Example Usage

    todo_list = TodoList()

    print("Running todo list...")
    # Add a new item
    try:
        #ident = bson.Binary.from_uuid(uuid.uuid4())
        for ident in range(1, 20):
            new_item = TodoItem(id=ident, title="Buy Groceries", description="Milk, Bread, Eggs", due_date="2024-01-25", status="pending")
            todo_list.add_item(new_item)
    except ValueError as e:
        print(e)

    # List all items
    for item in todo_list.list_items():
        print(f"{item.id}: {item.title} - {item.status}")

    #todo_list.clear_all_items()
