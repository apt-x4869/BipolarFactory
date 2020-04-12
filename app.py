from flask import Flask, jsonify
from flask_restful import Api
from flask_jwt_extended import JWTManager
from resources.user import UserRegister, UserLogin, UserLogout, TokenRefresh, User
from resources.book import Book
from blacklist import BLACKLIST

from db import db

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['JWT_SECRET_KEY'] = 'AMAN'
app.config['JWT_BLACKLIST_ENABLED'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
api = Api(app)

@app.before_first_request
def create_tables():
    db.create_all()

jwt = JWTManager(app)

@jwt.user_claims_loader
def add_claims_to_jwt(identity):
    if identity == 1:
        return {'is_admin': True}
    return {'is_admin': False}

@jwt.token_in_blacklist_loader
def check_if_token_in_blacklist(decrypted_token):
    return decrypted_token['jti'] in BLACKLIST

api.add_resource(UserRegister, '/register')
api.add_resource(UserLogin, '/login')
api.add_resource(UserLogout,'/logout')
api.add_resource(TokenRefresh,'/refresh')
api.add_resource(User,'/user/<int:user_id>')
api.add_resource(Book, '/book/<string:title>')
if __name__ == '__main__':
    db.init_app(app)
    app.run(port=5000, debug=True)