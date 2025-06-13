import requests
import time
from decimal import Decimal
from web3 import Web3

# === Configuration ===

# ✅ Reliable Ankr RPC (your key)
BASE_RPC = "https://rpc.ankr.com/base/771c5a98e239e1408deb1448260331b2681301af27f4a7f6e323a57e383ffd95"
web3 = Web3(Web3.HTTPProvider(BASE_RPC))

# ✅ AaveOracle address on Base
AAVE_ORACLE_ADDRESS = Web3.to_checksum_address("0x2Cc0Fc26eD4563A5ce5e8bdcfe1A2878676Ae156")

# ✅ Supported tokens with working price feeds
ASSETS = {
    "cbETH": Web3.to_checksum_address("0x2Ae3F1Ec7F1F5012CFEab0185bfc7aa3cf0DEc22"),
    "WETH": Web3.to_checksum_address("0x4200000000000000000000000000000000000006"),
    "wstETH": Web3.to_checksum_address("0xc1CBa3fCea344f92D9239c08C0568f6F2F0ee452")
}

# Aave liquidation thresholds (Base config estimates)
LIQUIDATION_THRESHOLD = {
    "cbETH": Decimal("0.77"),
    "WETH": Decimal("0.80"),
    "wstETH": Decimal("0.77")
}

# ABI for getAssetPrice(address)
ORACLE_ABI = [{
    "inputs": [{"internalType": "address", "name": "asset", "type": "address"}],
    "name": "getAssetPrice",
    "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
    "stateMutability": "view",
    "type": "function"
}]

# ✅ Active Base v3 subgraph
SUBGRAPH_URL = "https://gateway.thegraph.com/api/1a8f7cc18094075c9ab149357cabf07a/subgraphs/id/GQFbb95cE6d8mV989mL5figjaGaKCQB3xqYrr1bRyXqF"

# === Core Logic ===

def get_aave_prices():
    oracle = web3.eth.contract(address=AAVE_ORACLE_ADDRESS, abi=ORACLE_ABI)
    prices = {}
    for symbol, token_addr in ASSETS.items():
        try:
            raw_price = oracle.functions.getAssetPrice(token_addr).call()
            prices[symbol] = Decimal(raw_price) / Decimal(1e18)
            print(f"✅ {symbol} price: {prices[symbol]:,.4f} USD")
        except Exception as e:
            print(f"❌ Error fetching {symbol} price: {e}")
    return prices

def calculate_health_factor(user_reserves, prices, thresholds):
    total_collateral_usd = Decimal("0")
    total_debt_usd = Decimal("0")

    for ur in user_reserves:
        symbol = ur["reserve"]["symbol"]
        decimals = int(ur["reserve"]["decimals"])
        price = prices.get(symbol, Decimal("0"))
        threshold = thresholds.get(symbol, Decimal("0"))

        collateral = Decimal(ur.get("currentATokenBalance", "0")) / (10 ** decimals)
        debt = Decimal(ur.get("currentTotalDebt", "0")) / (10 ** decimals)

        if ur.get("usageAsCollateralEnabledOnUser", False):
            total_collateral_usd += collateral * price * threshold

        total_debt_usd += debt * price

    if total_debt_usd == 0:
        return Decimal("999")
    return total_collateral_usd / total_debt_usd

def monitor_liquidations():
    QUERY = """
    {
      userReserves(first: 50, where: {currentTotalDebt_gt: "0"}) {
        user {
          id
        }
        currentTotalDebt
        currentATokenBalance
        usageAsCollateralEnabledOnUser
        reserve {
          symbol
          decimals
        }
      }
    }
    """

    print("🔁 Fetching Aave prices + user data...")
    prices = get_aave_prices()
    if not prices:
        print("❌ Failed to fetch live prices.")
        return

    res = requests.post(SUBGRAPH_URL, json={'query': QUERY})
    data = res.json()

    if "errors" in data:
        print("❌ Subgraph error:", data["errors"])
        return

    users = {}
    for ur in data["data"]["userReserves"]:
        uid = ur["user"]["id"]
        users.setdefault(uid, []).append(ur)

    print("\n📊 Health Factor Results:")
    for user_id, reserves in users.items():
        hf = calculate_health_factor(reserves, prices, LIQUIDATION_THRESHOLD)
        if hf < 1.0:
            print(f"  🔥 Risky User: {user_id[:8]}... HF = {hf:.4f}")
        else:
            print(f"  ✅ Safe User:  {user_id[:8]}... HF = {hf:.4f}")

# === Loop ===
if __name__ == "__main__":
    while True:
        try:
            monitor_liquidations()
        except Exception as e:
            print("❌ Unexpected error:", e)
        print("\n⏳ Sleeping 60 seconds...\n")
        time.sleep(60)
