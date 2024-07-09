import pprint
from flask import Blueprint, request, g
from controllers.quizzesController import getQuizById, getQuizResponseById, getQuizResponses, getQuizzes, createQuiz, gradeOpenQ, saveQuiz, saveQuizResponse
from controllers.token import TokenController

tokenController = TokenController()

quizzes_Router = Blueprint('quizzesBlueprint',__name__)

@quizzes_Router.before_request
def validate_token():
    if request.method != 'OPTIONS':
        token_data = tokenController.check_token(request.headers['Authorization'])
        
        if not token_data.get('isValid'):
            return {
                "message": "Invalid access token"
            }, 400
        else:
            g.userId = token_data.get('user_id')
    
@quizzes_Router.route('/', methods=['GET'])
def get():
    filteredRoutes = getQuizzes(request.args.to_dict())
    return filteredRoutes

@quizzes_Router.route('/<id>')
def getQuiz(id):
    return getQuizById(id)

@quizzes_Router.route('/', methods=['POST'])
def create():
    return createQuiz(request)

@quizzes_Router.route('/gradeAnswers', methods=['POST'])
def grade():
    return gradeOpenQ(request)

@quizzes_Router.route('/saveResponse', methods=['POST'])
def saveResponse():
    return saveQuizResponse(request)

@quizzes_Router.route('/getResponses', methods=['GET'])
def getResponses():
    return getQuizResponses(request)

@quizzes_Router.route('/getResponses/<id>', methods=['GET'])
def getResponsesById(id):
    return getQuizResponseById(request, id)

@quizzes_Router.route('/save', methods=['POST'])
def saveNewQuiz():
    return saveQuiz(request)