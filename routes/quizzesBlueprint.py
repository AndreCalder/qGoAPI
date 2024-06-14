import pprint
from flask import Blueprint, request
from controllers.quizzesController import getQuizzes

quizzes_Router = Blueprint('quizzesBlueprint',__name__)

@quizzes_Router.route('/')
def get():
    pprint.pprint(request.args.to_dict())
    filteredRoutes = getQuizzes(request.args.to_dict())
    return filteredRoutes