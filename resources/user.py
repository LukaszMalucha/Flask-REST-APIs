from flask_restful import Resource, reqparse
from models.user import UserModel
from werkzeug.security import safe_str_cmp
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_refresh_token_required, get_jwt_identity, \
    jwt_required, get_raw_jwt
from blacklist import BLACKLIST

BLANK_ERROR = "{} cannot be blank."
NAME_ALREADY_EXISTS = "A user with that username already exists"
USER_SUCCESS = "User created successfully."
ERROR_CREATING = "An error occured while creating a store."
USER_NOT_FOUND = "User not found."
USER_DELETED = "User deleted"
INVALID_CREDENTIALS = "Invalid credentials"
LOGOUT_SUCCESS = 'Successfully logged out.'

_user_parser = reqparse.RequestParser()
_user_parser.add_argument('username',
                          type=str,
                          required=True,
                          help=BLANK_ERROR.format('username')
                          )
_user_parser.add_argument('password',
                          type=str,
                          required=True,
                          help=BLANK_ERROR.format('password')
                          )


class UserRegister(Resource):

    @classmethod
    def post(cls):
        data = _user_parser.parse_args()

        if UserModel.find_by_username(data['username']):
            return {"message": NAME_ALREADY_EXISTS}, 400

        user = UserModel(**data)
        user.save_to_db()

        return {"message": USER_SUCCESS}, 201


class User(Resource):

    @classmethod
    def get(cls, user_id: int):
        user = UserModel.find_by_id(user_id)
        if not user:
            return {'message': USER_NOT_FOUND}, 404
        return user.json()

    @classmethod
    def delete(cls, user_id: int):
        user = UserModel.find_by_id(user_id)
        if not user:
            return {'message': USER_NOT_FOUND}, 404
        user.delete_from_db()
        return {'message': USER_DELETED}, 200


class UserLogin(Resource):

    @classmethod
    def post(cls):
        data = _user_parser.parse_args()
        user = UserModel.find_by_username(data['username'])

        if user and safe_str_cmp(user.password, data['password']):
            access_token = create_access_token(identity=user.id, fresh=True)
            refresh_token = create_refresh_token(user.id)
            return {
                       'access_token': access_token,
                       'refresh_token': refresh_token
                   }, 200

        return {'message': INVALID_CREDENTIALS}, 401


class UserLogout(Resource):
    @classmethod
    @jwt_required
    def post(cls):
        """Blacklist used token"""
        jti = get_raw_jwt()['jti']  # jti is JWT ID
        BLACKLIST.add(jti)
        return {'message': LOGOUT_SUCCESS}, 200


class TokenRefresh(Resource):
    @classmethod
    @jwt_refresh_token_required
    def post(cls):
        """Renewing token"""
        current_user = get_jwt_identity()
        new_token = create_access_token(identity=current_user, fresh=False)
        return {'access_token': new_token}, 200
