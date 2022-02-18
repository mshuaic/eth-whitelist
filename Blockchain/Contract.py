from web3 import Web3
from solcx import compile_files


class Contract():
    def __init__(self, contract_files, *,
                 base_path='.',
                 import_remappings=None):
        compiled_sol = compile_files(
            contract_files,
            output_values=["abi", "bin"],
            base_path='.',
            import_remappings=import_remappings)

        contract_id, contract_interface = compiled_sol.popitem()
        self.bytecode = contract_interface['bin']
        # get abi
        self.abi = contract_interface['abi']

        # self.contract = w3.eth.contract(abi=abi, bytecode=bytecode)


# c = Contract(['./contracts/GameItem.sol'], {
#     "@openzeppelin": "/node_modules/@openzeppelin"})


# # web3.py instance
# w3 = Web3(Web3.EthereumTesterProvider())
# # set pre-funded account as sender
# w3.eth.default_account = w3.eth.accounts[0]


# Hello = w3.eth.contract(abi=abi, bytecode=bytecode)
# tx_hash = Hello.constructor().transact()
# tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)

# hello = w3.eth.contract(
#     address=tx_receipt.contractAddress,
#     abi=abi
# )

# print(hello.functions.get().call())


# Hello = w3.eth.contract(abi=abi, bytecode=bytecode)
# tx_hash = Hello.constructor().transact()
# tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
