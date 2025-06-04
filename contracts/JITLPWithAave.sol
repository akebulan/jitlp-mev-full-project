// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

import "@openzeppelin/contracts/access/Ownable.sol";
import "@openzeppelin/contracts/token/ERC20/IERC20.sol";
import "@openzeppelin/contracts/token/ERC721/IERC721Receiver.sol";

import { IPool } from "@aave/core-v3/contracts/interfaces/IPool.sol";
import { ISwapRouter } from "@uniswap/v3-periphery/contracts/interfaces/ISwapRouter.sol";
import { INonfungiblePositionManager } from "@uniswap/v3-periphery/contracts/interfaces/INonfungiblePositionManager.sol";

contract JITLPWithAave is Ownable, IERC721Receiver {
    address public immutable weth;
    address public immutable usdc;
    address public immutable aavePool;
    address public immutable swapRouter;
    address public immutable positionManager;

    uint24 public constant poolFee = 500;
    int24 public constant tickLower = -60;
    int24 public constant tickUpper = 60;

    uint256 public tokenId;

    constructor(
        address _weth,
        address _usdc,
        address _aavePool,
        address _swapRouter,
        address _positionManager
    ) {
        weth = _weth;
        usdc = _usdc;
        aavePool = _aavePool;
        swapRouter = _swapRouter;
        positionManager = _positionManager;

        IERC20(weth).approve(swapRouter, type(uint256).max);
        IERC20(usdc).approve(swapRouter, type(uint256).max);
        IERC20(weth).approve(positionManager, type(uint256).max);
        IERC20(usdc).approve(positionManager, type(uint256).max);
    }

    function initiateFlashLoan(uint256 amount) external onlyOwner {
        address[] memory assets;
        uint256[] memory amounts;
        uint256[] memory modes;

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
        address initiator,
        bytes calldata
    ) external returns (bool) {
        require(msg.sender == aavePool, "Not Aave pool");
        require(initiator == address(this), "Not initiated by this contract");

        uint256 flashAmount = amounts[0];
        uint256 half = flashAmount / 2;
        assets;

        // Swap half WETH → USDC
        ISwapRouter.ExactInputSingleParams memory params = ISwapRouter.ExactInputSingleParams({
            tokenIn: weth,
            tokenOut: usdc,
            fee: poolFee,
            recipient: address(this),
            deadline: block.timestamp,
            amountIn: half,
            amountOutMinimum: 0,
            sqrtPriceLimitX96: 0
        });

        uint256 usdcOut = ISwapRouter(swapRouter).exactInputSingle(params);

        // Add liquidity to Uniswap v3
        (tokenId,,,) = INonfungiblePositionManager(positionManager).mint(
            INonfungiblePositionManager.MintParams({
                token0: weth,
                token1: usdc,
                fee: poolFee,
                tickLower: tickLower,
                tickUpper: tickUpper,
                amount0Desired: half,
                amount1Desired: usdcOut,
                amount0Min: 0,
                amount1Min: 0,
                recipient: address(this),
                deadline: block.timestamp
            })
        );

        // Immediately pull liquidity (JIT strategy)
        INonfungiblePositionManager(positionManager).decreaseLiquidity(
            INonfungiblePositionManager.DecreaseLiquidityParams({
                tokenId: tokenId,
                liquidity: 1e6, // placeholder for actual liquidity
                amount0Min: 0,
                amount1Min: 0,
                deadline: block.timestamp
            })
        );

        INonfungiblePositionManager(positionManager).collect(
            INonfungiblePositionManager.CollectParams({
                tokenId: tokenId,
                recipient: address(this),
                amount0Max: type(uint128).max,
                amount1Max: type(uint128).max
            })
        );

        // Repay Aave
        uint256 totalOwed = amounts[0] + premiums[0];
        IERC20(weth).approve(aavePool, totalOwed);

        return true;
    }

    function onERC721Received(
        address,
        address,
        uint256,
        bytes calldata
    ) external pure override returns (bytes4) {
        return this.onERC721Received.selector;
    }

    receive() external payable {}
}
