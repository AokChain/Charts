from datetime import datetime
from decimal import Decimal
from .block import Block
from .base import db
from pony import orm

class Transaction(db.Entity):
    _table_ = "chain_transactions"

    amount = orm.Required(Decimal, precision=20, scale=8)
    coinstake = orm.Required(bool, default=False)
    coinbase = orm.Required(bool, default=False)
    txid = orm.Required(str, index=True)
    created = orm.Required(datetime)
    locktime = orm.Required(int)
    size = orm.Required(int)

    block = orm.Required("Block")

    @property
    def currencies(self):
        currencies = []

        for output in self.outputs:
            if output.currency not in currencies:
                currencies.append(output.currency)

        return currencies

    @property
    def confirmations(self):
        latest_blocks = Block.select().order_by(
            orm.desc(Block.height)
        ).first()
        return latest_blocks.height - self.block.height + 1

    def display(self):
        output_amount = 0
        input_amount = 0
        outputs = []
        inputs = []

        for vin in self.inputs:
            inputs.append({
                "address": vin.vout.address.address,
                "currency": vin.vout.currency,
                "amount": float(vin.vout.amount),
                "id": vin.id,
            })

            if vin.vout.currency == "AOK":
                input_amount += vin.vout.amount

        inputs = sorted(inputs, key=lambda d: d["id"])
        inputs = [{key: val for key, val in sub.items() if key != "id"} for sub in inputs]

        for vout in self.outputs:
            outputs.append({
                "vin": vout.vin.transaction.txid if vout.vin else None,
                "address": vout.address.address,
                "currency": vout.currency,
                "timelock": vout.timelock,
                "amount": float(vout.amount),
                "category": vout.category,
                "spent": vout.spent,
                "index": vout.n
            })

            if vout.currency == "AOK":
                output_amount += vout.amount

        outputs = sorted(outputs, key=lambda d: d["index"])

        return {
            "confirmations": self.confirmations,
            "fee": float(input_amount - output_amount),
            "timestamp": int(self.created.timestamp()),
            "amount": float(self.amount),
            "coinstake": self.coinstake,
            "height": self.block.height,
            "coinbase": self.coinbase,
            "txid": self.txid,
            "size": self.size,
            "outputs": outputs,
            "mempool": False,
            "inputs": inputs
        }
