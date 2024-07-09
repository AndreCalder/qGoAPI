from datetime import datetime, timedelta, timezone
from docx import Document
from flask import jsonify, g
from mongoConnection import db
from bson import ObjectId, json_util
import json
from tempfile import NamedTemporaryFile

# GLOBAL AI QUIZ GENERATION FUNCTIONS
from controllers.common.generate_quiz import grade_answers, single_file_basic

import tempfile

quizzes = db["quizzes"]
questions = db["questions"]
answers = db["answers"]
quizResponse = db["quizResponses"]

# Takes pdf, doc, docx, ppt, pptx
def createQuiz(request):
    
    if request.form.get('function') == 'single_file_basic':
       return single_file_basic(request)
        
# Saves quiz and creates questions and relations in db
def saveQuiz(request):
    body = request.json.get('quiz')
    title = body.get('title')
    quiz_questions = body.get('questions')

    qArray = []

    for q in quiz_questions:
        qArray.append({
            "question": q.get("question"),
            "q_type": q.get("q_type"),
            "answers": q.get("answers"),
            "complete_answer": q.get("answer"),
            "justification": q.get("justification")
        })

    savedQuestions = questions.insert_many(qArray).inserted_ids

    quizData = {
        "title": title,
        "questions": savedQuestions,
        "createDate": datetime.now(),
        "createdBy": ObjectId(g.userId)
    }
    savedQuiz = quizzes.insert_one(quizData).inserted_id
    
    return str(savedQuiz)

def gradeOpenQ(request):
    return grade_answers(request)
    
# Saving quiz Response
def saveQuizResponse(request):
    #{
    #_id: ObjectId | undefined;
    #quizId: request.json['quizId']['$oid'];
    #responses: Array<QuestionResponse>;
    #};
    quizResponseData = {
        'quizId': ObjectId(request.json['quizId']['$oid']),
        'grade': request.json['grade'],
        'responses': request.json['responses'],
        'userId': ObjectId(g.userId),
        "createDate": datetime.now()
    }
    
    savedQuizResponse = quizResponse.insert_one(quizResponseData).inserted_id
    
    return str(savedQuizResponse)

def getQuizResponses(request):
    pipeline = [
        {
            '$match':
            {
                'userId': ObjectId(g.userId)
            }
        },
        {
            '$lookup':
            {
                'from': "quizzes",
                'localField': "quizId",
                'foreignField': "_id",
                'as': "quizName"
            },
        },
        {
            '$set': {
            'quizName': { '$arrayElemAt': ["$quizName.title", 0] }
            }
        },
        {'$sort':{'createDate':-1}},
        {'$limit': 5}
    ]
    quizResponses = quizResponse.aggregate(pipeline)
    return json.loads(json_util.dumps(quizResponses))

def getQuizResponseById(request, id):
    pipeline = [
        {
            '$match':
            {
                'userId': ObjectId(g.userId)
            }
        },
        {
            '$match':
                {
                    '_id': ObjectId(id)
                }
        },
        {
            '$lookup':
            {
                'from': "quizzes",
                'localField': "quizId",
                'foreignField': "_id",
                'as': "quizName"
            },
        },
        {
            '$set': {
            'quizName': { '$arrayElemAt': ["$quizName.title", 0] }
            }
        },
        {'$sort':{'createDate':-1}},
        {'$limit': 5}
    ]
    quizResponses = quizResponse.aggregate(pipeline)
    return json.loads(json_util.dumps(quizResponses))

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