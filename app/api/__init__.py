from flask import Flask , request , jsonify , abort
from flask_pymongo import PyMongo , ObjectId
import os

def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev'
    )
    mongodb_client = PyMongo(app, uri="mongodb://localhost:27017/todo_af")
    db = mongodb_client.db

    if test_config is None:
        app.config.from_pyfile('config.py', silent=True)
    else:
        app.config.from_mapping(test_config)

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass


    #GET Route to display one todo
    @app.route('/todo/<ObjectId:id>', methods=["GET"])
    def display_single_todo(id):
        todo = db.todo.find_one({"_id": id})
        if  not todo:
            return jsonify({
                "message":"Id not found",
                "success": False
                })
        todo['_id']=str(todo['_id'])
        return jsonify({
            "data": todo,
            "success": True
            })
        
    #GET Route to display all todos
    @app.route('/todo', methods=["GET"])
    def display_todo():
        todos =list(db.todo.find()) 
        for x in todos:
            x['_id']= str(x['_id'])
        return jsonify({"data":todos ,"count":len(todos)})


    #POST Route to add a todo
    @app.route('/todo',methods=["POST"])
    def add_todo():
        if not request.json:
            abort(500)
        title = request.json.get("title",None)
        des = request.json.get("description","")
        if title is None:
            return jsonify(message="Invalid Request"), 500
        db.todo.insert_one({'title': title, 'description': des})
        return jsonify(message="Added Successfully") 
        

    #PATCH Route to update a todo
    @app.route('/todo/<ObjectId:id>' , methods=["PATCH"])
    def update_todo(id):
        if not request.json:
            abort(500)
        data = request.json
        if "title" in data or "description" in data:
            db.todo.find_one_and_update({'_id':id} , {"$set": data})
            return jsonify(message="Updated Successfully")
        else:
            return jsonify(message="KeyValue Error")
        

    #DELETE Route to delete a todo
    @app.route('/todo/<ObjectId:id>' , methods=["DELETE"])
    def delete_todo(id):
        todo = db.todo.find_one_and_delete({'_id': id})
        if  not todo:
            return jsonify({
                "message":"Todo not found",
                "success": False
                })
        return jsonify({
            "message":"Deleted Successfully",
            "success": True
         })
    
    return app