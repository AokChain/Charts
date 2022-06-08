from ..models import TransactionTick
from ..services import BlockService
from ..models import AddressTick
from ..models import TokenTick
from datetime import datetime
from ..models import Stats
from pony import orm
from .. import utils
import json

def log_block(message, block, tx=[]):
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    time = block.created.strftime("%Y-%m-%d %H:%M:%S")
    print(f"{now} {message}: hash={block.blockhash} height={block.height} tx={block.transactions} addr={block.addresses} tkn={block.tokens} date='{time}'")

def log_message(message):
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"{now} {message}")

def get_current_height():
    return utils.make_request("getblockcount")["result"]

def get_height(height: int):
    return utils.make_request("getblockhash", [height])["result"]

def get_block_hash(height: int):
    return utils.make_request("getblockhash", [height])["result"]

def get_block(blockhash: str):
    return utils.make_request("getblock", [blockhash])["result"]

def get_transaction(txid: str):
    data = utils.make_request("getrawtransaction", [txid, True])

    for index, vin in enumerate(data["result"]["vin"]):
        if "txid" in vin:
            vin_data = utils.make_request("getrawtransaction", [vin["txid"], True])
            if vin_data["error"] is None:
                data["result"]["vin"][index]["scriptPubKey"] = vin_data["result"]["vout"][vin["vout"]]["scriptPubKey"]

    return data["result"]

@orm.db_session
def sync_chain():
    if not BlockService.latest_block():
        data = get_block(get_height(0))

        created = datetime.fromtimestamp(data["time"])

        block = BlockService.create(
            data["hash"], data["height"], created
        )

        log_block("Genesis block", block)

        orm.commit()

    current_height = get_current_height()
    latest_block = BlockService.latest_block()

    log_message(f"Current node height: {current_height}, db height: {latest_block.height}")

    # Get stats object
    if not(stats := Stats.select().for_update().first()):
        stats = Stats()

    while latest_block.blockhash != get_block_hash(latest_block.height):
        log_block("Found reorg", latest_block)

        reorg_block = latest_block
        latest_block = reorg_block.previous_block

        stats.transactions -= reorg_block.transactions
        stats.addresses -= reorg_block.addresses
        stats.tokens -= reorg_block.tokens

        if (transactions_tick := TransactionTick.get_for_update(timestamp=timestamp)):
            transactions_tick.transactions -= reorg_block.transactions

        if (addresses_tick := AddressTick.get_for_update(timestamp=timestamp)):
            addresses_tick.addresses -= reorg_block.addresses

        if (tokens_tick := TokenTick.get_for_update(timestamp=timestamp)):
            tokens_tick.tokens -= reorg_block.tokens

        reorg_block.delete()
        orm.commit()

    for height in range(latest_block.height + 1, current_height + 1):
        block_data = get_block(get_height(height))
        created = datetime.fromtimestamp(block_data["time"])

        block = BlockService.create(
            block_data["hash"], block_data["height"], created
        )

        block.previous_block = latest_block

        transactions = 0
        addresses = 0
        tokens = 0

        for txid in block_data["tx"]:
            transactions += 1

            tx = get_transaction(txid)

            for vin in tx["vin"]:
                if "scriptPubKey" in vin:
                    addresses += len(vin["scriptPubKey"]["addresses"])

            for vout in tx["vout"]:
                if "scriptPubKey" in vout and vout["scriptPubKey"]["type"] == "new_token":
                    if "!" not in vout["scriptPubKey"]["token"]["name"]:
                        tokens += 1

        block.transactions += transactions
        block.addresses += addresses
        block.tokens += tokens

        stats.transactions += transactions
        stats.addresses += addresses
        stats.tokens += tokens

        timestamp = utils.round_day(block.created)

        if not (transactions_tick := TransactionTick.get_for_update(timestamp=timestamp)):
            transactions_tick = TransactionTick(timestamp=timestamp)

        transactions_tick.transactions += transactions

        if not (addresses_tick := AddressTick.get_for_update(timestamp=timestamp)):
            addresses_tick = AddressTick(timestamp=timestamp)

        addresses_tick.addresses += addresses

        if not (tokens_tick := TokenTick.get_for_update(timestamp=timestamp)):
            tokens_tick = TokenTick(timestamp=timestamp)

        tokens_tick.tokens += tokens

        latest_block = block

        log_block("New block", block, block_data["tx"])

        orm.commit()
