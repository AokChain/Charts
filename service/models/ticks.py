from datetime import datetime
from decimal import Decimal
from .base import db
from pony import orm

class PriceTick(db.Entity):
    _table_ = "chart_price_ticks"

    timestamp = orm.Required(datetime, default=datetime.utcnow)
    volume = orm.Optional(Decimal, precision=20, scale=8)
    price = orm.Optional(Decimal, precision=20, scale=8)
    cap = orm.Optional(Decimal, precision=20, scale=8)

    @property
    def display(self):
        return {
            "timestamp": int(self.timestamp.timestamp()),
            "price": self.price,
            "cap": self.cap,
            "volume": self.volume
        }
