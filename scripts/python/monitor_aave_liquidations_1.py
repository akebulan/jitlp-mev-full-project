import os
import time
from decimal import Decimal

import requests
# === RPC + Web3 Setup ===
from dotenv import load_dotenv
from web3 import Web3

load_dotenv()
BASE_RPC = os.environ.get("BASE_RPC")
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

# === Liquidator Contract Setup ===
# Replace with your deployed contract address
LIQUIDATOR_ADDRESS = os.environ.get("LIQUIDATOR_ADDRESS")

# Minimal ABI for the liquidator contract
LIQUIDATOR_ABI = [
    {
        "inputs": [
            {"internalType": "address", "name": "user", "type": "address"},
            {"internalType": "address", "name": "debtAsset", "type": "address"},
            {"internalType": "address", "name": "collateralAsset", "type": "address"},
            {"internalType": "uint256", "name": "amount", "type": "uint256"}
        ],
        "name": "executeLiquidation",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function"
    }
]

# === Private Key for Transactions ===
# WARNING: Never hardcode private keys in production code
# Use environment variables or secure key management
PRIVATE_KEY = os.environ.get("PRIVATE_KEY")

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
        return hf, data
    except Exception as e:
        print(f"❌ HF error for {user[:8]}...: {e}")
        return None, None

def fetch_risky_users():
    query = """
    {
      userReserves(first: 100, where: {currentTotalDebt_gt: "0"}) {
        user {
          id
        }
        reserve {
          underlyingAsset
          symbol
        }
        currentTotalDebt
      }
    }
    """
    try:
        res = requests.post(SUBGRAPH_URL, json={"query": query})
        out = res.json()
        if "errors" in out:
            print("❌ Subgraph error:", out["errors"])
            return []

        # Group by user to get debt and collateral info
        user_data = {}
        for entry in out["data"]["userReserves"]:
            user_id = entry["user"]["id"].lower()
            if user_id not in user_data:
                user_data[user_id] = {"debts": [], "collaterals": []}

            debt = float(entry["currentTotalDebt"])
            asset = entry["reserve"]["underlyingAsset"]
            symbol = entry["reserve"]["symbol"]

            if debt > 0:
                user_data[user_id]["debts"].append({
                    "asset": asset,
                    "symbol": symbol,
                    "amount": debt
                })
            else:
                user_data[user_id]["collaterals"].append({
                    "asset": asset,
                    "symbol": symbol
                })

        return user_data
    except Exception as e:
        print(f"❌ Error fetching subgraph users: {e}")
        return {}

def get_token_decimals(token_address):
    """Get the number of decimals for a token"""
    try:
        abi = [{"inputs": [], "name": "decimals", "outputs": [{"internalType": "uint8", "name": "", "type": "uint8"}], "stateMutability": "view", "type": "function"}]
        token = web3.eth.contract(address=Web3.to_checksum_address(token_address), abi=abi)
        return token.functions.decimals().call()
    except Exception:
        # Default to 18 decimals if we can't determine
        return 18

def execute_liquidation(user, debt_asset, collateral_asset, amount, test_mode=True):
    if not PRIVATE_KEY:
        print("⚠️ No private key set. Skipping liquidation.")
        return False

    try:
        account = web3.eth.account.from_key(PRIVATE_KEY)
        liquidator = web3.eth.contract(address=LIQUIDATOR_ADDRESS, abi=LIQUIDATOR_ABI)
        
        # In test mode, use a fixed meaningful amount (1 ETH)
        if test_mode:
            amount_wei = web3.to_wei(1, 'ether')
            print(f"  Using test amount: 1.0 ETH")
        else:
            # For real liquidations, use the calculated amount
            # Get token decimals for the debt asset
            decimals = get_token_decimals(debt_asset)
            print(f"  Token decimals: {decimals}")
            
            # Convert to Wei for the contract call
            amount_wei = web3.to_wei(amount, 'ether')

        # Build transaction
        tx = liquidator.functions.executeLiquidation(
            Web3.to_checksum_address(user),
            Web3.to_checksum_address(debt_asset),
            Web3.to_checksum_address(collateral_asset),
            amount_wei
        ).build_transaction({
            'from': account.address,
            'nonce': web3.eth.get_transaction_count(account.address),
            'gas': 2000000,
            'gasPrice': web3.eth.gas_price
        })

        # Sign and send transaction
        signed_tx = web3.eth.account.sign_transaction(tx, PRIVATE_KEY)
        # Handle different web3.py versions
        if hasattr(signed_tx, 'rawTransaction'):
            tx_hash = web3.eth.send_raw_transaction(signed_tx.rawTransaction)
        else:
            tx_hash = web3.eth.send_raw_transaction(signed_tx.raw_transaction)

        print(f"🚀 Liquidation tx sent: {web3.to_hex(tx_hash)}")

        # Wait for transaction receipt
        receipt = web3.eth.wait_for_transaction_receipt(tx_hash)
        if receipt.status == 1:
            print(f"✅ Liquidation successful!")
            return True
        else:
            print(f"❌ Liquidation failed!")
            
            # Get transaction details for debugging
            tx_details = web3.eth.get_transaction(tx_hash)
            print(f"  Transaction details:")
            print(f"  - Gas used: {receipt.gasUsed}")
            print(f"  - Gas limit: {tx_details['gas']}")
            
            # Try to get revert reason
            try:
                # Get the full transaction trace
                debug_trace = web3.provider.make_request("debug_traceTransaction", [web3.to_hex(tx_hash), {"tracer": "callTracer"}])
                if "error" in debug_trace:
                    print(f"  - Error: {debug_trace['error']}")
                elif "result" in debug_trace and "error" in debug_trace["result"]:
                    print(f"  - Revert reason: {debug_trace['result']['error']}")
                else:
                    # Try another method to get revert reason
                    tx_data = {
                        "from": tx_details["from"],
                        "to": tx_details["to"],
                        "data": tx_details["input"],
                        "gas": tx_details["gas"],
                        "gasPrice": tx_details["gasPrice"],
                        "value": tx_details["value"]
                    }
                    
                    # Call the transaction to get revert reason
                    try:
                        web3.eth.call(tx_data, receipt.blockNumber)
                    except Exception as call_error:
                        print(f"  - Revert reason: {str(call_error)}")
            except Exception as trace_error:
                print(f"  - Could not get detailed error: {trace_error}")
                
            # Get transaction URL for block explorer
            tx_url = f"https://basescan.org/tx/{web3.to_hex(tx_hash)}"
            print(f"  - View transaction: {tx_url}")
            
            return False

    except Exception as e:
        print(f"❌ Liquidation error: {e}")
        return False

def monitor(test_mode=False, max_liquidations=1, use_bloxroute=False):
    print("🔁 Fetching active borrowers from The Graph...")
    user_data = fetch_risky_users()
    if not user_data:
        print("⚠️ No borrowers fetched from subgraph.")
        return

    pool = get_pool()
    print(f"✅ Aave Pool: {pool}")
    
    if use_bloxroute:
        print("🚀 Using bloXroute for MEV protection")
        # Import here to avoid dependency issues if bloXroute is not configured
        try:
            import bloxroute_liquidator
            print("✅ bloXroute module loaded")
        except ImportError:
            print("❌ bloXroute module not found, falling back to regular transactions")
            use_bloxroute = False

    print("\n📊 On-Chain Health Factors:")
    
    # Track users with lowest health factors for test mode
    lowest_hf_users = []
    
    for user, data in user_data.items():
        hf, account_data = get_user_hf(pool, user)
        if hf is None:
            continue
            
        # Store users with low HF for test mode
        if hf < 1.1:
            lowest_hf_users.append((user, hf, data))
        
        # Print normal health factor
        if hf >= 1:
            print(f"✅ Safe User: {user[:8]}... HF = {hf:.4f}")
        
    # Sort users by health factor (ascending)
    if lowest_hf_users:
        lowest_hf_users.sort(key=lambda x: x[1])
        
    # Process liquidatable users or test mode
    liquidation_count = 0
    
    for user, hf, data in lowest_hf_users:
        # Stop if we've reached the maximum number of liquidations
        if liquidation_count >= max_liquidations:
            break
            
        if hf < 1 or (test_mode and hf < 1.05):
            # In test mode, simulate liquidation for the user with lowest HF
            test_str = "[TEST MODE] " if test_mode and hf >= 1 else ""
            print(f"🔥 {test_str}LIQUIDATABLE: {user[:8]}... HF = {hf:.4f}")

            # Find largest debt to liquidate
            if data["debts"]:
                largest_debt = max(data["debts"], key=lambda x: x["amount"])
                debt_asset = largest_debt["asset"]
                debt_symbol = largest_debt["symbol"]

                # Get collateral assets from on-chain data if none found in subgraph
                if not data["collaterals"]:
                    print(f"  ⚠️ No collateral found in subgraph for {user[:8]}...")
                    
                    try:
                        # Import the collateral finder module
                        import aave_collateral_finder
                        
                        # Get the best collateral asset for this user
                        print(f"  Querying on-chain data for collateral...")
                        _, best_collateral = aave_collateral_finder.get_best_liquidation_pair(user)
                        
                        if best_collateral:
                            collateral_asset = best_collateral
                            # Get symbol (simplified)
                            collateral_symbol = best_collateral[-4:]
                            print(f"  Found on-chain collateral: {collateral_symbol}")
                        else:
                            # Fallback to default
                            collateral_asset = "0x4200000000000000000000000000000000000006"  # WETH on Base
                            collateral_symbol = "WETH"
                            print(f"  Using default collateral: {collateral_symbol}")
                    except Exception as e:
                        print(f"  Error finding collateral: {e}")
                        # Fallback to default
                        collateral_asset = "0x4200000000000000000000000000000000000006"  # WETH on Base
                        collateral_symbol = "WETH"
                        print(f"  Using default collateral: {collateral_symbol}")
                else:
                    collateral_asset = data["collaterals"][0]["asset"]
                    collateral_symbol = data["collaterals"][0]["symbol"]

                # Calculate liquidation amount (50% of debt)
                # For Aave liquidations, you can liquidate up to 50% of the debt
                # Note: The amount from subgraph is already in token units, not raw
                liquidation_amount = largest_debt["amount"] * 0.5
                print(f"  Raw debt amount: {largest_debt['amount']}")
                print(f"  50% liquidation amount: {liquidation_amount}")

                print(f"  Attempting liquidation:")
                print(f"  - Debt: {debt_symbol} ({debt_asset[:8]}...)")
                print(f"  - Collateral: {collateral_symbol} ({collateral_asset[:8]}...)")
                print(f"  - Amount: {liquidation_amount:.4f}")

                # Execute liquidation
                try:
                    if use_bloxroute:
                        # Try to use bloXroute for MEV protection
                        import bloxroute_liquidator
                        print("Attempting to use bloXroute for transaction submission...")
                        result = bloxroute_liquidator.execute_liquidation_with_bloxroute(
                            user, debt_asset, collateral_asset, 
                            1.0 if test_mode else liquidation_amount
                        )
                    else:
                        # Use regular transaction
                        result = execute_liquidation(user, debt_asset, collateral_asset, liquidation_amount, test_mode)
                except Exception as e:
                    print(f"❌ Error with bloXroute: {e}")
                    print("Falling back to regular transaction submission...")
                    result = execute_liquidation(user, debt_asset, collateral_asset, liquidation_amount, test_mode)
                if result:
                    liquidation_count += 1

# === Loop ===
if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description='Aave liquidation monitor')
    parser.add_argument('--test', action='store_true', help='Run in test mode to simulate liquidations')
    parser.add_argument('--max-liquidations', type=int, default=1, help='Maximum number of liquidations per run')
    parser.add_argument('--interval', type=int, default=60, help='Seconds between checks')
    parser.add_argument('--bloxroute', action='store_true', help='Use bloXroute for MEV protection')
    parser.add_argument('--auth', type=str, help='bloXroute auth token (overrides env variable)')
    args = parser.parse_args()
    
    test_mode = args.test
    max_liquidations = args.max_liquidations
    interval = args.interval
    use_bloxroute = args.bloxroute
    
    # Override auth token if provided
    if args.auth:
        os.environ["BLOXROUTE_AUTH_HEADER"] = args.auth
        print(f"Using provided auth token: {args.auth[:10]}...")
    
    print(f"🚀 Starting Aave liquidation monitor on Base network")
    if test_mode:
        print(f"⚠️ RUNNING IN TEST MODE - Will simulate up to {max_liquidations} liquidations per run")
    print(f"📝 Liquidator contract: {LIQUIDATOR_ADDRESS}")
    print(f"🔑 Using account: {web3.eth.account.from_key(PRIVATE_KEY).address if PRIVATE_KEY else 'No private key set'}")
    
    while True:
        try:
            monitor(test_mode, max_liquidations, use_bloxroute)
        except Exception as e:
            print("❌ Unexpected error:", e)
        print(f"\n⏳ Sleeping {interval} seconds...\n")
        time.sleep(interval)