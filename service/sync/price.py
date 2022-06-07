from service.models import PriceTick
from datetime import datetime
from .. import constants
from pony import orm
from .. import utils
import requests

@orm.db_session
def sync_price():
    try:
        result = requests.get(constants.PRICE_ENDPOINT).json()
        market_data = result["market_data"]

        timestamp = utils.round_day(datetime.strptime(
            market_data["last_updated"],
            "%Y-%m-%dT%H:%M:%S.%fZ"
        ))

        if not (pricetick := PriceTick.get_for_update(timestamp=timestamp)):
            pricetick = PriceTick(timestamp=timestamp)

        pricetick.cap = market_data["fully_diluted_valuation"]["usd"]
        pricetick.price = market_data["current_price"]["usd"]
        pricetick.volume = market_data["total_volume"]["usd"]

    except requests.exceptions.RequestException:
        print("Request to CoinGecko API failed")
