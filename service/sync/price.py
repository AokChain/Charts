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

        if not (price_tick := PriceTick.get_for_update(timestamp=timestamp)):
            price_tick = PriceTick(timestamp=timestamp)

        price_tick.cap = market_data["fully_diluted_valuation"]["usd"]
        price_tick.price = market_data["current_price"]["usd"]
        price_tick.volume = market_data["total_volume"]["usd"]

    except requests.exceptions.RequestException:
        print("Request to CoinGecko API failed")
