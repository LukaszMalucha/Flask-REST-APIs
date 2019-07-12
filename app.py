import os
import env
from flask import Flask, jsonify
from flask_restful import Api
from flask_jwt_extended import JWTManager
from resources.user import User, UserRegister, UserLogin, UserLogout, TokenRefresh
from resources.item import Item, ItemList
from blacklist import BLACKLIST
from ma import ma

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('SQLALCHEMY_DATABASE_URI')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # do not track changes until saved
app.config['PROPAGATE_EXCEPTIONS'] = True  # flask extensions can raise their own errors
app.config['JWT_BLACKLIST_ENABLED'] = True  # enable blacklisting user id's
app.config['JWT_BLACKLIST_TOKEN_CHECKS'] = ['access', 'refresh']  # enable blacklist for those functions
app.config['DEBUG'] = True
api = Api(app)

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


if __name__ == '__main__':
    from db import db

    db.init_app(app)
    ma.init_app(app)

    if app.config['DEBUG']:
        @app.before_first_request
        def create_tables():
            db.create_all()

    app.run()
