import pprint
from flask import Blueprint, request
from controllers.quizzesController import getQuizzes, createQuiz

quizzes_Router = Blueprint('quizzesBlueprint',__name__)

@quizzes_Router.route('/', methods=['GET'])
def get():
    pprint.pprint(request.args.to_dict())
    filteredRoutes = getQuizzes(request.args.to_dict())
    return filteredRoutes

@quizzes_Router.route('/', methods=['POST'])
def create():
    return createQuiz(request)