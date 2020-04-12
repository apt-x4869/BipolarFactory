from flask import Flask, jsonify
from flask_restful import Api
from flask_jwt_extended import JWTManager
from resources.user import UserRegister

from db import db

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['JWT_SECRET_KEY'] = 'AMAN'
api = Api(app)

jwt = JWTManager(app)


api.resource(UserRegister,'/register')

if __name__ == '__main__':
    db.init_app(app)
    app.run(port=5000, debug=True)