import os
from flask import Flask
from flask_restful import Api
from flask_jwt import JWT

from security import authenticate, identity
from resources.user_register import UserRegister
from resources.item import Item, ItemList
from resources.store import Store, StoreList


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQALCHEMY_TRACK_MODIFICATIONS']= False                          ## turn off tracker
app.secret_key = "biggest_secret"
api = Api(app)


## RUN BEFORE FIRST REQUEST
@app.before_first_request
def create_tables():
    db.create_all()


jwt = JWT(app, authenticate, identity)              # /auth


api.add_resource(Item, '/item/<string:name>') ## assign resource
api.add_resource(ItemList, '/items')
api.add_resource(Store, '/store/<string:name>') ## assign resource
api.add_resource(StoreList, '/stores')
api.add_resource(UserRegister, '/register')




if __name__ == '__main__':
    from db import db                           ## avoiding circular imports
    db.init_app(app)
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True) 
