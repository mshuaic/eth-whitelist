// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "./SignatureWhiteList.sol";
// import "@openzeppelin/contracts/utils/cryptography/ECDSA.sol";
// import "@openzeppelin/contracts/utils/cryptography/draft-EIP712.sol";

contract test_sign is SignatureWhiteList {

    constructor(address signingPK)
	SignatureWhiteList("Artopus", "1", signingPK)
	{}

    function test(bytes calldata signature)
	whitelisted(signature)
	public view returns(bool)
        {
            return true;
        }    
}
