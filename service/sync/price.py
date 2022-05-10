from requests import Session, TooManyRedirects, ConnectionError, Timeout
from service.models import PriceTick
from dateutil import parser
from pony import orm

@orm.db_session
def sync_price():
    url = "https://api.coingecko.com/api/v3/coins/aok?localization=false&tickers=false&market_data=true"
    session = Session()

    try:
        req = session.get(url).json()
        market_data = req["market_data"]

        last_updated = parser.parse(market_data["last_updated"])

        if not (PriceTick.get_for_update(timestamp=last_updated)):

            data = {
                "timestamp": last_updated,
                "latest_price": market_data["current_price"]["usd"],
                "min_price": market_data["low_24h"]["usd"],
                "max_price":  market_data["high_24h"]["usd"],
                "volume":  market_data["total_volume"]["usd"],
                "market_cap":  market_data["fully_diluted_valuation"]["usd"]
            }

            PriceTick(**data)
        
    except (TooManyRedirects, ConnectionError, Timeout) as e:
        print(e)
        pass
