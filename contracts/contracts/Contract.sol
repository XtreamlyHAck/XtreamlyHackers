// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20 <0.8.24;

import "./ILendingPool.sol";
// import "@aave/protocol-v2/contracts/interfaces/ILendingPool.sol";
import "./ILendingPoolAddressesProvider.sol";

import "https://github.com/OpenZeppelin/openzeppelin-contracts/blob/master/contracts/token/ERC20/IERC20.sol";
// import "@openzeppelin/contracts/token/ERC20/ERC20.sol";

import "./IUniswapV2Router02.sol";

contract FlashLoanExample {
    ILendingPoolAddressesProvider public provider;
    IUniswapV2Router02 public uniswapRouter;
    address public usdtAddress;
    address public wethAddress;

    constructor(
        address _provider,
        address _uniswapRouter,
        address _usdtAddress,
        address _wethAddress
    ) {
        provider = ILendingPoolAddressesProvider(_provider);
        uniswapRouter = IUniswapV2Router02(_uniswapRouter);
        usdtAddress = _usdtAddress;
        wethAddress = _wethAddress;
    }

    function executeFlashLoan(uint256 amount) external {
        ILendingPool lendingPool = ILendingPool(provider.getLendingPool());
        
        address receiverAddress = address(this);
        address asset = usdtAddress;
        uint256 amountToLoan = amount;
        bytes memory params = "";
        uint16 referralCode = 0;

        lendingPool.flashLoan(
            receiverAddress,
            asset,
            amountToLoan,
            params,
            referralCode
        );
    }

    function executeOperation(
        address asset,
        uint256 amount,
        uint256 premium,
        address initiator,
        bytes calldata params
    ) external returns (bool) {
        require(msg.sender == provider.getLendingPool(), "Invalid sender");
        require(asset == usdtAddress, "Invalid flash loan asset");

        uint256 amountToSwap = amount;
        IERC20(usdtAddress).approve(address(uniswapRouter), amountToSwap);

        address[] memory path;
        path[0] = usdtAddress;
        path[1] = wethAddress;

        uint256[] memory amounts = uniswapRouter.swapExactTokensForTokens(
            amountToSwap,
            1,
            path,
            address(this),
            block.timestamp
        );

        uint256 ethAmount = amounts[1];

        uint256 repaymentAmount = amount + premium;
        uint256 fee = (amount * 3) / 100;
        uint256 totalRepayment = repaymentAmount + fee;

        require(
            IERC20(usdtAddress).balanceOf(address(this)) >= totalRepayment,
            "Insufficient USDT to repay loan"
        );

        IERC20(usdtAddress).approve(msg.sender, totalRepayment);

        return true;
    }

    function withdraw(address token, uint256 amount) external {
        IERC20(token).transfer(msg.sender, amount);
    }

    receive() external payable {}
}