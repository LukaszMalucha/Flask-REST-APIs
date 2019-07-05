import os
from flask import Flask, request
from flask_restful import Resource, Api, reqparse
from flask_jwt import JWT, jwt_required

from security import authenticate, identity


app = Flask(__name__)
app.secret_key = "biggest_secret"
api = Api(app)

jwt = JWT(app, authenticate, identity)              # /auth


items = []



## define resource
class Item(Resource):
    parser = reqparse.RequestParser()                                 ## parse request - make sure only required fields are passed   
    parser.add_argument('price',
                        type=float,
                        required=True,
                        help="This field cannot be blank!"
                        )
    data = parser.parse_args()
        
    ## get method
    @jwt_required()
    def get(self, name):              
        item = next(filter(lambda x: x['name'] == name, items), None)     ## filter out results and get first matching item; if not found return None
        return {'item': item}, 200 if item else 404                       ## return in case not found 
        
        
    def post(self, name):
        if next(filter(lambda x: x['name'] == name, items), None):        ## make sure names are unique
            return {'message': " {} already exists".format(name)}, 400    ## bad request
        
        data = Item.parser.parse_args()
        
        item = {'name': name, 'price': data['price']}
        items.append(item)
        return item, 201
        
    def delete(self, name):
        global items                                                      ## bring in global variable
        items = list(filter(lambda x: x['name'] != name, items))
        return {'message': 'Item deleted'}
            
    def put(self, name):                                                  ## crate/update method  
        item = next(filter(lambda x: x['name'] == name, items), None) 
        
        data = Item.parser.parse_args()
        
        if item is None:
            item = {'name': name, 'price': data['price']}
            items.append(item)
        else:
            item.update(data)
        return item    
            
        
        
    
class ItemsList(Resource):
    
    def get(self):
        return {'items' : items}
        
        
        
        

api.add_resource(Item, '/item/<string:name>') ## assign resource
api.add_resource(ItemsList, '/items')


if __name__ == '__main__':
    # Bind to PORT if defined, otherwise default to 5000.
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True) 
