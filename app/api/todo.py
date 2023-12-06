from flask import request , jsonify , abort , Blueprint
from flask import current_app as app

todo_bp = Blueprint('todo',__name__)


# GET Route to display one todo
@todo_bp.route('/todo/<ObjectId:id>', methods=["GET"])
def display_single_todo(id):
   mongo = app.extensions['mongo']
   todo = mongo.db.todo.find_one({"_id": id})
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
@todo_bp.route('/todo', methods=["GET"])
def display_todo():
   mongo = app.extensions['mongo']
   todos =list(mongo.db.todo.find()) 
   for x in todos:
       x['_id']= str(x['_id'])
   return jsonify({"data":todos ,"count":len(todos)})


#POST Route to add a todo
@todo_bp.route('/todo',methods=["POST"])
def add_todo():
    mongo = app.extensions['mongo']
    if not request.json:
        abort(500)
    title = request.json.get("title",None)
    des = request.json.get("description","")
    if title is None:
        return jsonify(message="Invalid Request"), 500
    mongo.db.todo.insert_one({'title': title, 'description': des})
    return jsonify(message="Added Successfully") 
        

#PATCH Route to update a todo
@todo_bp.route('/todo/<ObjectId:id>' , methods=["PATCH"])
def update_todo(id):
   mongo = app.extensions['mongo']
   if not request.json:
       abort(500)
   data = request.json
   if "title" in data or "description" in data:
       mongo.db.todo.find_one_and_update({'_id':id} , {"$set": data})
       return jsonify(message="Updated Successfully")
   else:
       return jsonify(message="KeyValue Error")


#DELETE Route to delete a todo
@todo_bp.route('/todo/<ObjectId:id>' , methods=["DELETE"])
def delete_todo(id):
   mongo = app.extensions['mongo']
   todo = mongo.db.todo.find_one_and_delete({'_id': id})
   if  not todo:
       return jsonify({
           "message":"Todo not found",
           "success": False
           })
   return jsonify({
       "message":"Deleted Successfully",
       "success": True
       })