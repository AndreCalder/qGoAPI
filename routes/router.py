from flask import Blueprint
from routes.routesBueprint import routes_Blueprint
from routes.quizzesBlueprint import quizzes_Router

# Routing file, add all new routes here

router = Blueprint('router',__name__)

router.register_blueprint(quizzes_Router, url_prefix='/quizzes')