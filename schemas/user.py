from marshmallow import Schema, fields


class UserSchema(Schema):
    class Meta:
        load_only = ("password",)  # not returnable fields, only to load
        dump_only = ("id",)  # returnable only, not to load

    id = fields.Int()  # not need to require as it'll be populated automatically by sqlalchemy
    username = fields.Str(required=True)
    password = fields.Str(required=True)
