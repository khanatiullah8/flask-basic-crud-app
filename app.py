from flask import Flask, jsonify, request

data = []

app = Flask('asdfasd')

# welcome page
@app.route("/")
def welcome():
    return """
            <h2>*** Todo Application ***</h2>
            <p>Try these APIs:</p>
            <ul>
                <li>/get-todo-all</li>
                <li>/get-todo/&lt;id&gt;</li>
                <li>/create-todo (pass data using 'post' method)</li>
                <li>/update-todo (pass data using 'put' method)</li>
                <li>/delete-todo/&lt;id&gt;</li>
            </ul>
            """

# get all todos
@app.route("/get-todo-all")
def show_all():
    if not data:
        return "your todo bucket is empty"
    
    return jsonify(data)

# get single todo
@app.route("/get-todo/<int:id>")
def show(id):
    if not data:
        return "your todo bucket is empty"
    
    for item in data:
        if item.get("id") == id:
            return jsonify(item)
        
    return "ID mismatch"

# add new todo
@app.route("/create-todo", methods=["POST"])
def create_todo():
    new_todo = request.get_json()
    new_todo["id"] = 1 if not data else data[len(data)-1].get("id")+1
    new_todo["status"] = "pending"
    data.append(new_todo)
    return "todo created successfully"

# update todo
@app.route("/update-todo",methods=["PUT"])
def update_todo():
    req_body = request.get_json()
    
    if not data:
        return "your todo bucket is empty to perform UPDATE operation"
    
    for item in data:
        if item.get("id") == req_body.get("id"):
            if req_body.get("title"):
                item["title"] = req_body["title"]
            if req_body.get("status"):
                item["status"] = req_body["status"]
            return "todo updated successfully"
        
    return "ID mismatch"

# delete todo
@app.route("/delete-todo/<int:id>",methods=["DELETE"])
def delete_todo(id):
    if not data:
        return "your todo bucket is empty to perform DELETE operation"
    
    for item in data:
        if item.get("id") == id:
            data.remove(item)
            return "todo deleted successfully"
        
    return "ID mismatch"

# app run
if __name__ == "__main__":
    app.run(debug=True)