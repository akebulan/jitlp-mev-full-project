// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

import {IPool} from "@aave/core-v3/contracts/interfaces/IPool.sol";
import {IPoolAddressesProvider} from "@aave/core-v3/contracts/interfaces/IPoolAddressesProvider.sol";
import {IFlashLoanSimpleReceiver} from "@aave/core-v3/contracts/flashloan/interfaces/IFlashLoanSimpleReceiver.sol";
import {IERC20} from "@openzeppelin/contracts/token/ERC20/IERC20.sol";
import {SafeERC20} from "@openzeppelin/contracts/token/ERC20/utils/SafeERC20.sol";
import {Ownable} from "@openzeppelin/contracts/access/Ownable.sol";

contract AaveV3Liquidator is IFlashLoanSimpleReceiver, Ownable {
    using SafeERC20 for IERC20;

    IPoolAddressesProvider private immutable _addressesProvider;
    IPool public immutable override POOL;
    
    // Override the interface function to return the correct type
    function ADDRESSES_PROVIDER() public view override returns (IPoolAddressesProvider) {
        return _addressesProvider;
    }

    constructor(
        address _provider,
        address _pool
    ) {
        _addressesProvider = IPoolAddressesProvider(_provider);
        POOL = IPool(_pool);
    }

    function executeLiquidation(
        address user,
        address debtAsset,
        address collateralAsset,
        uint256 amount
    ) external onlyOwner {
        bytes memory params = abi.encode(user, debtAsset, collateralAsset);
        POOL.flashLoanSimple(
            address(this),
            debtAsset,
            amount,
            params,
            0
        );
    }

    function executeOperation(
        address asset,
        uint256 amount,
        uint256 premium,
        address initiator,
        bytes calldata params
    ) external override returns (bool) {
        require(msg.sender == address(POOL), "Only Aave Pool can call");
        require(initiator == address(this), "Only this contract can initiate");

        (address user, address debtAsset, address collateralAsset) = abi.decode(params, (address, address, address));

        // Approve debtAsset for repayment
        IERC20(debtAsset).safeApprove(address(POOL), amount);

        // Perform liquidation
        POOL.liquidationCall(
            collateralAsset,
            debtAsset,
            user,
            amount,
            false
        );

        // Repay flash loan
        uint256 totalOwed = amount + premium;
        IERC20(asset).safeApprove(address(POOL), totalOwed);

        return true;
    }

    // Allow recovery of ERC20s mistakenly sent
    function sweep(address token) external onlyOwner {
        IERC20(token).safeTransfer(msg.sender, IERC20(token).balanceOf(address(this)));
    }
}
