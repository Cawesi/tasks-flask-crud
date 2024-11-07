from flask import Flask, request, jsonify
from models.tasks import Task

app = Flask(__name__)

tasks = []
task_id_control = 1

@app.route("/tasks", methods=['POST'])
def create_task():
    global task_id_control
    data = request.get_json()
    new_task = Task(id=task_id_control, tittle=data["title"], description=data.get("description", ""))
    task_id_control += 1
    tasks.append(new_task)
    print(tasks)
    print(data)
    return jsonify({"message": "Nova tarefa criada com sucesso!"})


@app.route("/tasks", methods=["GET"])
def get_tasks():
    task_list = [task.to_dict() for task in tasks]
    output = {
        "tasks": task_list,
        "total_tasks": len(task_list)
    }
    return jsonify(output)


@app.route("/tasks/<int:id>", methods=["GET"])
def get_task_selected(id):
    for t in tasks:
        if t.id == id:
            return jsonify(t.to_dict())
    return jsonify({"message": "Não foi possível localizar a tarefa!"}), 404
        

@app.route("/tasks/<int:id>", methods=["PUT"])
def update_task(id):
    task = None
    for t in tasks:
        if t.id == id:
            data = request.get_json()
            t.tittle = data["title"]
            t.description = data["description"]
            t.completed = bool(data["completed"])
            return jsonify({"message": "Tarefa atualizada com sucesso!"})

    if task == None:
        return jsonify({"message": "Não foi possível localizar a tarefa!"}), 404
    

@app.route("/tasks/<int:id>", methods=["DELETE"])
def delete_task(id):
    task = None
    for t in tasks:
        if t.id == id:
            task = t

    if task == None:
        return jsonify({"message": "Não foi possível localizar a tarefa!"}), 404
    
    tasks.remove(task)
    return jsonify({"message": "Tarefa deletada com sucesso!"})
    

if __name__ == "__main__":
    app.run(debug=True)