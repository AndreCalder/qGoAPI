import pprint
from flask import Blueprint, request
from controllers.quizzesController import getQuizById, getQuizzes, createQuiz, saveQuiz

quizzes_Router = Blueprint('quizzesBlueprint',__name__)

@quizzes_Router.route('/', methods=['GET'])
def get():
    print(request.args.to_dict())
    filteredRoutes = getQuizzes(request.args.to_dict())
    return filteredRoutes

@quizzes_Router.route('/<id>')
def getQuiz(id):
    return getQuizById(id)

@quizzes_Router.route('/', methods=['POST'])
def create():
    return createQuiz(request)

@quizzes_Router.route('/save', methods=['POST'])
def saveNewQuiz():
    return saveQuiz(request)