from datetime import datetime
from pony import orm
from .base import db

class TokenTick(db.Entity):
    _table_ = "chart_token_ticks"

    timestamp = orm.Required(datetime, default=datetime.utcnow)
    count = orm.Optional(int)

    @property
    def display(self):
        return {
            "count": self.count
        }
