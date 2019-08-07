import os
import env
import stripe
from db import db
from typing import List

CURRENCY = "usd"


class ItemsInOrder(db.Model):
    __tablename__ = "items_in_order"

    id = db.Column(db.Integer, primary_key=True)
    item_id = db.Column(db.Integer, db.ForeignKey("items.id"))
    order_id = db.Column(db.Integer, db.ForeignKey("orders.id"))
    quantity = db.Column(db.Integer)

    item = db.relationship("ItemModel")
    order = db.relationship("OrderModel", back_populates="items")  # reflects changes on one to the other


class OrderModel(db.Model):
    __tablename__ = 'orders'

    id = db.Column(db.Integer, primary_key=True)
    status = db.Column(db.String(20), nullable=False)

    items = db.relationship("ItemsInOrder", back_populates="order")

    @property       # acts as variable
    def description(self):
        """String representation for Stripe DB"""
        item_counts = [f"{i.quantity}x {i.item.name}" for i in self.items]
        return ",".join(item_counts)

    @property
    def amount(self):
        return int(sum([item_data.item.price * item_data.quantity for item_data in self.items]) * 100)

    @classmethod
    def find_all(cls):
        return cls.query.all()

    @classmethod
    def find_by_id(cls, _id):
        return cls.query.filter_by(id=_id).first()

    def charge_with_stripe(self, token):
        stripe.api_key = os.environ.get("STRIPE_API_KEY")
        return stripe.Charge.create(
            amount=self.ammount,
            currency=CURRENCY,
            description=self.description,
            source=token
        )

    def set_status(self, new_status):
        self.status = new_status
        self.save_to_db()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
