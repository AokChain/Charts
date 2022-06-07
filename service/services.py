from .models import Transaction
from .models import Address
from .models import Block
from .models import User
from pony import orm

class UserService(object):
    @classmethod
    def get_by_username(cls, username):
        return User.get(username=username)

    @classmethod
    def get_by_email(cls, email):
        return User.get(email=email)

    @classmethod
    def create(cls, username, email, password):
        return User(
            username=username, password=password,
            email=email
        )

class BlockService(object):
    @classmethod
    def latest_block(cls):
        return Block.select().order_by(
            orm.desc(Block.height)
        ).first()

    @classmethod
    def create(cls, blockhash, height, created):
        return Block(**{
            "blockhash": blockhash,
            "created": created,
            "height": height
       })

    @classmethod
    def get_by_height(cls, height):
        return Block.get(height=height)

    @classmethod
    def get_by_hash(cls, bhash):
        return Block.get(blockhash=bhash)

    @classmethod
    def blocks(cls):
        return Block.select().order_by(
            orm.desc(Block.height)
        )

    @classmethod
    def chart(cls):
        query = orm.select((b.height, len(b.transactions)) for b in Block)
        query = query.order_by(-1)
        return query[:1440]

class TransactionService(object):
    @classmethod
    def get_by_txid(cls, txid):
        return Transaction.get(txid=txid)

    @classmethod
    def create(cls, amount, txid, created, locktime, size, block,
               coinbase=False, coinstake=False):
        return Transaction(
            amount=amount, txid=txid, created=created,
            locktime=locktime, size=size, coinbase=coinbase,
            coinstake=coinstake, block=block
        )

class AddressService(object):
    @classmethod
    def get_by_address(cls, address):
        return Address.get(address=address)

    @classmethod
    def create(cls, address):
        return Address(address=address)