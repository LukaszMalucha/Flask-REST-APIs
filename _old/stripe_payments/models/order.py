import os

from db import db
from typing import List

items_to_orders = db.Table(
    "items_to_orders",
    db.Column("item_id", db.Integer, db.ForeignKey("items.id")),
    db.Column("order_id", db.Integer, db.ForeignKey("orders.id"))

)

class OrderModel(db.Model):
    __tablename__ = 'orders'

    id = db.Column(db.Integer, primary_key=True)
    status = db.Column(db.String(20), nullable=False)

    items = db.relationship("ItemModel", secondary=items_to_orders, lazy="dynamic")

    @classmethod
    def find_all(cls):
        return cls.query.all()

    @classmethod
    def find_by_id(cls, _id):
        return cls.query.filter_by(id=_id).first()

    def set_status(self, new_status):
        self.status = new_status
        self.save_to_db()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()


