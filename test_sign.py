from eth_account.messages import encode_defunct, encode_structured_data
from Blockchain.Contract import Contract
from web3 import Web3
from web3.middleware import geth_poa_middleware
from eth_tester import EthereumTester, PyEVMBackend
from eth_utils import to_wei


c = Contract(['./contracts/test_sign.sol'], import_remappings={
    "@openzeppelin": "/node_modules/@openzeppelin"})

num_acct = 20

"""
pyevm hard sets chainid to 131277322940537
https://github.com/ethereum/eth-tester/blob/0d03374f7d2e7344d14277deb6c0414cb4c3cef9/eth_tester/backends/pyevm/main.py#L182
https://github.com/ethereum/web3.py/issues/1677
"""
chainid = 131277322940537
state_overrides = {'balance': to_wei(100, 'ether')}
custom_genesis_state = PyEVMBackend.generate_genesis_state(
    overrides=state_overrides, num_accounts=num_acct+1)
pyevm_backend = PyEVMBackend(genesis_state=custom_genesis_state)


t = EthereumTester(backend=pyevm_backend)

# web3.py instance
w3 = Web3(Web3.EthereumTesterProvider(t))
# w3 = Web3(Web3.IPCProvider('/home/markma/NFT/eth/data/geth.ipc'))
# w3.middleware_onion.inject(geth_poa_middleware, layer=0)
w3.eth.default_account = w3.eth.accounts[0]

Test = w3.eth.contract(abi=c.abi, bytecode=c.bytecode)
tx_hash = Test.constructor(w3.eth.accounts[0]).transact()


tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
test = w3.eth.contract(
    address=tx_receipt.contractAddress,
    abi=c.abi
)

msg = {
    "types": {
        "EIP712Domain": [
            {
                "name": "name",
                "type": "string"
            },
            {
                "name": "version",
                "type": "string"
            },
            {
                "name": "chainId",
                "type": "uint256"
            },
            {
                "name": "verifyingContract",
                "type": "address"
            }
        ],
        "WhiteListAddress": [
            {
                "name": "whitelisted",
                "type": "address"
            }
        ]
    },
    "primaryType": "WhiteListAddress",
    "domain": {
        "name": "Artopus",
        "version": "1",
        "chainId": chainid,  # main net chainid; replace to 1 later
        "verifyingContract": None  # our contract address
    },
    "message": {
        "whitelisted": None  # user's address
    }
}


msg["message"]["whitelisted"] = w3.eth.accounts[1]
msg["domain"]["verifyingContract"] = tx_receipt.contractAddress
message = encode_structured_data(msg)
# use account[0]'s private key to sign account[1]'s message
sk = pyevm_backend.account_keys[0]
s = w3.eth.account.sign_message(message, sk)

try:

    r = test.functions.test(s.signature).call({"from": w3.eth.accounts[1]})
    print(f"accounts[1] is in the whitelist: {r}")
    # print true

    r = test.functions.test(s.signature).call({"from": w3.eth.accounts[2]})
    print(f"accounts[2] is in the whitelist: {r}")
    # throw exception

except Exception as e:
    print(e)
