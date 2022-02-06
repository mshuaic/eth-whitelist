// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "./BloomFilterWhiteList.sol";

contract test is BloomFilterWhiteList {
    
    constructor(uint256[] memory arr,
		uint256 num_probes)
	BloomFilterWhiteList(arr, num_probes)
	{}

    function hello()
	public
	whitelisted()
	returns(string memory){
	return "hello";
    }

}
