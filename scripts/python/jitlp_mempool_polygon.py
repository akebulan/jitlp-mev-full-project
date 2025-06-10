from web3 import Web3
from eth_account import Account
from flashbots import flashbot
from eth_account.signers.local import LocalAccount

# RPC URL (use a Polygon-compatible Flashbots relay or node)
POLYGON_RPC = "https://polygon-mainnet.infura.io/v3/YOUR_INFURA_KEY"
w3 = Web3(Web3.HTTPProvider(POLYGON_RPC))

# Load private keys
searcher_account: LocalAccount = Account.from_key("YOUR_SEARCHER_PRIVATE_KEY")
auth_account = Account.create()  # Ephemeral auth signer

# Inject Flashbots middleware
flashbot(w3, auth_account)

# Example placeholder transactions (already signed)
signed_tx1 = w3.eth.account.sign_transaction({
    "to": "0xUniswapV3PoolAddress",
    "value": 0,
    "gas": 250000,
    "gasPrice": w3.to_wei("100", "gwei"),
    "nonce": w3.eth.get_transaction_count(searcher_account.address),
    "data": "0x...",  # LP Mint
    "chainId": 137
}, searcher_account.key)

signed_tx2 = w3.eth.account.sign_transaction({
    "to": "0xRouterAddress",
    "value": 0,
    "gas": 250000,
    "gasPrice": w3.to_wei("100", "gwei"),
    "nonce": w3.eth.get_transaction_count(searcher_account.address) + 1,
    "data": "0x...",  # User Swap
    "chainId": 137
}, searcher_account.key)

signed_tx3 = w3.eth.account.sign_transaction({
    "to": "0xUniswapV3PoolAddress",
    "value": 0,
    "gas": 250000,
    "gasPrice": w3.to_wei("100", "gwei"),
    "nonce": w3.eth.get_transaction_count(searcher_account.address) + 2,
    "data": "0x...",  # LP Burn + Collect
    "chainId": 137
}, searcher_account.key)

# Bundle and simulate
bundle = [
    {'signed_transaction': signed_tx1.rawTransaction},
    {'signed_transaction': signed_tx2.rawTransaction},
    {'signed_transaction': signed_tx3.rawTransaction}
]

block = w3.eth.block_number + 1
print("Simulating bundle...")
sim_result = w3.flashbots.simulate(bundle, block)

if "error" in sim_result:
    print("❌ Simulation failed:", sim_result["error"])
else:
    print("✅ Simulation successful")
    print("Sending bundle to Flashbots relay...")

    send_result = w3.flashbots.send_bundle(bundle, target_block_number=block)
    print("Bundle sent:", send_result)
