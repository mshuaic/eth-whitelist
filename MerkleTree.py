from sha3 import keccak_256
from math import ceil, log
from eth_abi.packed import encode_abi_packed


def encoder(data):
    # return str(data).encode("utf-8")
    return encode_abi_packed(["address"], [data])


class MerkleTree:
    def __init__(self, data, hash_func=lambda x: keccak_256(x).digest(), encoder=encoder):
        n = len(data)
        n_padding = 2 ** ceil(log(n, 2)) - n
        self.leaves = list(map(lambda x: hash_func(
            encoder(x)), data + data[n-n_padding:]))

        self.nodes = [self.leaves]
        self.proofs = [[] for _ in self.leaves]
        while len(self.nodes[-1]) > 1:
            curr = self.nodes[-1]
            self.nodes += [],
            for i in range(0, len(curr), 2):
                left, right = sorted([curr[i], curr[i+1]])
                self.nodes[-1] += hash_func(left+right),

        self.root = self.nodes[-1][0]

        for i in range(len(self.leaves)):
            level = 0
            while len(self.nodes) - level > 1:
                sibling = (-1) ** (i // (2 ** level)) + i // (2 ** level)
                self.proofs[i] += self.nodes[level][sibling],
                level += 1


def test():

    mt = MerkleTree(list(map(str, (range(8)))),
                    hash_func=lambda x: x, encoder=lambda x: str(x))
    print(mt.nodes)
    print(mt.proofs)


if __name__ == '__main__':
    test()
