from flask import Flask

app = Flask(__name__)

stores = [
    {
        'name': "My Store",
        'items': [
            {
                'name': 'My Item',
                'price': 15.99

            }

        ]

    }

]


@app.route('/store', methods=['POST'])
def create_store():
    pass


@app.route('/store/<string:name>')
def get_store(name):
    pass


@app.route('/stores')
def get_stores():
    pass


@app.route('/store/<string:name>/item', methods=['POST'])
def create_item_in_store(name):
    pass


@app.route('/store/<string:name>/item')
def get_item_in_store(name):
    pass


app.run()
