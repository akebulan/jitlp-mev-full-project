import requests
import time
from decimal import Decimal
from web3 import Web3

# === RPC + Web3 Setup ===
BASE_RPC = "https://rpc.ankr.com/base/771c5a98e239e1408deb1448260331b2681301af27f4a7f6e323a57e383ffd95"
web3 = Web3(Web3.HTTPProvider(BASE_RPC))

# === Aave Addresses and ABIs ===
PROVIDER_ADDRESS = Web3.to_checksum_address("0xe20fCBdBfFC4Dd138cE8b2E6FBb6CB49777ad64D")

PROVIDER_ABI = [{
    "inputs": [],
    "name": "getPool",
    "outputs": [{"internalType": "address", "name": "", "type": "address"}],
    "stateMutability": "view",
    "type": "function"
}]

POOL_ABI = [{
    "inputs": [{"internalType": "address", "name": "user", "type": "address"}],
    "name": "getUserAccountData",
    "outputs": [
        {"internalType": "uint256", "name": "totalCollateralBase", "type": "uint256"},
        {"internalType": "uint256", "name": "totalDebtBase", "type": "uint256"},
        {"internalType": "uint256", "name": "availableBorrowsBase", "type": "uint256"},
        {"internalType": "uint256", "name": "currentLiquidationThreshold", "type": "uint256"},
        {"internalType": "uint256", "name": "ltv", "type": "uint256"},
        {"internalType": "uint256", "name": "healthFactor", "type": "uint256"}
    ],
    "stateMutability": "view",
    "type": "function"
}]

# ✅ Aave v3 Subgraph for Base
SUBGRAPH_URL = "https://gateway.thegraph.com/api/1a8f7cc18094075c9ab149357cabf07a/subgraphs/id/GQFbb95cE6d8mV989mL5figjaGaKCQB3xqYrr1bRyXqF"

# === Functions ===

def get_pool():
    provider = web3.eth.contract(address=PROVIDER_ADDRESS, abi=PROVIDER_ABI)
    return provider.functions.getPool().call()

def get_user_hf(pool_addr, user):
    pool = web3.eth.contract(address=pool_addr, abi=POOL_ABI)
    try:
        data = pool.functions.getUserAccountData(Web3.to_checksum_address(user)).call()
        hf = Decimal(data[5]) / Decimal(1e18)
        return hf
    except Exception as e:
        print(f"❌ HF error for {user[:8]}...: {e}")
        return None

def fetch_risky_users():
    query = """
    {
      userReserves(first: 100, where: {currentTotalDebt_gt: "0"}) {
        user {
          id
        }
      }
    }
    """
    try:
        res = requests.post(SUBGRAPH_URL, json={"query": query})
        out = res.json()
        if "errors" in out:
            print("❌ Subgraph error:", out["errors"])
            return []
        users = {entry["user"]["id"].lower() for entry in out["data"]["userReserves"]}
        return list(users)
    except Exception as e:
        print(f"❌ Error fetching subgraph users: {e}")
        return []

def monitor():
    print("🔁 Fetching active borrowers from The Graph...")
    risky_users = fetch_risky_users()
    if not risky_users:
        print("⚠️ No borrowers fetched from subgraph.")
        return

    pool = get_pool()
    print(f"✅ Aave Pool: {pool}")

    print("\n📊 On-Chain Health Factors:")
    for user in risky_users:
        hf = get_user_hf(pool, user)
        if hf is None:
            continue
        status = "🔥 Risky" if hf < 1 else "✅ Safe "
        print(f"{status} User: {user[:8]}... HF = {hf:.4f}")

# === Loop ===
if __name__ == "__main__":
    while True:
        try:
            monitor()
        except Exception as e:
            print("❌ Unexpected error:", e)
        print("\n⏳ Sleeping 60 seconds...\n")
        time.sleep(60)
