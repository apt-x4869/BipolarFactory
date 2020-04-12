from flask import Flask, jsonify
from flask_restful import Api
from flask_jwt_extended import JWTManager


app = Flask(__name__)
app.config['JWT_SECRET_KEY'] = 'AMAN'
api = Api(app)

jwt = JWTManager(app)


if __name__ == '__main__':

    app.run(port=5000, debug=True)