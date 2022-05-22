from datetime import timedelta, datetime
import requests
import hashlib
import bcrypt
import config
import json
import math

def hashpwd(password: str) -> str:
    return bcrypt.hashpw(str.encode(password), bcrypt.gensalt()).decode()

def checkpwd(password, bcrypt_hash) -> bool:
    return bcrypt.checkpw(str.encode(password), str.encode(bcrypt_hash))

def blake2b(data: str, size=32, key=""):
    """Hash wrapper for blake2b"""
    return hashlib.blake2b(
        str.encode(data),
        key=str.encode(key),
        digest_size=size
    ).digest()

def round_day(created):
    return created - timedelta(
        days=created.day % 1,
        hours=created.hour,
        minutes=created.minute,
        seconds=created.second,
        microseconds=created.microsecond
    )

def dead_response(message="Invalid Request", rid=config.rid):
    return {"error": {"code": 404, "message": message}, "id": rid}

def response(result, error=None, rid=config.rid, pagination=None):
    result = {"error": error, "id": rid, "result": result}

    if pagination:
        result["pagination"] = pagination

    return result

def make_request(method, params=[]):
    headers = {"content-type": "text/plain;"}
    data = json.dumps({"id": config.rid, "method": method, "params": params})

    try:
        return requests.post(config.endpoint, headers=headers, data=data).json()
    except Exception:
        return dead_response()

def reward(height):
    halvings = height // 525960

    if halvings >= 10:
        return 0

    return int(satoshis(4) // (2 ** halvings))

def supply(height):
    premine = satoshis(2100000000)
    reward = satoshis(4)
    halvings = 525960
    halvings_count = 0
    supply = premine + reward

    while height > halvings:
        total = halvings * reward
        reward = reward / 2
        height = height - halvings
        halvings_count += 1

        supply += total

        if halvings > 10:
            reward = 0
            break

    supply = supply + height * reward

    return {
        "halvings": int(halvings_count),
        "supply": int(supply)
    }

def satoshis(value):
    return int(float(value) * math.pow(10, 8))

def amount(value, decimals=8):
    return round(float(value) / math.pow(10, decimals), decimals)