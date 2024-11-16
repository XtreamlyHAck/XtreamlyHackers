// SPDX-License-Identifier: MIT
pragma solidity 0.8.20;

import "./generated/interfaces/verification/IJsonApiVerification.sol";
import "./generated/implementation/verification/JsonApiVerification.sol";

struct Volatility {
    uint256 volatility;
}

contract VolatilityApi {
    Volatility[] public volatilities;
    IJsonApiVerification public jsonApiAttestationVerification;

    constructor() {
        jsonApiAttestationVerification = new JsonApiVerification();
    }

    function addVolatility(IJsonApi.Response calldata jsonResponse) public {
        // We mock the proof for testing and hackathon
        IJsonApi.Proof memory proof = IJsonApi.Proof({
            merkleProof: new bytes32[](0),
            data: jsonResponse
        });
        require(
            jsonApiAttestationVerification.verifyJsonApi(proof),
            "Invalid proof"
        );

        Volatility memory _volatility = abi.decode(
            jsonResponse.responseBody.abi_encoded_data,
            (Volatility)
        );

        volatilities.push(_volatility);
    }
}
