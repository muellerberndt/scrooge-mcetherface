from web3 import Web3
from web3.utils.empty import empty


class W3(Web3):
    """Helper class that extends Web3 with convenience methods"""

    def __init__(
        self,
        providers=empty,
        middlewares=None,
        modules=None,
        ens=empty,
        gas_price=1000000000,
    ):
        super().__init__(
            providers=providers, middlewares=middlewares, modules=modules, ens=ens
        )
        self.gas_price = gas_price

    def request_blocking(
        self, sender: str, receiver: str, value: int, data: str
    ) -> str:
        """Sends a transaction and returns once the transaction has been mined.

           :param sender: Ethereum address of the sender
           :param receiver: Ethereum address of the receiver
           :param value: Call value
           :param data: Call data
           :returns: Transaction receipt string

           """
        tx_hash = self.eth.sendTransaction(
            {
                "to": receiver,
                "from": sender,
                "data": data,
                "value": value,
                "gas": 5000000,
                "gasPrice": self.gas_price,
            }
        )
        print(
            "Transaction sent successfully, tx-hash: %s. Waiting for transaction to be mined..."
            % tx_hash.hex()
        )
        tx_hash = self.eth.waitForTransactionReceipt(tx_hash, timeout=120)

        return tx_hash

    def balance(self, address: str) -> int:
        """Retrieve the Ether balance for an account.

           :param address: Ethereum address
           :returns: Accunt balance

           """
        return self.fromWei(self.eth.getBalance(address), "ether")
