from datetime import datetime
from decimal import Decimal
from .base import db
from pony import orm

class Block(db.Entity):
    _table_ = "chain_blocks"

    blockhash = orm.Required(str, index=True)
    height = orm.Required(int, index=True)
    created = orm.Required(datetime)

    previous_block = orm.Optional("Block")
    next_block = orm.Optional("Block")
