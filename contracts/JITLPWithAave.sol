// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

import { IPool } from "@aave/core-v3/contracts/interfaces/IPool.sol";
import { IERC20 } from "@openzeppelin/contracts/token/ERC20/IERC20.sol";
import { ISwapRouter } from "@uniswap/v3-periphery/contracts/interfaces/ISwapRouter.sol";
import { INonfungiblePositionManager, INonfungiblePositionManagerStructs } from "@uniswap/v3-periphery/contracts/interfaces/INonfungiblePositionManager.sol";

interface IWETH is IERC20 {
    function deposit() external payable;
    function withdraw(uint256) external;
}

contract JITLPWithAave {
    address public owner;
    address public aavePool;
    address public weth;
    address public usdc;
    address public uniswapRouter;
    address public positionManager;

    uint24 public constant FEE_TIER = 500;
    int24 public constant TICK_LOWER = -60;
    int24 public constant TICK_UPPER = 60;

    uint256 public tokenId;

    constructor(
        address _aavePool,
        address _weth,
        address _usdc,
        address _uniswapRouter,
        address _positionManager
    ) {
        owner = msg.sender;
        aavePool = _aavePool;
        weth = _weth;
        usdc = _usdc;
        uniswapRouter = _uniswapRouter;
        positionManager = _positionManager;

        IERC20(weth).approve(positionManager, type(uint256).max);
        IERC20(usdc).approve(positionManager, type(uint256).max);
        IERC20(weth).approve(uniswapRouter, type(uint256).max);
    }

    modifier onlyOwner() {
        require(msg.sender == owner, "Not owner");
        _;
    }

    function initiateFlashLoan(uint256 amount) external onlyOwner {
        address[] memory assets = new address[](1);
        uint256[] memory amounts = new uint256[](1);
        uint256[] memory modes = new uint256[](1);

        assets[0] = weth;
        amounts[0] = amount;
        modes[0] = 0;

        IPool(aavePool).flashLoan(
            address(this),
            assets,
            amounts,
            modes,
            address(this),
            "",
            0
        );
    }

    function executeOperation(
        address[] calldata assets,
        uint256[] calldata amounts,
        uint256[] calldata premiums,
        address,
        bytes calldata
    ) external returns (bool) {
        require(msg.sender == aavePool, "Unauthorized caller");

        uint256 flashAmount = amounts[0];
        uint256 loanFee = premiums[0];

        uint256 half = flashAmount / 2;

        ISwapRouter.ExactInputSingleParams memory params = ISwapRouter.ExactInputSingleParams({
            tokenIn: weth,
            tokenOut: usdc,
            fee: FEE_TIER,
            recipient: address(this),
            deadline: block.timestamp,
            amountIn: half,
            amountOutMinimum: 0,
            sqrtPriceLimitX96: 0
        });

        uint256 usdcOut = ISwapRouter(uniswapRouter).exactInputSingle(params);

        (tokenId,,,) = INonfungiblePositionManager(positionManager).mint(
            INonfungiblePositionManagerStructs.MintParams({
                token0: weth,
                token1: usdc,
                fee: FEE_TIER,
                tickLower: TICK_LOWER,
                tickUpper: TICK_UPPER,
                amount0Desired: half,
                amount1Desired: usdcOut,
                amount0Min: 0,
                amount1Min: 0,
                recipient: address(this),
                deadline: block.timestamp
            })
        );

        INonfungiblePositionManager(positionManager).decreaseLiquidity(
            INonfungiblePositionManagerStructs.DecreaseLiquidityParams({
                tokenId: tokenId,
                liquidity: 1e6,
                amount0Min: 0,
                amount1Min: 0,
                deadline: block.timestamp
            })
        );

        INonfungiblePositionManager(positionManager).collect(
            INonfungiblePositionManagerStructs.CollectParams({
                tokenId: tokenId,
                recipient: address(this),
                amount0Max: type(uint128).max,
                amount1Max: type(uint128).max
            })
        );

        uint256 totalOwed = flashAmount + loanFee;
        IERC20(weth).approve(aavePool, totalOwed);

        return true;
    }

    receive() external payable {}
}
