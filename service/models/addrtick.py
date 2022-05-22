from datetime import datetime
from .base import db
from pony import orm

class AddressTick(db.Entity):
    _table_ = "chart_address_ticks"

    timestamp = orm.Required(datetime, default=datetime.utcnow)
    count = orm.Optional(int)

    @property
    def display(self):
        return {
            "count": self.count
        }
