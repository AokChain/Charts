from ..services import TransactionService
from ..services import AddressService
from ..services import BlockService
from datetime import datetime
from pony import orm
from .. import utils


def log_block(message, block, tx=[]):
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    time = block.created.strftime("%Y-%m-%d %H:%M:%S")
    print(f"{now} {message}: hash={block.blockhash} height={block.height} date='{time}'")

def log_message(message):
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"{now} {message}")


def current_height():
    return utils.make_request("getblockcount")["result"]

def get_height(height: int):
    return utils.make_request("getblockhash", [height])["result"]

def blockhash(height: int):
    return utils.make_request("getblockhash", [height])["result"]


@orm.db_session
def sync_chain():
    if not BlockService.latest_block():
        data = get_height(0)
        created = datetime.fromtimestamp(data["time"])

        block = BlockService.create(
            data["hash"], data["height"], created
        )

        log_block("Genesis block", block)

        orm.commit()

    current_height = current_height()
    latest_block = BlockService.latest_block()


    log_message(f"Current node height: {current_height}, db height: {latest_block.height}")

    while latest_block.blockhash != blockhash(latest_block.height):
        log_block("Found reorg", latest_block)

        reorg_block = latest_block
        latest_block = reorg_block.previous_block

        reorg_block.delete()
        orm.commit()



    for height in range(latest_block.height + 1, current_height + 1):
        block_data = get_height(height)
        created = datetime.fromtimestamp(block_data["time"])

        block = BlockService.create(
            block_data["hash"], block_data["height"], created
        )

        block.previous_block = latest_block

        for index, txid in enumerate(block_data["tx"]):
            # ToDo: Parse address/transactions stats here
            pass

        latest_block = block
        orm.commit()
