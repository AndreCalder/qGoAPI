from flask import Blueprint, request, g
from controllers.qAssignmentController import createAssignment, getAssignments
from controllers.schoolsController import createSchool, getschools
from controllers.groupsController import getGroupById, getTeacherGroups
from controllers.token import TokenController

quizAssignment_router = Blueprint('qAssignmentBlueprint',__name__)
tokenController = TokenController()

@quizAssignment_router.before_request
def validate_token():
    if request.method != 'OPTIONS':
        token_data = tokenController.check_token(request.headers['Authorization'])

        # ADD PERMISSION VALIDATIONS HERE
        
        g.userId = token_data.get('user_id')
        
@quizAssignment_router.route('/', methods=['POST'])
def create():
    return createAssignment(request)

@quizAssignment_router.route('/getStudentAssignments', methods=['GET'])
def getStudentAssignments():
    return getAssignments(request)