import os
from flask import Flask, jsonify, request, render_template

app = Flask(__name__)


## List of Stores
stores = [
    {
        'name': 'My Rest Store',   
        'items':[
             {
              'name': 'My Item',
              'price': 12.99
             }
             
        ]
    }
]

@app.route('/')
def home():
    return render_template('index.html')


@app.route('/store')
def get_stores():
    return jsonify({'stores':stores})  ## turn list into dictionary


@app.route('/store/<string:name>', methods=['GET'])
def get_store(name):
    for store in stores:
        if store['name'] == name:
            return jsonify({'store' : store}) 
    return jsonify({'message': 'store not found'})



@app.route('/store', methods=['POST'])
def create_store():
    request_data = request.get_json()
    new_store = {
        'name': request_data['name'],
        'items': []
    }
    stores.append(new_store)   
    return jsonify(new_store)




@app.route('/store/<string:name>/item', methods=['POST'])
def create_item_in_store(name):
    request_data = request.get_json()
    for store in stores:
        if store['name'] == name:
            new_item = {
                'item': request_data['item'],
                'price': request_data['price']
            }
            store['items'].append(new_item)
            return jsonify(new_item)
    return jsonify({'message': 'store not found'})    


@app.route('/store/<string:name>/items', methods=['GET'])
def get_items_in_store(name):
    for store in stores:
        if store['name'] == name:
            return jsonify({'items' : store['items']})
    return jsonify({'message': 'store not found'})





if __name__ == '__main__':
    # Bind to PORT if defined, otherwise default to 5000.
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True) 

