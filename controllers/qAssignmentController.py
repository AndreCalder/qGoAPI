import datetime
import json
from bson import ObjectId, json_util
from mongoConnection import db
from flask import g
from controllers.userController import UserController
from controllers.schoolsController import getschool
from controllers.quizzesController import getQuizById
from datetime import datetime

userController = UserController()

groups = db["groups"]
assignments = db["quizAssignments"]

def createAssignment(request):
    body = request.json
    
    quiz = getQuizById(body.get("quiz_id"))
    
    if len(quiz == 0):
        return {
            "message": "Quiz does not exist"
        }, 400
        
    assignmentName = quiz[0].get("title") + ' ' + body.get("startDate")
    
    groupData = {
        "name": assignmentName,
        "quiz_id": ObjectId(body.get("quiz_id")),
        "group_id": ObjectId(body.get("group_id")),
        "createdBy": ObjectId(g.userId), 
        "tries": body.get("tries"),
        "startDate": datetime.strptime(body.get("startDate"), '%b %d %Y %I:%M%p').isoformat(),
        "endDate": datetime.strptime(body.get('endDate'), '%b %d %Y %I:%M%p').isoformat()
    }
    
    assignment_id = assignments.insert_one(groupData).inserted_id
    
    return str(assignment_id)

def getAssignments(request):
    
    studentGroup = json.loads(json_util.dumps(groups.find({"students": ObjectId(g.userId)})))
    
    group_ids = [ObjectId(group["_id"]["$oid"]) for group in studentGroup]
    print(group_ids)
    
    groupAssignments = assignments.find({"$and": [{"group_id": {"$in": group_ids}}]})
    
    return json.loads(json_util.dumps(groupAssignments))