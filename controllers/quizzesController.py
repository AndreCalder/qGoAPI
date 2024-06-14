from mongoConnection import db
from bson import json_util
import json

quizzes = db["quizzes"]
print(quizzes)

def createQuiz(file, args):
    return ""

def getQuizzes(args):
    filteredQuizzes = list(quizzes.find(args))
    return filteredQuizzes

def updateQuiz(args):
    return ""

def deleteQuiz(id):
    return ""