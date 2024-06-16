from mongoConnection import db
from bson import json_util
import json
from tempfile import NamedTemporaryFile

# GLOBAL AI QUIZ GENERATION FUNCTIONS
from controllers.common.generate_quiz import single_file_basic

quizzes = db["quizzes"]

def createQuiz(request):
    
    print(request.files['file'])

    match request.form.get('function'):
       case 'single_file_basic' : return single_file_basic(request)

def getQuizzes(args):
    # Este cambio va a ai
    filteredQuizzes = list(quizzes.find(args))
    return json.loads(json_util.dumps(filteredQuizzes))

def updateQuiz(args):
    return ""

def deleteQuiz(id):
    return ""