from datetime import datetime
from decimal import Decimal
from .base import db
from pony import orm

class TransactionIndex(db.Entity):
    _table_ = "chain_transaction_index"

    currency = orm.Required(str, default="AOK", index=True)
    amount = orm.Required(Decimal, precision=20, scale=8)
    transaction = orm.Required("Transaction")
    created = orm.Required(datetime)