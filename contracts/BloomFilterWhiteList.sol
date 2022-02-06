// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "@openzeppelin/contracts/utils/Context.sol";


abstract contract BloomFilterWhiteList is Context{

    uint256[] private arr;
    uint256 private num_probes;
    
    constructor(uint256[] memory _arr, uint256 _num_probes){
	arr = _arr;
	num_probes = _num_probes;
    }

    modifier whitelisted()
    {
	require(contains(_msgSender()), "no access");
	_;
    }
    
    function contains(address key)
	internal
	virtual
	returns(bool)
    {
	uint256 arr_index;
	uint256 mask;
	uint256 bitSize=arr.length * 256;
	for(uint i=0; i<num_probes;i++){
	    (arr_index, mask) = prob_func(arr.length, i, bitSize, key);
	    if(arr[arr_index] & mask == 0){
		return false;
	    }						
	}
	return true;
    }

    
    function prob_func(uint256 arrSize,
		       uint256 i_probes,
		       uint256 bitSize,
		       address key)
	pure
	internal
	virtual
	returns(uint256, uint256){
	uint256 digest = uint256(keccak256(abi.encodePacked(key, i_probes)));
	uint256 index = digest % bitSize;
        uint256 array_index = index / 256;
        uint256 bit_index = index - array_index * 256;
        return (array_index, 1 << bit_index);	
    }
	
}
