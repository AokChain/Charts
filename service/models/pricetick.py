from datetime import datetime
from decimal import Decimal
from .base import db
from pony import orm
from .. import utils

class PriceTick(db.Entity):
    _table_ = "chart_price_ticks"

    timestamp = orm.Required(datetime, default=datetime.utcnow)
    latest_price = orm.Optional(Decimal, precision=20, scale=8)
    min_price = orm.Optional(Decimal, precision=20, scale=8)
    max_price = orm.Optional(Decimal, precision=20, scale=8)
    volume = orm.Optional(Decimal, precision=20, scale=8)
    market_cap = orm.Optional(Decimal, precision=20, scale=8)

    @property
    def display(self):
        return {
            "day": utils.round_day(self.timestamp),
            "latest_price": self.latest_price,
            "min_price": self.min_price,
            "max_price": self.max_price,
            "volume": self.volume,
            "market_cap": self.market_cap
        }
