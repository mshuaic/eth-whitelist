from web3 import Web3
from web3.middleware import geth_poa_middleware
import math
from sha3 import keccak_256
from eth_abi.packed import encode_abi_packed
from eth_tester import EthereumTester, PyEVMBackend
from eth_utils import to_wei
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


# c = Contract(['./contracts/BloomFilterWhiteList.sol'], import_remappings={
# "@openzeppelin": "/node_modules/@openzeppelin"})
c = Contract(['./contracts/test_bf.sol'], import_remappings={
    "@openzeppelin": "/node_modules/@openzeppelin"})


num_acct = 100

state_overrides = {'balance': to_wei(100, 'ether')}
custom_genesis_state = PyEVMBackend.generate_genesis_state(
    overrides=state_overrides, num_accounts=num_acct+1)
pyevm_backend = PyEVMBackend(genesis_state=custom_genesis_state)
t = EthereumTester(backend=pyevm_backend)

# web3.py instance
w3 = Web3(Web3.EthereumTesterProvider(t))
w3.eth.default_account = w3.eth.accounts[0]


MAX_UINT_BITSIZE = 256


class BloomFilter:
    # http://en.wikipedia.org/wiki/Bloom_filter

    def __init__(self, max_elements, error_rate, probe_func):

        # self.num_bits = num_bits
        self.error_rate_p = error_rate
        # With fewer elements, we should do very well. With more elements, our
        # error rate "guarantee" drops rapidly.
        self.ideal_num_elements_n = max_elements

        numerator = (
            -1
            * self.ideal_num_elements_n
            * math.log(self.error_rate_p)
        )
        denominator = math.log(2) ** 2
        real_num_bits_m = numerator / denominator
        self.num_bits = int(math.ceil(real_num_bits_m))

        # number of unsigned long long
        num_ull = (self.num_bits + MAX_UINT_BITSIZE) // MAX_UINT_BITSIZE
        self.arr = [0] * num_ull
        self.bitarry = 1 << self.num_bits

        real_num_probes_k = (
            (self.num_bits / self.ideal_num_elements_n)
            * math.log(2)
        )
        self.num_probes = int(math.ceil(real_num_probes_k))

        self.probe_func = get_probes

    def add(self, key):
        for i, mask in self.probe_func(self, key):
            self.arr[i] |= mask

    def __contains__(self, key):
        return all(self.arr[i] & mask for i, mask in self.probe_func(self, key))


def int_to_bytes(x: int) -> bytes:
    return x.to_bytes((x.bit_length() + 7) // 8, 'big')


def int_from_bytes(xbytes: bytes) -> int:
    return int.from_bytes(xbytes, 'big')


def get_probes(bfilter, key, hasher=keccak_256):

    bitSize = MAX_UINT_BITSIZE * len(bfilter.arr)
    for i in range(bfilter.num_probes):
        digest = int_from_bytes(hasher(encode_abi_packed(
            ['address', "uint256"], [key, i])).digest())
        index = digest % bitSize
        array_index = index // MAX_UINT_BITSIZE
        bit_index = index - array_index * MAX_UINT_BITSIZE
        yield array_index, 1 << bit_index


if __name__ == '__main__':

    addresses = [w3.eth.account.create().address for _ in range(num_acct)]

    bf = BloomFilter(len(addresses), 0.01, probe_func=get_probes)
    for addr in addresses:
        bf.add(addr)

    m = sum(addr in bf for addr in addresses)
    print('%d true positives out of %d trials' % (m, len(addresses)))

    trials = 1000
    m = sum(w3.eth.account.create().address in bf for i in range(trials))
    print('%d true negatives and %d false positive out of %d trials'
          % (trials-m, m, trials))

    bf.add(w3.eth.accounts[0])
    print(bf.num_bits, bf.num_probes, len(bf.arr))

    tx_hash = w3.eth.contract(
        abi=c.abi, bytecode=c.bytecode).constructor(bf.arr, bf.num_probes).transact()
    tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
    bfsc = w3.eth.contract(
        address=tx_receipt.contractAddress,
        abi=c.abi
    )

    try:
        r = bfsc.functions.hello().call({"from": w3.eth.accounts[0]})
        print(r)

        r = bfsc.functions.hello().call({"from": w3.eth.accounts[num_acct]})
        print(r)
    except Exception as e:
        print(e)
