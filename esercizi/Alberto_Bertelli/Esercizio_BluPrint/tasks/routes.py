from flask import Blueprint, jsonify, request

#creiamo il blue print
tasks_bp = Blueprint("tasks", __name__, url_prefix="/tasks")


#creiamo una lista
tasks =[]
next_id=1 # contatore per assegnare id univoci


#restituisce tutti i task
@tasks_bp.route("/",methods=["GET"])
def get_all_tasks():
    #jsonify è una funzione di Flask che serve per restituire una risposta in formato JSON da una route.
    return jsonify(tasks)

#restituisce un task per id
@tasks_bp.route("/<int:id>",methods=["GET"])
def get_task(id):
    task =next((t for t in tasks if t["id"]==id),None)
    if task:
        return jsonify(tasks)
    return jsonify({"error": "Task non trovato"}), 404

#aggiunge un nuovo task
#restituisce un task per id
@tasks_bp.route("/",methods=["POST"])
def add_task():
    global next_id
    data =request.get_json()
    if not data or "title" not in data:
        return jsonify({"error": "Serve un campo 'title'"}), 400
    new_task ={"id":next_id,"title":data["title"]}
    tasks.append(new_task)
    next_id +=1
    return jsonify(new_task), 201

#modifica un task 
@tasks_bp.route("/<int:id>",methods=["PUT"])
def update_task(id):
    data = request.get_json()
    task =next((t for t in tasks if t["id"]==id),None)
    if not task:
        return jsonify({"error": "Task non trovato"}), 404
    task["title"]=data.get("title",task["title"])
    return jsonify(task)

#eliminare un task
@tasks_bp.route("/<int:id>",methods=["DELETE"])
def delete_task(id):
    #global serve per indicare che vuoi usare una variabile definita fuori da una funzione
    global tasks
    tasks =[t for t in tasks if t["id"] != id]
    return jsonify({"message": f"Task {id} eliminato"})



    







#