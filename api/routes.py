from flask import request, jsonify
from lib.pytodo import TodoList, TodoItem
from datetime import datetime

from services.auth_guard import auth_guard

todo_list = TodoList()

def init(app):
    @app.route('/api/todos', methods=['GET'])
    @auth_guard()
    def get_all_todos():
        try:
            items = todo_list.list_items()
            return jsonify([item.to_dict() for item in items]), 200
        except Exception as e:
            return jsonify({"error": str(e)}), 500

    @app.route('/api/todo', methods=['POST'])
    @auth_guard()
    def add_todo():
        try:
            data = request.json
            new_item = TodoItem(
                id=data['id'],
                title=data['title'],
                description=data.get('description', ''),
                due_date=datetime.strptime(data['due_date'], '%Y-%m-%d'),
                status=data['status'],
                category=data.get('category')
            )
            todo_list.add_item(new_item)
            return jsonify({"message": "Todo item added successfully."}), 201
        except Exception as e:
            return jsonify({"error": str(e)}), 400

    @app.route('/api/todo/<int:item_id>', methods=['GET'])
    @auth_guard()
    def get_todo(item_id):
        try:
            item = todo_list.get_item(item_id)
            return jsonify(item.to_dict()) if item else ('', 404)
        except Exception as e:
            return jsonify({"error": str(e)}), 500

    @app.route('/todo/<int:item_id>', methods=['PUT'])
    @auth_guard()
    def update_todo(item_id):
        try:
            data = request.json
            todo_list.update_item(item_id, **data)
            return jsonify({"message": "Todo item updated successfully."}), 200
        except Exception as e:
            return jsonify({"error": str(e)}), 400

    @app.route('/todo/<int:item_id>', methods=['DELETE'])
    @auth_guard()
    def delete_todo(item_id):
        try:
            todo_list.remove_item(item_id)
            return jsonify({"message": "Todo item deleted successfully."}), 200
        except Exception as e:
            return jsonify({"error": str(e)}), 400