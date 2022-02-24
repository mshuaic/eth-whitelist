from Blockchain.Contract import Contract
from web3 import Web3
from web3.middleware import geth_poa_middleware
from MerkleTree import MerkleTree
from eth_tester import EthereumTester, PyEVMBackend
from eth_utils import to_wei
from eth_abi.packed import encode_abi_packed


c = Contract(['./contracts/test_mt.sol'], import_remappings={
    "@openzeppelin": "/node_modules/@openzeppelin"})

num_acct = 20

state_overrides = {'balance': to_wei(100, 'ether')}
custom_genesis_state = PyEVMBackend.generate_genesis_state(
    overrides=state_overrides, num_accounts=num_acct+1)
pyevm_backend = PyEVMBackend(genesis_state=custom_genesis_state)
t = EthereumTester(backend=pyevm_backend)

# web3.py instance
w3 = Web3(Web3.EthereumTesterProvider(t))
w3.eth.default_account = w3.eth.accounts[0]

# print(w3.eth.accounts)

n_test_acct = 11
mt = MerkleTree(w3.eth.accounts[:n_test_acct])
print(w3.eth.accounts[:n_test_acct])

Test = w3.eth.contract(abi=c.abi, bytecode=c.bytecode)
tx_hash = Test.constructor(mt.root).transact()
print("0x"+mt.root.hex())


tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
test = w3.eth.contract(
    address=tx_receipt.contractAddress,
    abi=c.abi
)


r = all(test.functions.test(mt.proofs[i]).call(
    {"from": w3.eth.accounts[i]}) for i in range(n_test_acct))
print(r)

try:
    test.functions.test(mt.proofs[0]).call({"from": w3.eth.accounts[18]})
except Exception as e:
    print(e)
