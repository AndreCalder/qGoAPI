import datetime

from flask import jsonify
from mongoConnection import db
from bson import ObjectId, json_util
import json
from tempfile import NamedTemporaryFile

# GLOBAL AI QUIZ GENERATION FUNCTIONS
from controllers.common.generate_quiz import single_file_basic

quizzes = db["quizzes"]
questions = db["questions"]
answers = db["answers"]

# Takes pdf, doc, docx, ppt, pptx
def createQuiz(request):
    match request.form.get('function'):
       case 'single_file_basic' : return single_file_basic(request)
        
# Saves quiz and creates questions and relations in db
def saveQuiz(request):
    body = request.json.get('quiz')
    title = body.get('title')
    quiz_questions = body.get('questions')

    qArray = []

    for q in quiz_questions:
        qArray.append({
            "question": q.get("question"),
            "answers": q.get("answers")
        })

    savedQuestions = questions.insert_many(qArray).inserted_ids

    quizData = {
        "title": title,
        "questions": savedQuestions,
        "createDate": datetime.datetime.now(tz=datetime.timezone.utc),
    }
    savedQuiz = quizzes.insert_one(quizData).inserted_id
    
    return str(savedQuiz)

def getQuizById(id):
    pipeline = [
        {
            '$match':
            {
                '_id': ObjectId(id)
            }
        },
        {
            '$lookup':
            {
                'from': "questions",
                'localField': "questions",
                'foreignField': "_id",
                'as': "questions"
            },
        }
    ]
    quiz = quizzes.aggregate(pipeline)
    return json.loads(json_util.dumps(quiz))

# Returns filtered quizzes
def getQuizzes(args):
    pipeline = []

    if(args.get('aggregate')):
        pipeline.append({
            '$lookup':
            {
                'from': "questions",
                'localField': "questions",
                'foreignField': "_id",
                'as': "questions"
            },
        })

    filteredQuizzes = list(quizzes.aggregate(pipeline))
    return json.loads(json_util.dumps(filteredQuizzes))

def updateQuiz(args):
    return ""

def deleteQuiz(id):
    return ""