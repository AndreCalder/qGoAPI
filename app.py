from flask import Flask
from routes.router import router

app = Flask(__name__)

#Calling the router blueprint
app.register_blueprint(router)

app.run(port=3000, debug=True)