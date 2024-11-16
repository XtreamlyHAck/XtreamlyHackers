from typing import List
from web3 import Web3


class Web3Contact:
    def __init__(
        self,
        rpc: str,
        address: str,
        abi: any,
    ):
        self.web3 = self.connect(rpc)
        self.contract = self.web3.eth.contract(address=address, abi=abi)

    @staticmethod
    def connect(rpc):
        web3 = Web3(Web3.HTTPProvider(rpc))

        if not web3.is_connected():
            raise Exception(f"Unable to connect to {rpc}.")

        return web3

    def read_contract(self, function: str, arg: str):
        return self.contract.functions[function](arg).call()

    def write_contract(self, function: str, private_key: str, args: List[any]):
        account = self.web3.eth.account.from_key(private_key)
        wallet_address = account.address

        txn = self.contract.functions[function](*args).build_transaction({
            'from': wallet_address,
            'nonce': self.web3.eth.get_transaction_count(wallet_address),
        })

        signed_txn = self.web3.eth.account.sign_transaction(txn, private_key=private_key)
        txn_hash = self.web3.eth.send_raw_transaction(signed_txn.raw_transaction)
        txn_receipt = self.web3.eth.wait_for_transaction_receipt(txn_hash)

        return txn_hash.hex(), txn_receipt
