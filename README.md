# An Ethereum smart contract whitelist implementation using [bloom filter](https://en.wikipedia.org/wiki/Bloom_filter), [merkle tree](https://en.wikipedia.org/wiki/Merkle_tree), or a [EIP-712](https://eips.ethereum.org/EIPS/eip-712)

* smart contract dependencies

      npm install @openzeppelin/contracts
    
    
* python test driver

      test_[mt, bf, sign].py
      
* smart contract test contract

      contracts/test_[mt, bf, sign].sol
      
      
* bare minimum implementation for a whitelist 

      contracts/BloomFilterWhiteList.sol
	  contracts/MerkleTreeWhiteList.sol
	  contracts/SignatureWhiteList.sol
