from ..models import AddressTick
from ..models import Address
from datetime import datetime
from pony import orm
from .. import utils

@orm.db_session
def sync_address():
    if not (addrtick := AddressTick.get_for_update(timestamp=utils.round_day(datetime.utcnow()))):
        addrtick = AddressTick(timestamp=utils.round_day(datetime.utcnow()))

    addrtick.count = Address.select().count(distinct=False)
