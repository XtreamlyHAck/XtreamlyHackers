// SPDX-License-Identifier: MIT
pragma solidity <=0.8.24;

interface ILendingPool {
    function flashLoan(
        address receiverAddress,
        address asset,
        uint256 amount,
        bytes calldata params,
        uint16 referralCode
    ) external;
}