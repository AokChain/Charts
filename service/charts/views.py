# from ..models import TransactionTick, AddressTick
from webargs.flaskparser import use_args
from ..models import PriceTick
from flask import Blueprint
from .args import page_args
from pony import orm
import math

blueprint = Blueprint("chart", __name__)

@blueprint.route("/price", methods=["GET"])
@use_args(page_args, location="query")
@orm.db_session
def price(args):
    result = {"error": None, "data": {}}
    size = 20

    priceticks = PriceTick.select().order_by(
        lambda p: orm.desc(p.timestamp)
    )

    total = priceticks.count(distinct=False)
    pages = math.ceil(total / size)
    current = args["page"]

    result["data"]["pagination"] = {
        "current": current,
        "total": total,
        "pages": pages
    }

    priceticks = priceticks.page(current, size)
    result["data"]["list"] = []

    for pricetick in priceticks:
        result["data"]["list"].append(pricetick.display)

    return result

# @blueprint.route("/transactions", methods=["GET"])
# @use_args(page_args, location="query")
# @orm.db_session
# def transactions(args):
#     result = {"error": None, "data": {}}
#     size = 20

#     txticks = TransactionTick.select().order_by(
#         lambda t: orm.desc(t.timestamp)
#     )

#     total = txticks.count(distinct=False)
#     pages = math.ceil(total / size)
#     current = args["page"]

#     result["data"]["pagination"] = {
#         "current": current,
#         "total": total,
#         "pages": pages
#     }

#     txticks = txticks.page(current, size)
#     result["data"]["list"] = []

#     for txtick in txticks:
#         result["data"]["list"].append(txtick.display)

#     return result

# @blueprint.route("/addresses", methods=["GET"])
# @use_args(page_args, location="query")
# @orm.db_session
# def addresses(args):
#     result = {"error": None, "data": {}}
#     size = 20

#     addrticks = AddressTick.select().order_by(
#         lambda a: orm.desc(a.timestamp)
#     )

#     total = addrticks.count(distinct=False)
#     pages = math.ceil(total / size)
#     current = args["page"]

#     result["data"]["pagination"] = {
#         "current": current,
#         "total": total,
#         "pages": pages
#     }

#     addrticks = addrticks.page(current, size)
#     result["data"]["list"] = []

#     for addrtick in addrticks:
#         result["data"]["list"].append(addrtick.display)

#     return result
