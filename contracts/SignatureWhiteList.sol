// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "@openzeppelin/contracts/utils/cryptography/draft-EIP712.sol";
import "@openzeppelin/contracts/access/Ownable.sol";

abstract contract SignatureWhiteList is EIP712, Ownable {

    bytes32 public constant TYPE_HASH =
        keccak256("WhiteListAddress(address whitelisted)");

    address whitelistSigningKey = address(0);
    
    constructor(string memory name, string memory version, address whitelistSigningKey_)
	EIP712(name, version){
	whitelistSigningKey = whitelistSigningKey_;
    }

    function setWhitelistSigningAddress(address newSigningKey) public onlyOwner {
        whitelistSigningKey = newSigningKey;
    }

    modifier whitelisted(bytes calldata signature)
    {
	bytes32 digest = _hashTypedDataV4(keccak256(abi.encode(TYPE_HASH, _msgSender())));
	require(whitelistSigningKey == ECDSA.recover(digest, signature),
		"no matching signing key");
	_;
    }
    
}
