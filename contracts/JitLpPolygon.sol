// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

import {IERC20} from "@openzeppelin/contracts/token/ERC20/IERC20.sol";
import {SafeERC20} from "@openzeppelin/contracts/token/ERC20/utils/SafeERC20.sol";
import {IUniswapV3Pool} from "@uniswap/v3-core/contracts/interfaces/IUniswapV3Pool.sol";
import {ISwapRouter} from "@uniswap/v3-periphery/contracts/interfaces/ISwapRouter.sol";
import {IPoolAddressesProvider} from "@aave/core-v3/contracts/interfaces/IPoolAddressesProvider.sol";
import {IPool} from "@aave/core-v3/contracts/interfaces/IPool.sol";
import {IFlashLoanSimpleReceiver} from "@aave/core-v3/contracts/flashloan/interfaces/IFlashLoanSimpleReceiver.sol";
import {BaseRelayRecipient} from "@opengsn/contracts/src/BaseRelayRecipient.sol";

contract JITLPExecutor is IFlashLoanSimpleReceiver {
    using SafeERC20 for IERC20;

    address public owner;
    IPoolAddressesProvider public immutable override ADDRESSES_PROVIDER;
    IPool public immutable override POOL;
    ISwapRouter public immutable swapRouter;
    IUniswapV3Pool public immutable uniswapPool;

    address public token0;
    address public token1;
    address public recipient;

    modifier onlyOwner() {
        require(msg.sender == owner, "Not owner");
        _;
    }

    constructor(
        address _provider,
        address _router,
        address _pool,
        address _token0,
        address _token1
    ) {
        owner = msg.sender;
        ADDRESSES_PROVIDER = IPoolAddressesProvider(_provider);
        POOL = IPool(ADDRESSES_PROVIDER.getPool());
        swapRouter = ISwapRouter(_router);
        uniswapPool = IUniswapV3Pool(_pool);
        token0 = _token0;
        token1 = _token1;
    }

    function requestFlashLoan(address asset, uint256 amount) external onlyOwner {
        POOL.flashLoanSimple(address(this), asset, amount, bytes(""), 0);
    }

    function executeOperation(
        address asset,
        uint256 amount,
        uint256 premium,
        address initiator,
        bytes calldata params
    ) external override returns (bool) {
        require(msg.sender == address(POOL), "Untrusted lender");

        // Step 1: Insert liquidity into pool — simulated in production
        IERC20(asset).safeIncreaseAllowance(address(swapRouter), amount);

        // Step 2: Simulate swap or intercept MEV opportunity here
        // (Optional flashbots MEV bundle submission can happen off-chain)

        // Step 3: Withdraw/liquidate liquidity immediately
        // (placeholder — logic to add and remove LP quickly)

        // Step 4: Repay flash loan
        uint256 totalOwed = amount + premium;
        IERC20(asset).safeApprove(address(POOL), totalOwed);
        return true;
    }

    function withdrawToken(address token, uint256 amount) external onlyOwner {
        IERC20(token).safeTransfer(owner, amount);
    }
}
