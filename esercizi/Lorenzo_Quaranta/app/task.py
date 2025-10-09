from typing import Any, Literal

from flask import Blueprint, abort, request


bp = Blueprint("task", "task", url_prefix="/tasks")
cache: dict[int, Any] = {}
current_task_id: int = 0


@bp.route("/<int:task_id>", methods=("GET",))
def get_task(task_id: int) -> tuple[dict[str, Any], int]:
    if task_id not in cache:
        abort(404)
    
    return cache[task_id], 200


@bp.route("/", methods=("POST",'GET'))
def post_task() -> tuple[dict[str, Any], int]:
    task_name = request.form.get("task-name")
    description = request.form.get("description")
    if not task_name or not description:
        abort(400)

    current_task_id += 1
    obj: dict[str, Any] = {
        "task_id": current_task_id,
        "title": task_name,
        "description": description,
    }
    cache[current_task_id] = obj
    return obj, 201

def get_tasks():
    pass