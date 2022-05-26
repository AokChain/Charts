from requests import Session, TooManyRedirects, ConnectionError, Timeout
from service.models import PriceTick
from dateutil import parser
from datetime import datetime
from pony import orm
from .. import utils

@orm.db_session
def sync_price():
    url = "https://api.coingecko.com/api/v3/coins/aok?localization=false&tickers=false&market_data=true"
    session = Session()

    try:
        req = session.get(url).json()
        market_data = req["market_data"]

        last_updated = market_data["last_updated"].replace("Z", "")

        last_updated = datetime.fromisoformat(last_updated)

        if not (pricetick := PriceTick.get_for_update(timestamp=utils.round_day(last_updated))):
            pricetick = PriceTick(timestamp=utils.round_day(last_updated))

        pricetick.latest_price = market_data["current_price"]["usd"]
        pricetick.min_price = market_data["low_24h"]["usd"]
        pricetick.max_price = market_data["high_24h"]["usd"]
        pricetick.volume = market_data["total_volume"]["usd"]
        pricetick.market_cap = market_data["fully_diluted_valuation"]["usd"]
        
    except (TooManyRedirects, ConnectionError, Timeout) as e:
        print(e)
        pass
