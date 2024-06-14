import mongoConnection
from bson import json_util
import json


routesCollection = mongoConnection.db["routes"]

def getRoutes(args):
    filteredRoutes = list(routesCollection.find(args))
    return json.loads(json_util.dumps(filteredRoutes))