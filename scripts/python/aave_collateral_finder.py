import os
from decimal import Decimal
from web3 import Web3
from dotenv import load_dotenv

load_dotenv()
BASE_RPC = os.environ.get("BASE_RPC", "https://mainnet.base.org")
web3 = Web3(Web3.HTTPProvider(BASE_RPC))

# Aave V3 contract addresses on Base
PROVIDER_ADDRESS = Web3.to_checksum_address("0xe20fCBdBfFC4Dd138cE8b2E6FBb6CB49777ad64D")
PRICE_ORACLE_ADDRESS = Web3.to_checksum_address("0x2Cc0Fc26eD4563A5ce5e8bdcfe1A2878676Ae156")

# ABIs
PROVIDER_ABI = [
    {"inputs": [], "name": "getPool", "outputs": [{"internalType": "address", "name": "", "type": "address"}], "stateMutability": "view", "type": "function"},
    {"inputs": [], "name": "getPriceOracle", "outputs": [{"internalType": "address", "name": "", "type": "address"}], "stateMutability": "view", "type": "function"}
]

POOL_ABI = [
    {"inputs": [{"internalType": "address", "name": "user", "type": "address"}], "name": "getUserAccountData", "outputs": [{"internalType": "uint256", "name": "totalCollateralBase", "type": "uint256"}, {"internalType": "uint256", "name": "totalDebtBase", "type": "uint256"}, {"internalType": "uint256", "name": "availableBorrowsBase", "type": "uint256"}, {"internalType": "uint256", "name": "currentLiquidationThreshold", "type": "uint256"}, {"internalType": "uint256", "name": "ltv", "type": "uint256"}, {"internalType": "uint256", "name": "healthFactor", "type": "uint256"}], "stateMutability": "view", "type": "function"},
    {"inputs": [{"internalType": "address", "name": "asset", "type": "address"}], "name": "getReserveData", "outputs": [{"components": [{"components": [{"internalType": "uint256", "name": "data", "type": "uint256"}], "internalType": "struct DataTypes.ReserveConfigurationMap", "name": "configuration", "type": "tuple"}, {"internalType": "uint128", "name": "liquidityIndex", "type": "uint128"}, {"internalType": "uint128", "name": "currentLiquidityRate", "type": "uint128"}, {"internalType": "uint128", "name": "variableBorrowIndex", "type": "uint128"}, {"internalType": "uint128", "name": "currentVariableBorrowRate", "type": "uint128"}, {"internalType": "uint128", "name": "currentStableBorrowRate", "type": "uint128"}, {"internalType": "uint40", "name": "lastUpdateTimestamp", "type": "uint40"}, {"internalType": "uint16", "name": "id", "type": "uint16"}, {"internalType": "address", "name": "aTokenAddress", "type": "address"}, {"internalType": "address", "name": "stableDebtTokenAddress", "type": "address"}, {"internalType": "address", "name": "variableDebtTokenAddress", "type": "address"}, {"internalType": "address", "name": "interestRateStrategyAddress", "type": "address"}, {"internalType": "uint128", "name": "accruedToTreasury", "type": "uint128"}, {"internalType": "uint128", "name": "unbacked", "type": "uint128"}, {"internalType": "uint128", "name": "isolationModeTotalDebt", "type": "uint128"}], "internalType": "struct DataTypes.ReserveData", "name": "", "type": "tuple"}], "stateMutability": "view", "type": "function"},
    {"inputs": [], "name": "getReservesList", "outputs": [{"internalType": "address[]", "name": "", "type": "address[]"}], "stateMutability": "view", "type": "function"}
]

ATOKEN_ABI = [
    {"inputs": [{"internalType": "address", "name": "user", "type": "address"}], "name": "balanceOf", "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}], "stateMutability": "view", "type": "function"},
    {"inputs": [], "name": "UNDERLYING_ASSET_ADDRESS", "outputs": [{"internalType": "address", "name": "", "type": "address"}], "stateMutability": "view", "type": "function"}
]

PRICE_ORACLE_ABI = [
    {"inputs": [{"internalType": "address", "name": "asset", "type": "address"}], "name": "getAssetPrice", "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}], "stateMutability": "view", "type": "function"}
]

ERC20_ABI = [
    {"inputs": [], "name": "decimals", "outputs": [{"internalType": "uint8", "name": "", "type": "uint8"}], "stateMutability": "view", "type": "function"},
    {"inputs": [], "name": "symbol", "outputs": [{"internalType": "string", "name": "", "type": "string"}], "stateMutability": "view", "type": "function"}
]

def get_user_collaterals(user_address):
    """
    Get all collateral assets for a user with their USD values
    """
    user = Web3.to_checksum_address(user_address)
    
    # Get contract instances
    provider = web3.eth.contract(address=PROVIDER_ADDRESS, abi=PROVIDER_ABI)
    pool_address = provider.functions.getPool().call()
    pool = web3.eth.contract(address=pool_address, abi=POOL_ABI)
    
    # Get price oracle
    oracle_address = provider.functions.getPriceOracle().call()
    oracle = web3.eth.contract(address=oracle_address, abi=PRICE_ORACLE_ABI)
    
    # Get all reserves in the pool
    reserves = pool.functions.getReservesList().call()
    
    collaterals = []
    
    # Check each reserve for user's aToken balance
    for asset in reserves:
        try:
            # Get aToken address for this asset
            reserve_data = pool.functions.getReserveData(asset).call()
            atoken_address = reserve_data[8]  # aTokenAddress is at index 8
            
            # Create aToken contract
            atoken = web3.eth.contract(address=atoken_address, abi=ATOKEN_ABI)
            
            # Check user's balance
            balance = atoken.functions.balanceOf(user).call()
            
            if balance > 0:
                # Get asset details
                asset_contract = web3.eth.contract(address=asset, abi=ERC20_ABI)
                try:
                    symbol = asset_contract.functions.symbol().call()
                except:
                    symbol = f"Unknown-{asset[:6]}"
                
                try:
                    decimals = asset_contract.functions.decimals().call()
                except:
                    decimals = 18
                
                # Get price from oracle
                price = oracle.functions.getAssetPrice(asset).call()
                
                # Calculate USD value (price is in ETH, need to convert to USD)
                balance_decimal = Decimal(balance) / Decimal(10 ** decimals)
                price_decimal = Decimal(price) / Decimal(10 ** 8)  # Oracle prices are in 8 decimals
                
                value_usd = balance_decimal * price_decimal
                
                collaterals.append({
                    'asset': asset,
                    'symbol': symbol,
                    'balance': float(balance_decimal),
                    'price': float(price_decimal),
                    'value_usd': float(value_usd)
                })
        except Exception as e:
            print(f"Error processing asset {asset}: {e}")
    
    # Sort by USD value (highest first)
    collaterals.sort(key=lambda x: x['value_usd'], reverse=True)
    
    return collaterals

def get_best_liquidation_pair(user_address):
    """
    Find the best debt/collateral pair for liquidation
    """
    user = Web3.to_checksum_address(user_address)
    
    # Get contract instances
    provider = web3.eth.contract(address=PROVIDER_ADDRESS, abi=PROVIDER_ABI)
    pool_address = provider.functions.getPool().call()
    pool = web3.eth.contract(address=pool_address, abi=POOL_ABI)
    
    # Get user's collaterals
    collaterals = get_user_collaterals(user)
    if not collaterals:
        print(f"No collateral found for user {user}")
        return None, None
    
    # Get most valuable collateral
    best_collateral = collaterals[0]
    
    # For simplicity, we'll use USDC as debt asset
    # In a real implementation, you'd check the user's actual debts
    debt_asset = "0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913"  # USDC on Base
    
    return debt_asset, best_collateral['asset']

# Example usage
if __name__ == "__main__":
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python aave_collateral_finder.py <user_address>")
        sys.exit(1)
    
    user_address = sys.argv[1]
    
    print(f"Finding collaterals for {user_address}...")
    collaterals = get_user_collaterals(user_address)
    
    if not collaterals:
        print("No collateral found")
    else:
        print(f"\nFound {len(collaterals)} collateral assets:")
        for c in collaterals:
            print(f"  {c['symbol']}: {c['balance']:.4f} (${c['value_usd']:.2f})")
        
        debt_asset, collateral_asset = get_best_liquidation_pair(user_address)
        print(f"\nBest liquidation pair:")
        print(f"  Debt asset: {debt_asset}")
        print(f"  Collateral asset: {collateral_asset}")