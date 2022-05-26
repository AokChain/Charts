from .base import db
from pony import orm

class Address(db.Entity):
    _table_ = "chain_addresses"

    address = orm.Required(str, index=True)