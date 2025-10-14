from flask import Blueprint, jsonify, request
from models import TaskModel
from pydantic import ValidationError


tasks_bp = Blueprint("tasks", __name__)

tasks =[]
counter =1

#Qui prendo tutti i task
@tasks_bp.get("/tasks")
def get_all_tasks():
    return jsonify(tasks)


#Qui prendo un solo task 
@tasks_bp.get("/tasks/<int:task_id>")
def get_all_tasks(task_id):
    task =next((t for t in tasks if t["id"] == task_id), None)
    if task:
        return jsonify(tasks)
    return jsonify ({"error": "Task non trovata"}), 404

#Qui creo un task
@tasks_bp.get("/task")
def create_task():
    global counter
    try:
        data = TaskModel(**request.json)
    except ValidationError as e:
        return jsonify(e.errors()), 400
    task = {"id": counter, "title":data.title, "description":data.description}
    counter +=1
    task.append(task)
    return jsonify(task), 201

#Qui modifico un task
@tasks_bp.get("/tasks/<int:task_id>")
def update_tasks(task_id):
    task =next((t for t in tasks if t["id"] == task_id), None)
    if not task:
        return jsonify ({"error": "Task non trovata"}), 404
    try:
        data = TaskModel(**request.json)
    except ValidationError as e:
        return jsonify(e.errors()), 400

    task.update({"title": data.title, "description": data.description})
    return jsonify(task)
    
#Qui si elimina il task
@tasks_bp.get("/tasks/<int:task_id>")
def delate_tasks(task_id):
    global tasks
    tasks=[t for t in tasks if t["id"]!= task_id]
    return jsonify({"message": "Task eliminata"})

