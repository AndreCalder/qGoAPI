from flask import Blueprint
from routes.routesBueprint import routes_Blueprint
from routes.quizzesBlueprint import quizzes_Router
from routes.userBlueprint import user_Router
from routes.authBlueprint import auth_Router

# Routing file, add all new routes here

router = Blueprint('router',__name__)

router.register_blueprint(quizzes_Router, url_prefix='/quizzes')
router.register_blueprint(user_Router, url_prefix='/users')
router.register_blueprint(auth_Router, url_prefix='/auth')