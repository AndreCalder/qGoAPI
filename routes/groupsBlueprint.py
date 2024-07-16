from flask import Blueprint, request, g
from controllers.schoolsController import createSchool, getschools
from controllers.groupsController import getGroupById, getTeacherGroups
from controllers.token import TokenController

groups_Router = Blueprint('groupsBlueprint',__name__)
tokenController = TokenController()

@groups_Router.before_request
def validate_token():
    if request.method != 'OPTIONS':
        token_data = tokenController.check_token(request.headers['Authorization'])

        # ADD PERMISSION VALIDATIONS HERE
        
        g.userId = token_data.get('user_id')
        
@groups_Router.route('/byGroupID/<id>', methods=['GET'])
def getByID(id):
    return getGroupById(id)   
 
@groups_Router.route('/teachergroups', methods=['GET'])
def get():
    return getTeacherGroups(request)
    
@groups_Router.route('/', methods=['POST'])
def create():
    return createSchool(request)