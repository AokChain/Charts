from ..services import TransactionService
from ..services import AddressService
from ..services import BlockService
from ..methods import Transaction
from datetime import datetime
from ..methods import General
from ..methods import Block
from pony import orm
from .. import utils

def log_block(message, block, tx=[]):
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    time = block.created.strftime("%Y-%m-%d %H:%M:%S")
    print(f"{now} {message}: hash={block.blockhash} height={block.height} tx={len(tx)} date='{time}'")

def log_message(message):
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"{now} {message}")

@orm.db_session
def sync_chart_data():

    if not BlockService.latest_block():
        data = Block.height(0)["result"]
        created = datetime.fromtimestamp(data["time"])
        signature = data["signature"] if "signature" in data else None

        block = BlockService.create(
            utils.amount(data["reward"]), data["hash"], data["height"], created,
            data["difficulty"], data["merkleroot"], data["chainwork"],
            data["version"], data["weight"], data["stake"], data["nonce"],
            data["size"], data["bits"], signature
        )

        log_block("Genesis block", block)

        orm.commit()

    current_height = General.current_height()
    latest_block = BlockService.latest_block()

    for height in range(latest_block.height + 1, current_height + 1):
        block_data = Block.height(height)["result"]
        created = datetime.fromtimestamp(block_data["time"])
        signature = block_data["signature"] if "signature" in block_data else None

        block = BlockService.create(
            utils.amount(block_data["reward"]), block_data["hash"], block_data["height"], created,
            block_data["difficulty"], block_data["merkleroot"], block_data["chainwork"],
            block_data["version"], block_data["weight"], block_data["stake"], block_data["nonce"],
            block_data["size"], block_data["bits"], signature
        )

        block.previous_block = latest_block

        for index, txid in enumerate(block_data["tx"]):

            tx_data = Transaction.info(txid, False)["result"]
            created = datetime.fromtimestamp(tx_data["time"])

            transaction = TransactionService.create(
                utils.amount(tx_data["amount"]), tx_data["txid"],
                created, tx_data["locktime"], tx_data["size"], block
            )

            for vout in tx_data["vout"]:
                if vout["scriptPubKey"]["type"] in ["nonstandard", "nulldata"]:
                    continue

                script = vout["scriptPubKey"]["addresses"][0]
                address = AddressService.get_by_address(script)

                if not address:
                    AddressService.create(script)

        latest_block = block
        orm.commit()