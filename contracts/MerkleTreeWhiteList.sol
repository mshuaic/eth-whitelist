// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "@openzeppelin/contracts/utils/Context.sol";
import "@openzeppelin/contracts/utils/cryptography/MerkleProof.sol";


abstract contract MerkleTreeWhiteList is Context{

    bytes32 public root;
    
    constructor(bytes32 _root){
	root = _root;
    }

    modifier whitelisted(bytes32[] memory proof)
    {
	bytes32 leaf = keccak256(abi.encodePacked(_msgSender()));
	require(MerkleProof.verify(proof, root, leaf), "no access");
	_;
    }    	
}
