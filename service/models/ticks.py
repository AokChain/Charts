from datetime import datetime
from decimal import Decimal
from .base import db
from pony import orm

class TokenTick(db.Entity):
    _table_ = "chart_tokens"

    tokens = orm.Required(int, default=0)
    timestamp = orm.Required(datetime)

class TransactionTick(db.Entity):
    _table_ = "chart_transactions"

    transactions = orm.Required(int, default=0)
    timestamp = orm.Required(datetime)

class AddressTick(db.Entity):
    _table_ = "chart_addresses"

    addresses = orm.Required(int, default=0)
    timestamp = orm.Required(datetime)

class PriceTick(db.Entity):
    _table_ = "chart_prices"

    volume = orm.Optional(Decimal, precision=20, scale=8)
    price = orm.Optional(Decimal, precision=20, scale=8)
    cap = orm.Optional(Decimal, precision=20, scale=8)
    timestamp = orm.Required(datetime)

    @property
    def display(self):
        return {
            "timestamp": int(self.timestamp.timestamp()),
            "volume": self.volume,
            "price": self.price,
            "cap": self.cap
        }
