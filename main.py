from flask import Flask
from routes.router import router
from flask_cors import CORS, cross_origin
from flask_bcrypt import Bcrypt

app = Flask(__name__)
cors = CORS(app, resources={r"/*": {"origins": "*"}})

@app.route('/_ah/warmup')
def warmup():
    # Perform any necessary initialization here
    return '', 200

#Calling the router blueprint
app.register_blueprint(router)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000, debug=True)