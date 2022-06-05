from pony import orm
from .base import db

class Token(db.Entity):
    _table_ = "chain_tokens"

    name = orm.Required(str, index=True)
