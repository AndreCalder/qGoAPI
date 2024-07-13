import datetime
import json
from bson import ObjectId, json_util
from mongoConnection import db

schools = db["schools"]

def createSchool(request):
    body = request.form
    
    schoolData = {
        "name": body.get("schoolName"),
        "groupsCount": int(body.get("groups")),
        "groupSize": int(body.get("groupSize")),
        "teachersCount": int(body.get("teachers")),
        "preferredPrimary": body.get("preferredPrimary"),
        "teachers": [],
        "groups": [],
        "is_active": True,
        "createDate": datetime.now()
    }
    
    savedQuiz = schools.insert_one(schoolData).inserted_id
    
    return str(savedQuiz)

def getschool(id):
    if isinstance(id, dict):
        school_id = id.get('$oid')
        return json.loads(json_util.dumps(schools.find_one({"_id": ObjectId(school_id)})))
    elif isinstance(id, str):
        return json.loads(json_util.dumps(schools.find_one({"_id": ObjectId(id)})))
    
def getschools():
    return json.loads(json_util.dumps(schools.find()))