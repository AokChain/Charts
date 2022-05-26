from ..models import TransactionTick
from ..models import Transaction
from datetime import datetime
from pony import orm
from .. import utils

@orm.db_session
def sync_transaction():
    if not (txtick := TransactionTick.get_for_update(timestamp=utils.round_day(datetime.utcnow()))):
        txtick = TransactionTick(timestamp=utils.round_day(datetime.utcnow()))

    txtick.count = Transaction.select().count(distinct=False)
