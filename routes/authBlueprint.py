import datetime
import pprint
from flask import Blueprint, request
from controllers.quizzesController import getQuizById, getQuizzes, createQuiz, saveQuiz
from controllers.token import TokenController
from controllers.authController import AuthController

auth_Router = Blueprint('authBlueprint',__name__)
authController = AuthController()
tokenController = TokenController()

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
    if(datetime.datetime.fromtimestamp(token_data.get('exp')) > datetime.datetime.now()):
        data = {
            "user_id": token_data.get('user_id'),
            "username": token_data.get('username'),
        }
        access_token = tokenController.create_access_token(data)
        refresh_token = tokenController.create_refresh_token(data)
        
        return {
                "message": "Success",
                "access_token": access_token,
                "refresh_token": refresh_token,
                "user": token_data.get('username')
            }, 200
    return {
        "message": "Session Terminated"
    }, 400