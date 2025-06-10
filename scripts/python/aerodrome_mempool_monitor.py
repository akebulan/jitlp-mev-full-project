# aerodrome_polling_monitor.py

from web3 import Web3
import time

AERODROME_ROUTER = '0x1eC72d0483c478eAcD5a63a836618a4389F627A5'.lower()

SWAP_FUNCTIONS = {
    "0x38ed1739": "swapExactTokensForTokens",
    "0x18cbafe5": "swapExactETHForTokens",
    "0x7ff36ab5": "swapETHForExactTokens",
    "0x5c11d795": "swapExactTokensForETH"
}

QUICKNODE_HTTP = 'https://stylish-red-wildflower.base-mainnet.quiknode.pro/d2df1554392e6deea8124dc6a19434b49bf0a53b/'
w3 = Web3(Web3.HTTPProvider(QUICKNODE_HTTP))

seen = set()

print("🔁 Polling for Aerodrome swaps on Base...")

while True:
    try:
        pending = w3.manager.request_blocking("eth_pendingTransactions", [])
        for tx in pending:
            tx_hash = tx.get("hash")
            if not tx_hash or tx_hash in seen:
                continue
            seen.add(tx_hash)

            to = tx.get("to")
            if to and to.lower() == AERODROME_ROUTER:
                method_id = tx["input"][:10]
                if method_id in SWAP_FUNCTIONS:
                    print(f"🚨 Aerodrome Swap: {tx_hash}")
                    print(f"    Method: {SWAP_FUNCTIONS[method_id]}")
                    print(f"    From: {tx['from']}")
                    print(f"    Gas: {tx['gas']}, GasPrice: {tx['gasPrice']}")
                    print("")
    except Exception as e:
        print(f"[ERROR] {e}")

    time.sleep(2)
