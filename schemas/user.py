from ma import ma
from models.user import UserModel


class UserSchema(ma.ModelSchema):
    class Meta:
        model = UserModel
        load_only = ("password",)  # not returnable fields, only to load
        dump_only = ("id",)  # returnable only, not to load

