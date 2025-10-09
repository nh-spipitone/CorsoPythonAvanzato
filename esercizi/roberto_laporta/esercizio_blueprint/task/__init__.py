from flask import Blueprint, abort, jsonify, request

BLUEPRINT_NAME="task"

bp = Blueprint(BLUEPRINT_NAME, __name__, url_prefix=f"/{BLUEPRINT_NAME}") 

def id_generator(initial_id=1):
    current_id = initial_id
    while True:
        yield current_id
        current_id += 1


tasks = []

task_id_gen = id_generator(initial_id=len(tasks) + 1)

@bp.get("/")
def get_tasks():
    return tasks

@bp.get("/<int:id>")
def get_tasks_by_id(id: int):
    try:
        task = next(t for t in tasks if t["id"] == id)
        return task
       
    except StopIteration:
        return jsonify("Elemento non trovato"), 404 


@bp.post("/")
def create_task():
    body = request.get_json(silent=True)
    if body is None:
        return jsonify("Nessun body fornito"), 400 
    
    try:
        title = body["title"]
    except:
        return jsonify("Campo title richiesto"), 400
    
    new_task = {
        "id": next(task_id_gen),
        "title" : title,
    }

    tasks.append(new_task)
    return new_task


@bp.route("/<int:id>", methods=["PUT"])
def update_task(id: int):
    body = request.get_json(silent=True)
    if body is None:
        return jsonify("Nessun body fornito"), 400 
    
    try:
        title = body["title"]
    except KeyError:
        return jsonify({"message": "Campo title richiesto"}), 400

    try:
        task_to_update = next(t for t in tasks if t["id"] == id)
    except:
        return jsonify({"message": f"La task con ID {id} non è stata trovata."}), 404 
    
    task_to_update["title"] = title
    
    return jsonify(task_to_update)


@bp.delete("/<int:id>")
def delete_task(id: int):
    try:
        index_to_delete = next(i for i, t in enumerate(tasks) if t["id"] == id)
    except:
        return jsonify({"message": f"La task con ID {id} non è stata trovata."}), 404 
    
    tasks.pop(index_to_delete)

    return jsonify({"message": f"Task con ID {id} eliminata con successo."}), 200 
