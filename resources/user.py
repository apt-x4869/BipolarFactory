from flask_restful import Resource, reqparse
from werkzeug.security import safe_str_cmp
import hashlib
from blacklist import BLACKLIST
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    jwt_required,
    get_raw_jwt,
    jwt_refresh_token_required,
    get_jwt_identity
)

from models.user import UserModel


_user_parser = reqparse.RequestParser()
_user_parser.add_argument('username',
                          type=str,
                          required=True,
                          help="Username is Required")
_user_parser.add_argument('password',
                          type=str,
                          required=True,
                          help="Username is Required")


class UserRegister(Resource):
    def post(self):
        data = _user_parser.parse_args()
        
        if UserModel.find_by_username(username=data['username']):
            return {"message": "A user with username '{}' already exist".format(data['username'])}, 400
        
        user = UserModel(**data)
        user.save_to_db()
        return {"message": "You have been Registered"}, 200

class UserLogin(Resource):
    def post(self):
        data = _user_parser.parse_args()

        user = UserModel.find_by_username(data['username'])

        if user and safe_str_cmp(user.password, hashlib.md5(data['password'].encode()).hexdigest()):

            access_token = create_access_token(identity=user.id, fresh=True)
            refresh_token = create_refresh_token(identity=user.id)
            return {
                'access_token': access_token,
                'refresh_token': refresh_token
            }, 200

        return {"message":"Invalid Credential"}, 401

class UserLogout(Resource):
    @jwt_required
    def post(self):
        jti = get_raw_jwt()['jti']
        BLACKLIST.add(jti)
        return {"message": "You have been successfully logged out"}

class TokenRefresh(Resource):
    @jwt_refresh_token_required
    def post(self):
        current_user = get_jwt_identity()
        new_token = create_access_token(identity=current_user,fresh=False)
        return {"access_token": new_token }, 200