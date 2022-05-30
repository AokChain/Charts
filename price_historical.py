from requests import Session, TooManyRedirects, ConnectionError, Timeout
from service.models import PriceTick
from datetime import datetime
from service import utils
from pony import orm

with orm.db_session:
    url = "https://api.coingecko.com/api/v3/coins/aok/market_chart?vs_currency=usd&days=11430"
    session = Session()

    url2 = "https://api.coingecko.com/api/v3/coins/aok?localization=false"
    session2 = Session()
    supply = session2.get(url2).json()["market_data"]["max_supply"]

    try:
        req = session.get(url).json()

        for i in range(0, len(req["prices"]) - 1):
            arr_price = req["prices"][i]
            market_cap = supply * arr_price[1]
            arr_vol = req["total_volumes"][i]
            timestamp = utils.round_day(datetime.fromtimestamp(arr_price[0]/1000))

            if not PriceTick.get(timestamp=timestamp):
                PriceTick(timestamp=timestamp, latest_price=arr_price[1], volume=arr_vol[1], market_cap=market_cap)

        print("Prices recorded")

    except (TooManyRedirects, ConnectionError, Timeout) as e:
        print(e)
        pass
