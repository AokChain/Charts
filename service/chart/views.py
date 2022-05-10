from webargs.flaskparser import use_args
from ..models import PriceTick
from flask import Blueprint
from .args import page_args
from pony import orm
import math

blueprint = Blueprint("chart", __name__, url_prefix="/chart")

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
