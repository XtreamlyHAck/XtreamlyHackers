// SPDX-License-Identifier: MIT
pragma solidity <=0.8.24;

interface ILendingPoolAddressesProvider {
    function getLendingPool() external view returns (address);
}