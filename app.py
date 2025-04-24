from flask import Flask, jsonify, request

data = []

app = Flask('asdfasd')


# util functions -> start

def initiate_todo(todo_item, todo_list):
    todo_item["id"] = 1 if not todo_list else todo_list[len(todo_list)-1].get("id")+1
    todo_item["status"] = "pending"
    todo_list.append(todo_item) 

# util functions -> end

        
# welcome page
@app.route("/")
def welcome():
    return """
            <h2>*** Todo Application ***</h2>
            <p>Try these APIs:</p>
            <ul>
                <li>/get-todo-all</li>
                <li>/get-todo/&lt;todo_id&gt;</li>
                <li>/create-todo (pass data using 'post' method)</li>
                <li>/update-todo/&lt;todo_id&gt; (pass data using 'put' method)</li>
                <li>/delete-todo/&lt;todo_id&gt;</li>
            </ul>
            """

# get all todos
@app.route("/get-todo-all")
def show_all():
    if not data:
        return "your todo bucket is empty"
    
    return jsonify(data)

# get single todo
@app.route("/get-todo/<int:todo_id>")
def show(todo_id):
    if not data:
        return "your todo bucket is empty"
    
    for item in data:
        if item.get("id") == todo_id:
            return jsonify(item)
        
    return "ID mismatch"

# add new todo
@app.route("/create-todo", methods=["POST"])
def create_todo():
    new_todo = request.get_json()
    if "todo_items" in new_todo:                        # add multiple todos
        for item in new_todo.get("todo_items"):   
            initiate_todo(item, data)
    else:                                               # add single todo
        initiate_todo(new_todo, data)                   
    return "todo created successfully"

# update todo
@app.route("/update-todo/<int:todo_id>",methods=["PUT"])
def update_todo(todo_id):
    req_body = request.get_json()
    
    if not data:
        return "your todo bucket is empty to perform UPDATE operation"
    
    for item in data:
        if item.get("id") == todo_id:
            if req_body.get("title"):
                item["title"] = req_body["title"]
            if req_body.get("status"):
                item["status"] = req_body["status"]
            return "todo updated successfully"
        
    return "ID mismatch"

# delete multiple todos
@app.route("/delete-todo",methods=["PUT"])
def delete_multiple_todos():
    global data
    original_length = len(data)
    ids_to_delete = request.get_json()
    
    if not data:
        return "your todo bucket is empty to perform DELETE operation"
    
    if 'ids' not in ids_to_delete:
        return "invalid request"
    
    data = [item for item in data if item.get("id") not in ids_to_delete.get("ids")]
    
    if len(data) < original_length:
        return "todo deleted successfully"
    else:
        return "no todos found with provided IDs"
               
# delete todo
@app.route("/delete-todo/<int:todo_id>",methods=["DELETE"])
def delete_todo(todo_id):
    if not data:
        return "your todo bucket is empty to perform DELETE operation"
    
    for item in data:
        if item.get("id") == todo_id:
            data.remove(item)
            return "todo deleted successfully"
        
    return "ID mismatch"

# app run
if __name__ == "__main__":
    app.run(debug=True)