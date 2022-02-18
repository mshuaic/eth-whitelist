// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "./MerkleTreeWhiteList.sol";

contract test_mt is MerkleTreeWhiteList{

    constructor(bytes32 roothash)
	MerkleTreeWhiteList(roothash)
	{}
    

    function test(bytes32[] memory proof)
	whitelisted(proof)
	public view returns(bool)
        {
            return true;
        }

}
