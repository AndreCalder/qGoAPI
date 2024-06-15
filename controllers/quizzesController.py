from mongoConnection import db
from bson import json_util
import json

quizzes = db["quizzes"]

def createQuiz(file, args):
    return ""

def getQuizzes(args):
    # Este cambio va a ai
    filteredQuizzes = list(quizzes.find(args))
    return json.loads(json_util.dumps(filteredQuizzes))

def updateQuiz(args):
    return ""

def deleteQuiz(id):
    return ""