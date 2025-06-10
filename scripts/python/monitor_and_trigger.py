# monitor_and_trigger.py
from web3 import Web3
import asyncio
import json

QUICKNODE_WSS = "wss://your-polygon-ws-endpoint"
CONTRACT_ADDRESS = "0xYourDeployedContract"
POOL_ADDRESS = "0xTargetUniswapV3Pool"
TOKEN = "0x7ceB23fD6bC0adD59E62ac25578270cFf1b9f619"  # Example: WETH
AMOUNT = Web3.toWei(1, 'ether')  # Adjust based on strategy

with open("JITLPExecutor_abi.json") as f:
    CONTRACT_ABI = json.load(f)

w3 = Web3(Web3.WebsocketProvider(QUICKNODE_WSS))
contract = w3.eth.contract(address=CONTRACT_ADDRESS, abi=CONTRACT_ABI)
account = w3.eth.account.from_key("0xYourPrivateKey")

def decode_input(input_data):
    return input_data[:10] in [
        "0x04e45aaf",  # exactInputSingle
        "0x5023b4df",  # exactOutputSingle
    ]

async def main():
    print("🔍 Listening for mempool swaps on Polygon...")
    sub = await w3.eth.subscribe('newPendingTransactions')
    async for tx_hash in sub:
        try:
            tx = w3.eth.get_transaction(tx_hash)
            if tx['to'] and tx['to'].lower() == POOL_ADDRESS.lower():
                if decode_input(tx.input):
                    print(f"🚨 Swap detected: {tx_hash.hex()}")
                    tx_data = contract.functions.requestFlashLoan(TOKEN, AMOUNT).build_transaction({
                        'from': account.address,
                        'nonce': w3.eth.get_transaction_count(account.address),
                        'gas': 800000,
                        'gasPrice': w3.toWei('80', 'gwei')
                    })
                    signed_tx = w3.eth.account.sign_transaction(tx_data, private_key=account.key)
                    tx_hash = w3.eth.send_raw_transaction(signed_tx.rawTransaction)
                    print(f"🚀 Triggered flash loan tx: {tx_hash.hex()}")
        except Exception as e:
            print(f"[WARN] {e}")

asyncio.run(main())
