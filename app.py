# app.py
from flask import Flask, jsonify, request

app = Flask(__name__)

# Sample data
tasks = [
    {"id": 1, "title": "Buy groceries", "done": False},
    {"id": 2, "title": "Write code", "done": True},
]

@app.route("/tasks", methods=["GET"])
def get_tasks():
    return jsonify({"tasks": tasks})

@app.route("/tasks/<int:task_id>", methods=["GET"])
def get_task(task_id):
    task = next((task for task in tasks if task["id"] == task_id), None)
    if task is None:
        return jsonify({"error": "Task not found"}), 404
    return jsonify({"task": task})

@app.route("/tasks", methods=["POST"])
def create_task():
    if not request.json or "title" not in request.json:
        return jsonify({"error": "Bad request"}), 400

    task = {
        "id": tasks[-1]["id"] + 1 if tasks else 1,
        "title": request.json["title"],
        "done": False,
    }
    tasks.append(task)
    return jsonify({"task": task}), 201

@app.route("/tasks/<int:task_id>", methods=["PUT"])
def update_task(task_id):
    task = next((task for task in tasks if task["id"] == task_id), None)
    if task is None:
        return jsonify({"error": "Task not found"}), 404

    if not request.json:
        return jsonify({"error": "Bad request"}), 400

    task["title"] = request.json.get("title", task["title"])
    task["done"] = request.json.get("done", task["done"])
    return jsonify({"task": task})

@app.route("/tasks/<int:task_id>", methods=["DELETE"])
def delete_task(task_id):
    task = next((task for task in tasks if task["id"] == task_id), None)
    if task is None:
        return jsonify({"error": "Task not found"}), 404

    tasks.remove(task)
    return jsonify({"result": True})

if __name__ == "__main__":
    app.run(debug=True)
