from flask import Flask, request, jsonify
from pytodo import TodoList, TodoItem
from datetime import datetime

app = Flask(__name__)
todo_list = TodoList()

@app.route('/todos', methods=['GET'])
def get_all_todos():
    try:
        items = todo_list.list_items()
        return jsonify([item.to_dict() for item in items]), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/todo', methods=['POST'])
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

@app.route('/todo/<int:item_id>', methods=['GET'])
def get_todo(item_id):
    try:
        item = todo_list.get_item(item_id)
        return jsonify(item.to_dict()) if item else ('', 404)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/todo/<int:item_id>', methods=['PUT'])
def update_todo(item_id):
    try:
        data = request.json
        todo_list.update_item(item_id, **data)
        return jsonify({"message": "Todo item updated successfully."}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@app.route('/todo/<int:item_id>', methods=['DELETE'])
def delete_todo(item_id):
    try:
        todo_list.remove_item(item_id)
        return jsonify({"message": "Todo item deleted successfully."}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400

if __name__ == '__main__':
    app.run(debug=True)
