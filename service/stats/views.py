from ..models import TransactionTick
from ..models import AddressTick
from ..models import TokenTick
from flask import Blueprint
from pony import orm

blueprint = Blueprint("stats", __name__, url_prefix="/stats")

@blueprint.route("/address", methods=["GET"])
@orm.db_session
def address():
    result = {"error": None, "data": {}}

    addr_ticks = AddressTick.select().order_by(
        lambda a: a.timestamp
    )

    current = addr_ticks.first().count
    previous = current

    if len(list(addr_ticks)) > 1:
        addr_ticks = list(addr_ticks)
        previous = addr_ticks[1].count

    result["data"] = {
        "count": current,
        "change": current - previous
    }

    return result

@blueprint.route("/transactions", methods=["GET"])
@orm.db_session
def transaction():
    result = {"error": None, "data": {}}

    tx_ticks = TransactionTick.select().order_by(
        lambda t: t.timestamp
    )

    current = tx_ticks.first().count
    previous = current

    if len(list(tx_ticks)) > 1:
        tx_ticks = list(tx_ticks)
        previous = tx_ticks[1].count

    result["data"] = {
        "count": current,
        "change": current - previous
    }

    return result

@blueprint.route("/tokens", methods=["GET"])
@orm.db_session
def token():
    result = {"error": None, "data": {}}

    token_ticks = TokenTick.select().order_by(
        lambda t: t.timestamp
    )

    current = token_ticks.first().count
    previous = current

    if len(list(token_ticks)) > 1:
        token_ticks = list(token_ticks)
        previous = token_ticks[1].count

    result["data"] = {
        "count": current,
        "change": current - previous
    }

    return result
