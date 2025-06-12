import requests
import json
import time
import asyncio
import websockets
import ssl
from web3 import Web3
from eth_account import Account
import os

# Configuration
BLOXROUTE_AUTH_HEADER = "YOUR_BLOXROUTE_AUTH_HEADER"  # Replace with your auth header
BLOXROUTE_WS_URI = "wss://api.blxrbdn.com/ws"
SIMULATION_API_URL = "https://api.blxrbdn.com/eth/bundle/simulate"
BUNDLE_SUBMIT_URL = "https://api.blxrbdn.com/eth/v1/bundle"
RPC_URL = "https://eth-mainnet.g.alchemy.com/v2/YOUR_API_KEY"  # Replace with your RPC URL
PRIVATE_KEY = os.environ.get("PRIVATE_KEY", "0x" + "1" * 64)  # Use env var or dummy key

# Contract addresses
POSITION_MANAGER_ADDRESS = "0xC36442b4a4522E871399CD717aBDD847Ab11FE88"
UNISWAP_V3_ROUTER = "0xE592427A0AEce92De3Edee1F18E0157C05861564"
WETH_ADDRESS = "0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2"
USDC_ADDRESS = "0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48"
WETH_USDC_POOL = "0x8ad599c3A0ff1De082011EFDDc58f1908eb6e6D8"  # 0.3% fee tier
POOL_FEE = 3000  # 0.3%

# Initialize Web3
w3 = Web3(Web3.HTTPProvider(RPC_URL))
account = Account.from_key(PRIVATE_KEY)
address = account.address

# ABIs
POSITION_MANAGER_ABI = [
    {
        "inputs": [
            {
                "components": [
                    {"name": "token0", "type": "address"},
                    {"name": "token1", "type": "address"},
                    {"name": "fee", "type": "uint24"},
                    {"name": "tickLower", "type": "int24"},
                    {"name": "tickUpper", "type": "int24"},
                    {"name": "amount0Desired", "type": "uint256"},
                    {"name": "amount1Desired", "type": "uint256"},
                    {"name": "amount0Min", "type": "uint256"},
                    {"name": "amount1Min", "type": "uint256"},
                    {"name": "recipient", "type": "address"},
                    {"name": "deadline", "type": "uint256"}
                ],
                "name": "params",
                "type": "tuple"
            }
        ],
        "name": "mint",
        "outputs": [
            {"name": "tokenId", "type": "uint256"},
            {"name": "liquidity", "type": "uint128"},
            {"name": "amount0", "type": "uint256"},
            {"name": "amount1", "type": "uint256"}
        ],
        "stateMutability": "payable",
        "type": "function"
    },
    {
        "inputs": [
            {
                "components": [
                    {"name": "tokenId", "type": "uint256"},
                    {"name": "liquidity", "type": "uint128"},
                    {"name": "amount0Min", "type": "uint256"},
                    {"name": "amount1Min", "type": "uint256"},
                    {"name": "deadline", "type": "uint256"}
                ],
                "name": "params",
                "type": "tuple"
            }
        ],
        "name": "decreaseLiquidity",
        "outputs": [
            {"name": "amount0", "type": "uint256"},
            {"name": "amount1", "type": "uint256"}
        ],
        "stateMutability": "payable",
        "type": "function"
    },
    {
        "inputs": [
            {
                "components": [
                    {"name": "tokenId", "type": "uint256"},
                    {"name": "recipient", "type": "address"},
                    {"name": "amount0Max", "type": "uint128"},
                    {"name": "amount1Max", "type": "uint128"}
                ],
                "name": "params",
                "type": "tuple"
            }
        ],
        "name": "collect",
        "outputs": [
            {"name": "amount0", "type": "uint256"},
            {"name": "amount1", "type": "uint256"}
        ],
        "stateMutability": "payable",
        "type": "function"
    },
    {
        "inputs": [{"name": "tokenId", "type": "uint256"}],
        "name": "positions",
        "outputs": [
            {"name": "nonce", "type": "uint96"},
            {"name": "operator", "type": "address"},
            {"name": "token0", "type": "address"},
            {"name": "token1", "type": "address"},
            {"name": "fee", "type": "uint24"},
            {"name": "tickLower", "type": "int24"},
            {"name": "tickUpper", "type": "int24"},
            {"name": "liquidity", "type": "uint128"},
            {"name": "feeGrowthInside0LastX128", "type": "uint256"},
            {"name": "feeGrowthInside1LastX128", "type": "uint256"},
            {"name": "tokensOwed0", "type": "uint128"},
            {"name": "tokensOwed1", "type": "uint128"}
        ],
        "stateMutability": "view",
        "type": "function"
    }
]

POOL_ABI = [
    {
        "inputs": [],
        "name": "slot0",
        "outputs": [
            {"name": "sqrtPriceX96", "type": "uint160"},
            {"name": "tick", "type": "int24"},
            {"name": "observationIndex", "type": "uint16"},
            {"name": "observationCardinality", "type": "uint16"},
            {"name": "observationCardinalityNext", "type": "uint16"},
            {"name": "feeProtocol", "type": "uint8"},
            {"name": "unlocked", "type": "bool"}
        ],
        "stateMutability": "view",
        "type": "function"
    }
]

ERC20_ABI = [
    {
        "inputs": [
            {"name": "spender", "type": "address"},
            {"name": "amount", "type": "uint256"}
        ],
        "name": "approve",
        "outputs": [{"name": "", "type": "bool"}],
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "inputs": [{"name": "account", "type": "address"}],
        "name": "balanceOf",
        "outputs": [{"name": "", "type": "uint256"}],
        "stateMutability": "view",
        "type": "function"
    }
]

# Create contract instances
position_manager = w3.eth.contract(address=POSITION_MANAGER_ADDRESS, abi=POSITION_MANAGER_ABI)
pool = w3.eth.contract(address=WETH_USDC_POOL, abi=POOL_ABI)
weth = w3.eth.contract(address=WETH_ADDRESS, abi=ERC20_ABI)
usdc = w3.eth.contract(address=USDC_ADDRESS, abi=ERC20_ABI)

# Global variable to store the token ID of the last minted position
current_token_id = None

# Monitor mempool for swap transactions
async def monitor_mempool():
    ssl_context = ssl.create_default_context()
    ssl_context.check_hostname = False
    ssl_context.verify_mode = ssl.CERT_NONE

    async with websockets.connect(
        BLOXROUTE_WS_URI,
        extra_headers={"Authorization": BLOXROUTE_AUTH_HEADER},
        ssl=ssl_context
    ) as websocket:
        # Subscribe to pending transactions targeting Uniswap router
        subscribe_request = {
            "id": 1,
            "method": "subscribe",
            "params": [
                "pendingTxs",
                {
                    "include": ["tx_hash", "raw_tx", "tx_contents"],
                    "filters": f"to = '{UNISWAP_V3_ROUTER}'"
                }
            ]
        }

        await websocket.send(json.dumps(subscribe_request))
        response = await websocket.recv()
        print(f"Subscription response: {response}")

        while True:
            try:
                message = await websocket.recv()
                tx_data = json.loads(message)
                
                if "params" in tx_data and "result" in tx_data["params"]:
                    swap_tx = tx_data["params"]["result"]
                    
                    # Check if this is a large swap transaction we want to target
                    if is_large_swap(swap_tx):
                        print(f"Found large swap transaction: {swap_tx['txHash']}")
                        
                        # Create and execute JIT LP bundle
                        await create_jitlp_bundle(swap_tx)
            except Exception as e:
                print(f"Error in mempool monitoring: {e}")
                await asyncio.sleep(1)

# Check if transaction is a large swap we want to target
def is_large_swap(tx_data):
    # Extract transaction details
    tx_contents = tx_data.get("txContents", {})
    input_data = tx_contents.get("input", "")
    
    # Check for exactInputSingle function signature (0x414bf389)
    if input_data.startswith("0x414bf389"):
        try:
            # Check if it's a large swap (> 10 ETH or equivalent)
            value = int(tx_contents.get("value", "0"), 16)
            gas_price = int(tx_contents.get("gasPrice", "0"), 16)
            
            # If it's a large swap or high gas price (indicating urgency)
            if value > w3.to_wei(10, 'ether') or gas_price > w3.to_wei(100, 'gwei'):
                return True
        except Exception as e:
            print(f"Error parsing swap: {e}")
    
    return False

# Create and execute a JIT LP bundle with the swap transaction
async def create_jitlp_bundle(swap_tx):
    # Get the raw transaction
    swap_raw_tx = swap_tx.get("rawTx")
    
    # Get current tick from the pool
    slot0 = pool.functions.slot0().call()
    current_tick = slot0[1]
    
    # Calculate tick range for concentrated liquidity
    tick_spacing = 60  # 0.3% pool has 60 tick spacing
    
    # Determine if swap is buying or selling WETH (simplified)
    # In a real implementation, you'd decode the swap data to determine direction
    is_buying_weth = True  # Assume buying WETH for this example
    
    if is_buying_weth:
        # If buying WETH (USDC → WETH), place liquidity above current price
        tick_lower = current_tick
        tick_upper = current_tick + (tick_spacing * 5)  # 5 tick spaces above
        
        # Provide WETH liquidity
        amount0 = w3.to_wei(50, 'ether')  # 50 ETH
        amount1 = 0
    else:
        # If selling WETH (WETH → USDC), place liquidity below current price
        tick_lower = current_tick - (tick_spacing * 5)  # 5 tick spaces below
        tick_upper = current_tick
        
        # Provide USDC liquidity
        amount0 = 0
        amount1 = 100_000 * 10**6  # 100,000 USDC
    
    # Round to nearest tick spacing
    tick_lower = (tick_lower // tick_spacing) * tick_spacing
    tick_upper = (tick_upper // tick_spacing) * tick_spacing
    
    # 1. Create approve transactions
    approve_txs = create_approve_txs(amount0, amount1)
    
    # 2. Create add liquidity transaction
    add_liquidity_tx = create_add_liquidity_tx(tick_lower, tick_upper, amount0, amount1)
    
    # 3. User's swap transaction from mempool
    
    # 4. Create remove liquidity transaction
    remove_liquidity_tx = create_remove_liquidity_tx()
    
    # Create bundle with approve + add liquidity + swap + remove liquidity
    bundle = []
    
    # Add approve transactions
    for tx in approve_txs:
        bundle.append({"transaction": tx, "canRevert": False})
    
    # Add main transactions
    bundle.extend([
        {"transaction": add_liquidity_tx, "canRevert": False},
        {"transaction": swap_raw_tx, "canRevert": False},
        {"transaction": remove_liquidity_tx, "canRevert": False}
    ])
    
    # Simulate bundle
    simulation_result = simulate_bundle(bundle)
    
    # If profitable, submit the bundle
    if is_profitable(simulation_result):
        # Extract just the transaction hex strings
        tx_list = [item["transaction"] for item in bundle]
        submit_bundle(tx_list)

# Create approve transactions for WETH and USDC
def create_approve_txs(amount0, amount1):
    txs = []
    
    # Approve WETH if needed
    if amount0 > 0:
        tx = weth.functions.approve(
            POSITION_MANAGER_ADDRESS,
            amount0
        ).build_transaction({
            'from': address,
            'nonce': w3.eth.get_transaction_count(address),
            'gas': 100_000,
            'gasPrice': w3.eth.gas_price * 2,
            'chainId': 1
        })
        
        signed_tx = w3.eth.account.sign_transaction(tx, PRIVATE_KEY)
        txs.append(w3.to_hex(signed_tx.rawTransaction))
    
    # Approve USDC if needed
    if amount1 > 0:
        tx = usdc.functions.approve(
            POSITION_MANAGER_ADDRESS,
            amount1
        ).build_transaction({
            'from': address,
            'nonce': w3.eth.get_transaction_count(address) + (1 if amount0 > 0 else 0),
            'gas': 100_000,
            'gasPrice': w3.eth.gas_price * 2,
            'chainId': 1
        })
        
        signed_tx = w3.eth.account.sign_transaction(tx, PRIVATE_KEY)
        txs.append(w3.to_hex(signed_tx.rawTransaction))
    
    return txs

# Create add liquidity transaction
def create_add_liquidity_tx(tick_lower, tick_upper, amount0, amount1):
    global current_token_id
    
    # Calculate nonce based on previous transactions
    nonce_offset = 0
    if amount0 > 0:
        nonce_offset += 1
    if amount1 > 0:
        nonce_offset += 1
    
    nonce = w3.eth.get_transaction_count(address) + nonce_offset
    
    # Create mint params
    mint_params = {
        'token0': WETH_ADDRESS,
        'token1': USDC_ADDRESS,
        'fee': POOL_FEE,
        'tickLower': tick_lower,
        'tickUpper': tick_upper,
        'amount0Desired': amount0,
        'amount1Desired': amount1,
        'amount0Min': 0,
        'amount1Min': 0,
        'recipient': address,
        'deadline': w3.eth.get_block('latest').timestamp + 300
    }
    
    # Create transaction to mint position
    tx = position_manager.functions.mint(
        mint_params
    ).build_transaction({
        'from': address,
        'nonce': nonce,
        'gas': 500_000,
        'gasPrice': w3.eth.gas_price * 2,
        'chainId': 1,
        'value': 0
    })
    
    # Sign transaction
    signed_tx = w3.eth.account.sign_transaction(tx, PRIVATE_KEY)
    
    # Store expected token ID (this is an estimate - in production you'd track this more carefully)
    # In a real implementation, you'd need to track the actual token ID from the transaction receipt
    current_token_id = get_next_token_id()
    
    return w3.to_hex(signed_tx.rawTransaction)

# Create remove liquidity transaction
def create_remove_liquidity_tx():
    global current_token_id
    
    if current_token_id is None:
        raise ValueError("No token ID available - position hasn't been minted yet")
    
    # Calculate nonce based on previous transactions
    nonce = w3.eth.get_transaction_count(address) + 3  # Approve WETH + Approve USDC + Mint
    
    # First create decreaseLiquidity transaction
    # We need to get the liquidity amount, but since the position doesn't exist yet,
    # we'll use the maximum uint128 value to ensure we remove all liquidity
    max_uint128 = 2**128 - 1
    
    decrease_params = {
        'tokenId': current_token_id,
        'liquidity': max_uint128,
        'amount0Min': 0,
        'amount1Min': 0,
        'deadline': w3.eth.get_block('latest').timestamp + 300
    }
    
    tx = position_manager.functions.decreaseLiquidity(
        decrease_params
    ).build_transaction({
        'from': address,
        'nonce': nonce,
        'gas': 300_000,
        'gasPrice': w3.eth.gas_price * 2,
        'chainId': 1,
        'value': 0
    })
    
    # Sign transaction
    signed_tx = w3.eth.account.sign_transaction(tx, PRIVATE_KEY)
    decrease_tx = w3.to_hex(signed_tx.rawTransaction)
    
    # Then create collect transaction
    collect_params = {
        'tokenId': current_token_id,
        'recipient': address,
        'amount0Max': max_uint128,
        'amount1Max': max_uint128
    }
    
    tx = position_manager.functions.collect(
        collect_params
    ).build_transaction({
        'from': address,
        'nonce': nonce + 1,  # Increment nonce
        'gas': 200_000,
        'gasPrice': w3.eth.gas_price * 2,
        'chainId': 1,
        'value': 0
    })
    
    # Sign transaction
    signed_tx = w3.eth.account.sign_transaction(tx, PRIVATE_KEY)
    collect_tx = w3.to_hex(signed_tx.rawTransaction)
    
    # Return the collect transaction (which will be executed after decreaseLiquidity)
    # In a real implementation, you'd include both transactions in the bundle
    return collect_tx

# Get the next token ID (simplified - in production you'd track this more carefully)
def get_next_token_id():
    # This is a simplified approach - in production you'd need to track your positions
    # or query the contract for the actual token ID
    return 12345  # Placeholder

# Simulate bundle using bloxroute API
def simulate_bundle(bundle):
    headers = {
        "Content-Type": "application/json",
        "Authorization": BLOXROUTE_AUTH_HEADER
    }
    
    payload = {
        "transactions": bundle,
        "blockNumber": "latest",
        "stateBlockNumber": "latest",
        "timestamp": int(time.time())
    }
    
    response = requests.post(
        SIMULATION_API_URL,
        headers=headers,
        data=json.dumps(payload)
    )
    
    return response.json()

# Check if bundle is profitable
def is_profitable(simulation_result):
    print(f"Simulation result: {json.dumps(simulation_result, indent=2)}")
    
    if "profit" in simulation_result:
        profit = float(simulation_result["profit"])
        gas_cost = float(simulation_result.get("gasUsed", 0)) * float(w3.eth.gas_price) / 10**18
        net_profit = profit - gas_cost
        
        print(f"Simulated profit: {profit} ETH")
        print(f"Gas cost: {gas_cost} ETH")
        print(f"Net profit: {net_profit} ETH")
        
        return net_profit > 0.01  # At least 0.01 ETH profit
    
    return False

# Submit bundle to bloxroute
def submit_bundle(transactions):
    headers = {
        "Content-Type": "application/json",
        "Authorization": BLOXROUTE_AUTH_HEADER
    }
    
    payload = {
        "transactions": transactions,
        "replacementUuid": "",
        "frontrunningProtection": False
    }
    
    response = requests.post(
        BUNDLE_SUBMIT_URL,
        headers=headers,
        data=json.dumps(payload)
    )
    
    result = response.json()
    print(f"Bundle submission result: {result}")
    return result

# Main function
def main():
    print("Starting mempool monitoring for JIT LP opportunities...")
    asyncio.run(monitor_mempool())

if __name__ == "__main__":
    main()