from ma import ma
from models.store import StoreModel
from models.item import ItemModel
from schemas.item import ItemSchema

class StoreSchema(ma.ModelSchema):
    items = ma.Nested(ItemSchema, many=True)
    class Meta:
        model = StoreModel
        dump_only = ("id",)  # returnable only, not to load
        include_fk = True
