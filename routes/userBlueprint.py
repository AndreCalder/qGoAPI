import pprint
from flask import Blueprint, request
from controllers.userController import UserController

user_Router = Blueprint('usersBlueprint',__name__)
userController = UserController()

@user_Router.route('/', methods=['POST'])
def createUser():
    req = request.json
    username = req.get('username')
    password = req.get('password') 
    
    return userController.create_user(username, password)
    
@user_Router.route('/getByName', methods=['GET'])
def getUser():
    username = request.args.to_dict().get("username")
    if username:
        user = userController.get_user(username)
        if user:
            return user, 200
        else:
            return {"message": "User not found"}, 204
    else:
        return {"message": "Invalid request"}, 400