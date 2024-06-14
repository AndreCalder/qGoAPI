from flask import Blueprint, request
import mongoConnection
from bson import json_util
import json
from controllers.routesController import getRoutes

routes_Blueprint = Blueprint('routesBlueprint',__name__)

routesCollection = mongoConnection.db["routes"]

@routes_Blueprint.route('/')
def get():
    filteredRoutes = getRoutes(request.args.to_dict())
    return filteredRoutes