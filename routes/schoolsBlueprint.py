from flask import Blueprint, request, g
from controllers.schoolsController import createSchool, getschools
from controllers.token import TokenController

schools_Router = Blueprint('schoolBlueprint',__name__)
tokenController = TokenController()

@schools_Router.before_request
def validate_token():
    if request.method != 'OPTIONS':
        token_data = tokenController.check_token(request.headers['Authorization'])
        print(token_data)
        if not token_data.get('isValid') or not token_data.get('roles').get('admin'):
            return {
                "message": "Invalid access token"
            }, 400
        else:
            g.userId = token_data.get('user_id')
            
@schools_Router.route('/', methods=['GET'])
def get():
    return getschools()
    
@schools_Router.route('/', methods=['POST'])
def create():
    return createSchool(request)