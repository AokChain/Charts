from ..models import TokenTick
from datetime import datetime
from ..models import Token
from pony import orm
from .. import utils

@orm.db_session
def sync_token():
    if not (tokentick := TokenTick.get_for_update(timestamp=utils.round_day(datetime.utcnow()))):
        tokentick = TokenTick(timestamp=utils.round_day(datetime.utcnow()))

    tokentick.count = Token.select().count(distinct=False)
