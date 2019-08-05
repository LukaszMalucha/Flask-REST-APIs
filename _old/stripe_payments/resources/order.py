from flask import request
from flask_restful import Resource

from models.item import ItemModel
from libs.strings import gettext
from models.order import OrderModel

class Order(Resource):
    @classmethod
    def post(cls):
        """Gets a token and items id -> transform it into Stripe order"""
        data = request.get_json() # Token + list of items
        items = []

        # Iterate over items and retrieve them from the database
        for _id in data["item_ids"]:
            item = ItemModel.find_by_id(_id)
            if not item:
                return {"message": gettext("order_item_by_id_not_found").format(_id)}, 404

            items.append(item)

        order = OrderModel(items=items, status="pending")
        order.save_to_db()
