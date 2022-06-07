from service.models import PriceTick
from datetime import datetime
from service import constants
from service import utils
from pony import orm
import requests

with orm.db_session:
    try:
        supply = requests.get(constants.SUPPLY_ENDPOINT).json()
        marker = requests.get(constants.MARKET_ENDPOINT).json()

        for i in range(0, len(marker["prices"]) - 1):
            price = marker["prices"][i]
            timestamp = utils.round_day(datetime.fromtimestamp(price[0] / 1000))
            cap = supply["market_data"]["max_supply"] * price[1]
            volume = marker["total_volumes"][i]

            if PriceTick.get(timestamp=timestamp):
                continue

            PriceTick(**{
                "timestamp": timestamp,
                "volume": volume[1],
                "price": price[1],
                "cap": cap,
            })

        print("Prices recorded")

    except requests.exceptions.RequestException:
        print("Request to CoinGecko API failed")
