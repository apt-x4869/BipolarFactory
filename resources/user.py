from flask_restful import Resource, reqparse

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
        
        if UserModel.find_by_username(data['username']):
            return {"message": "A user with username '{}' already exist".format(data[username])}, 400
        
        user = UserModel(**data)
        user.save_to_db()
        return {"message": "You have been Registered"}, 200