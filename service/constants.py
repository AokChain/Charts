PRICE_ENDPOINT = "https://api.coingecko.com/api/v3/coins/aok?localization=false&tickers=false&market_data=true"
MARKET_ENDPOINT = "https://api.coingecko.com/api/v3/coins/aok/market_chart?vs_currency=usd&days=max"
SUPPLY_ENDPOINT = "https://api.coingecko.com/api/v3/coins/aok?localization=false"

class Interval:
    DAY = 1
    WEEK = 2
    MONTH = 3
    YEAR = 4

INTERVALS = {
    "1D": Interval.DAY,
    "1W": Interval.WEEK,
    "1M": Interval.MONTH,
    "1Y": Interval.YEAR
}

INTERVALS_LIMIT = {
    "1D": 30,  # ~1 Month
    "1W": 48,  # ~1 Year
    "1M": 48,  # 4 Years
    "1Y": 12  # 12 Years
}
