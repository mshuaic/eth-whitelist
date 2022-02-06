from array import array
from random import Random
import math
# import hashlib
from sha3 import keccak_256
from web3 import Web3
from eth_abi import encode_single, encode_abi
from eth_abi.packed import encode_single_packed, encode_abi_packed
from struct import unpack


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

        num_words = (self.num_bits + 31) // 32
        self.arr = array('L', [0]) * num_words
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
        # for mask in self.probe_func(self, key):
            # self.bitarry |= 1 << mask

    def __contains__(self, key):
        return all(self.arr[i] & mask for i, mask in self.probe_func(self, key))
        # return all(self.bitarry & 1 << mask for mask in self.probe_func(self, key))


def int_to_bytes(x: int) -> bytes:
    return x.to_bytes((x.bit_length() + 7) // 8, 'big')


def int_from_bytes(xbytes: bytes) -> int:
    return int.from_bytes(xbytes, 'big')


def get_probes(bfilter, key, hasher=keccak_256):
    # hasher = Random(key).randrange

    for i in range(bfilter.num_probes):

        # data = Web3.solidityKeccak(["string", "uint8"], [key, i])
        # data = hasher(encode_abi_packed(
            # ['string', "uint8"], [key, i])).digest()
        # yield unpack("p", data) % bfilter.num_bits
        # yield int.from_bytes(data, byteorder="big") % bfilter.num_bits
        # yield hasher(bfilter.num_bits) % bfilter.num_bits
        # n = len(bfilter.arr)
        # a = int.from_bytes(hasher(n.to_bytes(
        #     (n.bit_length() + 7)//8, byteorder="big")).digest(), byteorder="big")
        # array_index = a % len(bfilter.arr)
        # bit_index = int.from_bytes(
        #     hasher(int_to_bytes(32)).digest(), byteorder="big") % 32
        # digest =

        digest = int_from_bytes(hasher(encode_abi_packed(
            ['string', "uint8"], [key, i])).digest())
        array_index = digest % len(bfilter.arr)
        bit_index = digest % 32
        yield array_index, 1 << bit_index


if __name__ == '__main__':

    from random import sample
    from string import ascii_letters

    states = '''Alabama Alaska Arizona Arkansas California Colorado Connecticut
        Delaware Florida Georgia Hawaii Idaho Illinois Indiana Iowa Kansas
        Kentucky Louisiana Maine Maryland Massachusetts Michigan Minnesota
        Mississippi Missouri Montana Nebraska Nevada NewHampshire NewJersey
        NewMexico NewYork NorthCarolina NorthDakota Ohio Oklahoma Oregon
        Pennsylvania RhodeIsland SouthCarolina SouthDakota Tennessee Texas Utah
        Vermont Virginia Washington WestVirginia Wisconsin Wyoming'''.split()

    bf = BloomFilter(1000, 0.01, probe_func=get_probes)
    for state in states:
        bf.add(state)

    m = sum(state in bf for state in states)
    print('%d true positives out of %d trials' % (m, len(states)))

    # print("asd" in bf)

    trials = 100000
    m = sum(''.join(sample(ascii_letters, 5)) in bf for i in range(trials))
    print('%d true negatives and %d false negatives out of %d trials'
          % (trials-m, m, trials))

    # print(Web3.toHex(bf.bitarry))

    print(bf.num_bits, bf.num_probes, len(bf.arr))

    # print(int(hashlib.sha256(b"a").hexdigest(), 16))

    # print(keccak_256(encode_abi_packed(['string'], ['a'])).digest())
    # print(Web3.solidityKeccak(['string'], ['a']))
