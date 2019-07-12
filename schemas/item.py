from ma import ma
from models.item import ItemModel
from models.store import StoreModel


class ItemSchema(ma.ModelSchema):
    class Meta:
        model = ItemModel
        load_only = ("store",)  # not returnable fields, only to load, store is the same as store id
        dump_only = ("id",)  # returnable only, not to load
        include_fk = True    # include foreign keys

