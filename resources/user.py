import traceback
from flask import request, render_template, make_response
from flask_restful import Resource
from models.user import UserModel
from werkzeug.security import safe_str_cmp
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_refresh_token_required, get_jwt_identity, \
    jwt_required, get_raw_jwt
from marshmallow import ValidationError
from blacklist import BLACKLIST
from schemas.user import UserSchema
from libs.mailgun import MailGunException
from models.confirmation import ConfirmationModel

BLANK_ERROR = "{} cannot be blank."
NAME_ALREADY_EXISTS = "A user with that username already exists"
EMAIL_ALREADY_EXISTS = "That email is already registered"
FAILED_TO_CREATE = "Unable to register user at this time"
REGISTER_SUCCESS = "Account created successfully. An email with the activation link has been sent."
ERROR_CREATING = "An error occured while creating a store."
USER_NOT_FOUND = "User not found."
USER_DELETED = "User deleted"
INVALID_CREDENTIALS = "Invalid credentials"
LOGOUT_SUCCESS = "Successfully logged out."
NOT_ACTIVATED_ERROR = "Registration not cofirmed, please check your email."
USER_ACTIVATED = "Registration completed,  your account is activated."

user_schema = UserSchema()


class UserRegister(Resource):

    @classmethod
    def post(cls):
        user = user_schema.load(request.get_json())

        if UserModel.find_by_username(user.username):
            return {"message": NAME_ALREADY_EXISTS}, 400

        if UserModel.find_by_email(user.email):
            return {"message": EMAIL_ALREADY_EXISTS}, 400

        try:
            user.save_to_db()
            confirmation = ConfirmationModel(user.id)
            confirmation.save_to_db()
            user.send_confirmation_email()
            return {"message": REGISTER_SUCCESS}, 201
        except MailGunException as e:
            user.delete_from_db()
            return {"message": str(e)}, 500
        except: # user failed to save to db
            traceback.print_exc()
            user.delete_from_db()
            return {"message": FAILED_TO_CREATE}, 500

class User(Resource):

    @classmethod
    def get(cls, user_id: int):
        user = UserModel.find_by_id(user_id)
        if not user:
            return {'message': USER_NOT_FOUND}, 404
        return user_schema.dump(user), 200

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
        user_json = request.get_json()
        user_data = user_schema.load(user_json, partial=('email',))  # no need for email in login if not present

        user = UserModel.find_by_username(user_data.username)

        if user and safe_str_cmp(user.password, user_data.password):
            # Check if user is activated
            confirmation = user.most_recent_confirmation
            if confirmation and confirmation.confirmed:
                access_token = create_access_token(identity=user.id, fresh=True)
                refresh_token = create_refresh_token(user.id)
                return {
                           'access_token': access_token,
                           'refresh_token': refresh_token
                       }, 200
            return {"message": NOT_ACTIVATED_ERROR.format(user.username)}, 400

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
