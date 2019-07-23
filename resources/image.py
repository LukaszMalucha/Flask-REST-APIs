from flask_restful import Resource
from flask_uploads import UploadNotAllowed
from flask import request
from flask_jwt_extended import jwt_required, get_jwt_identity

from libs import image_helper
from libs.strings import gettext
from schemas.image import ImageSchema

image_schema = ImageSchema()

class ImageUpload(Resource):
    @jwt_required
    def post(self):
        """Verify JWT and upload an image to the folder"""

        data = image_schema.load(request.files)
        user_id = get_jwt_identity()
        folder = f"user_{user_id}"
        try:
            image_path = image_helper.save_image(data["image"])
            basename = image_helper.get_basename(image_path)
            return {"message" : gettext("image_uploaded").format(basename)}, 201
        except UploadNotAllowed:
            extension = image_helper.get_extension(data["image"])
            return {"message": gettext("image_illegal_extension").format(extension)}, 400