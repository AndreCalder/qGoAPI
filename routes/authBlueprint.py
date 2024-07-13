import datetime
import pprint
from flask import Blueprint, request
from controllers.quizzesController import getQuizById, getQuizzes, createQuiz, saveQuiz
from controllers.schoolsController import getschool
from controllers.token import TokenController
from controllers.authController import AuthController
from controllers.userController import UserController

auth_Router = Blueprint('authBlueprint',__name__)
authController = AuthController()
tokenController = TokenController()
userController = UserController()

@auth_Router.route('/login', methods=['POST'])
def get():
    req = request.json
    username = req.get('username')
    password = req.get('password') 
    
    if not username or not password:
        return {"message":"Authentication Required"}, 400
    
    return authController.login(username, password)

@auth_Router.route('/validatetoken', methods=['POST'])
def validateToken():
    token_data = tokenController.check_token(request.headers['Authorization'])
    roles = token_data.get('roles')
    user_id = token_data.get('user_id')
    user = userController.get_user_byId(user_id)
    
    #Set school as empty
    school = None
    if roles.get('teacher'):
        school = getschool(user.get('school_id'))
    elif not roles.get('admin'):
        school= getschool(user.get('school_id'))
        
    if token_data.get('isValid'):
        return {
                "message": "Success",
                "access_token": token_data.get('access_token'),
                "refresh_token": token_data.get('refresh_token'),
                "username": token_data.get('username'),
                "roles": token_data.get('roles')
            }, 200
            
    return {
        "message": "Session Terminated"
    }, 400