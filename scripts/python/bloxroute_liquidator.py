import os
import json
import time
import requests
from web3 import Web3
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# bloXroute configuration
BLOXROUTE_AUTH_HEADER = os.environ.get("BLOXROUTE_AUTH_HEADER")
BLOXROUTE_BASE_URL = os.environ.get("BLOXROUTE_BASE_URL", "https://api.blxrbdn.com")

# Contract configuration
LIQUIDATOR_ADDRESS = os.environ.get("LIQUIDATOR_ADDRESS")
PRIVATE_KEY = os.environ.get("PRIVATE_KEY")

# Initialize Web3 with standard RPC for read operations
BASE_RPC = os.environ.get("BASE_RPC")
web3 = Web3(Web3.HTTPProvider(BASE_RPC))

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

def try_auth_formats(auth_token):
    """Try different authentication formats"""
    auth_formats = []
    
    # Format 1: Direct token
    auth_formats.append(auth_token)
    
    # Format 2: Bearer token
    auth_formats.append(f"Bearer {auth_token}")
    
    # Format 3: Basic auth
    import base64
    try:
        auth_bytes = auth_token.encode('ascii')
        base64_auth = base64.b64encode(auth_bytes).decode('ascii')
        auth_formats.append(f"Basic {base64_auth}")
    except:
        pass
    
    return auth_formats

def send_tx_via_bloxroute(signed_tx):
    """
    Send a transaction through bloXroute
    """
    # Get raw transaction hex
    raw_tx = signed_tx.rawTransaction.hex() if hasattr(signed_tx, 'rawTransaction') else signed_tx.raw_transaction.hex()
    
    # Prepare payload for bloXroute API
    payload = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "blxr_tx",
        "params": {
            "transaction": raw_tx,
            "blockchain_network": "Base-Mainnet"
        }
    }
    
    # Try different authentication formats
    auth_formats = try_auth_formats(BLOXROUTE_AUTH_HEADER)
    
    for i, auth in enumerate(auth_formats):
        print(f"Trying authentication format {i+1}...")
        
        headers = {
            "Content-Type": "application/json",
            "Authorization": auth
        }
        
        try:
            response = requests.post(BLOXROUTE_BASE_URL, headers=headers, json=payload)
            result = response.json()
            
            # Check if successful
            if 'result' in result and not 'error' in result:
                print(f"✅ Authentication format {i+1} worked!")
                return result
            else:
                print(f"❌ Format {i+1} failed: {result.get('error', {}).get('message', 'Unknown error')}")
        except Exception as e:
            print(f"❌ Error with format {i+1}: {e}")
    
    # If all formats failed, return the last result
    print("All authentication formats failed")
    return result

def execute_liquidation_with_bloxroute(user, debt_asset, collateral_asset, amount):
    """
    Execute a liquidation using bloXroute for faster transaction propagation
    """
    if not PRIVATE_KEY or not BLOXROUTE_AUTH_HEADER:
        print("⚠️ Missing private key or bloXroute auth header")
        return False
    
    try:
        account = web3.eth.account.from_key(PRIVATE_KEY)
        liquidator = web3.eth.contract(address=LIQUIDATOR_ADDRESS, abi=LIQUIDATOR_ABI)
        
        # Convert amount to Wei
        amount_wei = web3.to_wei(amount, 'ether')
        
        # Build transaction with higher gas price for priority
        tx = liquidator.functions.executeLiquidation(
            Web3.to_checksum_address(user),
            Web3.to_checksum_address(debt_asset),
            Web3.to_checksum_address(collateral_asset),
            amount_wei
        ).build_transaction({
            'from': account.address,
            'nonce': web3.eth.get_transaction_count(account.address),
            'gas': 2000000,
            'maxFeePerGas': web3.eth.gas_price * 2,  # Higher gas price for priority
            'maxPriorityFeePerGas': web3.eth.gas_price // 2,
            'chainId': 8453  # Base chain ID
        })
        
        # Sign transaction
        signed_tx = web3.eth.account.sign_transaction(tx, PRIVATE_KEY)
        
        # Send transaction through bloXroute for faster propagation
        print(f"🚀 Sending liquidation through bloXroute network...")
        result = send_tx_via_bloxroute(signed_tx)
        
        if result and 'result' in result:
            # Extract the transaction hash from the result
            if isinstance(result['result'], dict) and 'txHash' in result['result']:
                tx_hash = result['result']['txHash']
            else:
                tx_hash = result['result']
                
            print(f"✅ Transaction accepted: {tx_hash}")
            
            # Wait for transaction to be mined
            print("Waiting for transaction to be mined...")
            try:
                # Make sure tx_hash is a string
                if isinstance(tx_hash, dict):
                    tx_hash = tx_hash.get('txHash')
                    
                receipt = web3.eth.wait_for_transaction_receipt(tx_hash, timeout=120)
                if receipt.status == 1:
                    print(f"✅ Liquidation successful!")
                    return True
                else:
                    print(f"❌ Liquidation failed!")
                    return False
            except Exception as e:
                print(f"Error waiting for receipt: {e}")
                print(f"Transaction may still be pending. Check tx: {tx_hash}")
                return False
        else:
            print(f"❌ Transaction rejected: {result.get('error', {}).get('message', 'Unknown error')}")
            return False
            
    except Exception as e:
        print(f"❌ Liquidation error: {e}")
        return False

# Example usage
if __name__ == "__main__":
    import sys
    
    if len(sys.argv) < 5:
        print("Usage: python bloxroute_liquidator.py <user_address> <debt_asset> <collateral_asset> <amount>")
        sys.exit(1)
    
    user = sys.argv[1]
    debt_asset = sys.argv[2]
    collateral_asset = sys.argv[3]
    amount = float(sys.argv[4])
    
    print(f"Executing liquidation via bloXroute:")
    print(f"- User: {user}")
    print(f"- Debt asset: {debt_asset}")
    print(f"- Collateral asset: {collateral_asset}")
    print(f"- Amount: {amount} ETH")
    
    execute_liquidation_with_bloxroute(user, debt_asset, collateral_asset, amount)