import json
from bson import ObjectId, json_util
from mongoConnection import db
import bcrypt

users = db["users"]

class UserController:
    
    def get_user(self, username):
        user = users.find_one({"username": username})
        return json.loads(json_util.dumps(user))
    
    def create_user(self, username, password):
        user = self.get_user(username)
        
        if user:
            return "User already exists"
        
        salt = bcrypt.gensalt(10)
        hashedpass = bcrypt.hashpw(password.encode('utf-8'), salt)
        createduser = users.insert_one({"username": username, "password": hashedpass.decode('utf-8')})
        return "a"
        return {"userId": str(createduser.inserted_id)}, 200
    
        