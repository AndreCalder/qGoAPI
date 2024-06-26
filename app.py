from flask import Flask
from routes.router import router
from flask_cors import CORS, cross_origin
from flask_bcrypt import Bcrypt

app = Flask(__name__)
cors = CORS(app, resources={r"/*": {"origins": "*"}})

#Calling the router blueprint
app.register_blueprint(router)

app.run(port=3000, debug=True)