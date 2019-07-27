import os
import env
from flask import Flask, jsonify
from flask_restful import Api
from flask_jwt_extended import JWTManager
from marshmallow import ValidationError
from flask_uploads import configure_uploads, patch_request_class

from resources.user import User, UserRegister, UserLogin, UserLogout, TokenRefresh
from resources.item import Item, ItemList
from resources.store import Store, StoreList
from resources.confirmation import Confirmation, ConfirmationByUser
from resources.image import ImageUpload, Image, AvatarUpload, Avatar
from libs.image_helper import IMAGE_SET
from blacklist import BLACKLIST
from ma import ma

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')
# app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('SQLALCHEMY_DATABASE_URI')
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('POSTGRES_DATABASE_URI')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # do not track changes until saved
app.config['PROPAGATE_EXCEPTIONS'] = True  # flask extensions can raise their own errors
app.config['JWT_BLACKLIST_ENABLED'] = True  # enable blacklisting user id's
app.config['JWT_BLACKLIST_TOKEN_CHECKS'] = ['access', 'refresh']  # enable blacklist for those functions
app.config['JWT_SECRET_KEY'] = os.environ["JWT_SECRET_KEY"]
app.config['UPLOADED_IMAGES_DEST'] = os.path.join("static", "images")
app.config['DEBUG'] = True
patch_request_class(app, 10 * 1024 * 1024)  # 10MB image size limit
configure_uploads(app, IMAGE_SET) # img extensions
api = Api(app)


@app.errorhandler(ValidationError)
def handle_marshmallow_validation(error):
    return jsonify(error.messages), 400

# Enable jwt authentication (check resources.user.UserLogin)
jwt = JWTManager(app)


@jwt.token_in_blacklist_loader
def chcek_if_token_in_blacklist(decrypted_token):
    return decrypted_token['identity'] in BLACKLIST


api.add_resource(User, '/user/<int:user_id>')
api.add_resource(UserRegister, '/register')
api.add_resource(UserLogin, '/login')
api.add_resource(UserLogout, '/logout')
api.add_resource(TokenRefresh, '/refresh')
api.add_resource(Item, '/item/<string:name>')
api.add_resource(ItemList, '/items')
api.add_resource(Store, '/store/<string:name>')
api.add_resource(StoreList, '/stores')
api.add_resource(Confirmation, '/user_confirmation/<string:confirmation_id>')
api.add_resource(ConfirmationByUser, '/confirmation/user/<int:user_id>')
api.add_resource(ImageUpload, '/upload/image')
api.add_resource(Image, '/image/<string:filename>')
api.add_resource(AvatarUpload, '/upload/avatar')
api.add_resource(Avatar, "/avatar/<int:user_id>")


if __name__ == '__main__':

    from db import db
    db.init_app(app)
    ma.init_app(app)

    if app.config['DEBUG']:
        @app.before_first_request
        def create_tables():
            db.create_all()

    app.run()
