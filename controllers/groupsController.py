import datetime
import json
from bson import ObjectId, json_util
from mongoConnection import db
from flask import g
from controllers.userController import UserController
from controllers.schoolsController import getschool
userController = UserController()

groups = db["groups"]

def createGroup(request):
    body = request.json
    
    groupData = {
        "school_id": ObjectId(body.get("school_id")),
        "teacher_id": ObjectId(g.userId), 
        "students": [],
        "createDate": datetime.now()
    }
    
    savedGroup = groups.insert_one(groupData).inserted_id
    
    return str(savedGroup)

def getGroupById(id):
    pipeline = [
        {
            "$match": {
                "_id": ObjectId(id)
            }
        },
        {
            "$lookup":{
                "from": "users",
                "localField": "students",
                "foreignField": "_id",
                "as": "students"
            }
        }
    ]
    
    teacherGroups = groups.aggregate(pipeline)
    return json.loads(json_util.dumps(teacherGroups))[0]

def getTeacherGroups(request):
    
    teacher = userController.get_user_byId(g.userId)
    
    pipeline = [
        {
            "$match": {
                "$and": [
                    {
                        "teacher_id": ObjectId(teacher.get("_id").get("$oid")),
                        "school_id": ObjectId(teacher.get("school_id").get("$oid"))
                    }
                ]
            }
        },
        {
            "$lookup":{
                "from": "users",
                "localField": "students",
                "foreignField": "_id",
                "as": "students"
            }
        }
    ]
    
    teacherGroups = groups.aggregate(pipeline)
    return json.loads(json_util.dumps(teacherGroups))