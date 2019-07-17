from time import time

from flask import make_response, render_template
from flask_restful import Resource

from models.confirmation import ConfirmationModel
from models.user import UserModel
from resources.user import USER_NOT_FOUND
from schemas.confirmation import ConfirmationSchema


NOT_FOUND = "Confirmation not found"
EXPIRED = "Confirmation link already expired"
ALREADY_CONFIRMED = "User registration already confirmed"

confirmation_schema = ConfirmationSchema()

class Confirmation(Resource):
    @classmethod
    def get(cls, confirmation_id:str):
        """Return confrimation HTML page."""
        confirmation = ConfirmationModel.find_by_id(confirmation_id)
        if not confirmation:
            return {"message": NOT_FOUND}, 404

        if confirmation.expired:
            return {"message": EXPIRED}, 404

        if confirmation.confirmed:
            return {"message": ALREADY_CONFIRMED}, 404

        confirmation.confirmed = True
        confirmation.save_to_db()

        headers = {"Content-Type": "text/html"}
        return make_response(render_template("confirmation_path.html", email=confirmation.user.email), 200, headers)


class CofrimationByUser(Resource):
    @classmethod
    def get(cls, user_id: int):
        """"Return all user confirmations - for testing only"""
        user = UserModel.find_by_id(user_id)
        if not user:
            return {"message": USER_NOT_FOUND}, 404

        return (
            {
                "current_time": int(time()),
                "confirmation": [
                    confirmation_schema.dump(each) for each in user.confirmation.order_by(ConfirmationModel.expire_at)
                ],
            },
            200,
        )



    @classmethod
    def post(cls, user_id: int):
        """Resend confirmation email"""
