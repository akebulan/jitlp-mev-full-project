import asyncio, json, ssl, websockets
import datetime


# Set minimum USDC value threshold (in USD)
MIN_USDC_VALUE = 1000  # Only show transactions with USDC value >= $1000

async def main():
    
    uri = "wss://api.blxrbdn.com/ws"
    # uri = "wss://virginia.polygon.blxrbdn.com/ws"
    # Introductory tier users should follow
    # uri="wss://api.blxrbdn.com/ws"
    headers_auth_key = "MTAzYWY1MjQtMDIwNC00OTNhLTk3NmItMWU4MTQ4ZGUxMDg0OmQwN2Q0MDQyZjI2NzY1ZDdhYTAwMTc0YjM0NDVlY2E3"

    ssl_context = ssl.create_default_context(purpose=ssl.Purpose.SERVER_AUTH)
    ssl_context.check_hostname = False
    ssl_context.verify_mode = ssl.CERT_NONE

    async with websockets.connect(
            uri,
            additional_headers={"Authorization": headers_auth_key},
            ssl=ssl_context
    ) as websocket:

        # Define token addresses
        USDC_ADDRESS = "0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48"
        
        # Router addresses
        routers = [
            "0x7a250d5630b4cf539739df2c5dacb4c659f2488d",  # Uniswap V2
            "0xe592427a0aece92de3edee1f18e0157c05861564",  # Uniswap V3
            "0xd9e1ce17f2641f24ae83637ab66a2cca9c378b9f",  # SushiSwap
            "0xba12222222228d8ba445958a75a0704d566bf2c8",  # Balancer V2
            "0xa5E0829CaCEd8fFDD4De3c43696c57F7D7A678ff",  # QuickSwap
            "0x1b02da8cb0d097eb8d57a175b88c7d8b47997506"   # Sushi
        ]
        
        # Create the subscription request
        subscribe_request = {
            "id": 1,
            "method": "subscribe",
            "params": [
                "pendingTxs",
                {
                    "include": ["tx_hash", "raw_tx", "tx_contents"],
                    "filters": f"to in [{', '.join(routers)}] AND ({'value'} > 1000000000000000000)",
                    # "blockchain_network": "Polygon-Mainnet"
                }
            ]
        }

        await websocket.send(json.dumps(subscribe_request))
        response = await websocket.recv()
        data = json.loads(response)

        if "error" in data:
            print("❌ Subscription error:", data["error"])
            return

        subscription_id = json.loads(response)["result"]
        print(f"Subscribed successfully with subscription_id {subscription_id}")

        while True:
            try:
                next_notification = await websocket.recv()
                tx_data = json.loads(next_notification)
                process_transaction(tx_data)
            except websockets.exceptions.ConnectionClosedError:
                print("Connection closed unexpectedly")

def process_transaction(tx_data):
    # Define common token addresses and symbols
    USDC_ADDRESS = "0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48".lower()
    WETH_ADDRESS = "0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2".lower()
    WBTC_ADDRESS = "0x2260fac5e5542a773aa44fbcfedf7c193bc2c599".lower()
    
    # Set to True to only show WBTC/USDC pairs
    FILTER_WBTC_USDC_ONLY = True
    
    # Common token symbols
    TOKEN_SYMBOLS = {
        USDC_ADDRESS: "USDC",
        WETH_ADDRESS: "WETH",
        "0xdac17f958d2ee523a2206206994597c13d831ec7".lower(): "USDT",
        "0x6b175474e89094c44da98b954eedeac495271d0f".lower(): "DAI",
        "0x2260fac5e5542a773aa44fbcfedf7c193bc2c599".lower(): "WBTC",
        "0x1f9840a85d5af5bf1d1762f925bdaddc4201f984".lower(): "UNI",
        "0x514910771af9ca656af840dff83e8264ecf986ca".lower(): "LINK",
        "0x255debf33bf6ff42668754cadb7b5ee708def9e5".lower(): "FRAX"
    }
    
    # Function to get token symbol
    def get_token_symbol(address):
        if address.lower() in TOKEN_SYMBOLS:
            return TOKEN_SYMBOLS[address.lower()]
        
        # Try to fetch token symbol from Etherscan API if not in our dictionary
        try:
            # This is a simplified example - in production you'd use an actual API call
            # For now, just return the shortened address
            return address[:6] + "..."
        except:
            return address[:6] + "..."
    
    if "params" in tx_data and "result" in tx_data["params"]:
        result = tx_data["params"]["result"]
        print(f"[{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] result: {result}")
        tx_contents = result.get("txContents", "Unknown")
        to = tx_contents.get("to", "Unknown")
        raw_tx = result.get("rawTx", "Unknown")

        # Parse input data to get token details
        input_data = tx_contents.get("input", "")

        # Common function signatures for swaps
        swap_sigs = {
            # Uniswap V2 swapExactTokensForTokens
            "0x38ed1739": {
                "amountIn_pos": 1,
                "amountOutMin_pos": 2,
                "path_pos": 3
            },
            # Uniswap V3 exactInputSingle
            "0x414bf389": {
                "tokenIn_pos": 1,
                "tokenOut_pos": 2,
                "amountIn_pos": 3
            },
            # Uniswap V2 swapExactETHForTokens
            "0x7ff36ab5": {
                "amountOutMin_pos": 1,
                "path_pos": 2
            },
            # Uniswap V2 swapTokensForExactTokens
            "0x8803dbee": {
                "amountOut_pos": 1,
                "amountInMax_pos": 2,
                "path_pos": 3
            },
            # Uniswap V2 swapExactTokensForETH
            "0x18cbafe5": {
                "amountIn_pos": 1,
                "amountOutMin_pos": 2,
                "path_pos": 3
            },
            # Uniswap V2 swapETHForExactTokens
            "0xfb3bdb41": {
                "amountOut_pos": 1,
                "path_pos": 2
            },
            # Uniswap V3 swapExactTokensForTokens
            "0x791ac947": {
                "amountIn_pos": 1,
                "amountOutMin_pos": 2,
                "path_pos": 3
            },
            # Uniswap V3 swapExactETHForTokens
            "0xb6f9de95": {
                "amountOutMin_pos": 1,
                "path_pos": 2
            }
        }

        # Get first 10 chars of input (function signature)
        func_sig = input_data[:10] if len(input_data) >= 10 else ""

        if func_sig in swap_sigs:
            # Parse based on function signature
            try:
                # Extract token addresses and amounts from input data using web3 ABI decoding
                from web3 import Web3
                from eth_abi.codec import ABICodec
                from eth_abi.registry import registry
                
                # Create an ABICodec instance for decoding
                codec = ABICodec(registry)
                
                # Define a decode_abi function
                def decode_abi(types, data):
                    return codec.decode(types, data)
                
                # Function to calculate pair address
                def get_pair_address(token_a, token_b, factory_address="0x5C69bEe701ef814a2B6a3EDD4B1652CB9cc5aA6f", 
                                    init_code_hash="0x96e8ac4277198ff8b6f785478aa9a39f403cb768dd02cbee326c3e7da348845f"):
                    # Sort tokens (required by Uniswap V2)
                    token0 = min(token_a, token_b, key=lambda x: x.lower())
                    token1 = max(token_a, token_b, key=lambda x: x.lower())
                    
                    # Create salt from the sorted token addresses
                    salt = Web3.solidity_keccak(
                        ['address', 'address'],
                        [Web3.to_checksum_address(token0), Web3.to_checksum_address(token1)]
                    )
                    
                    # Calculate pair address using CREATE2
                    pair_address = Web3.to_checksum_address(
                        Web3.solidity_keccak(
                            ['bytes1', 'address', 'bytes32', 'bytes32'],
                            [b'\xff', Web3.to_checksum_address(factory_address), salt, init_code_hash]
                        )[12:]
                    )
                    
                    return pair_address

                # Remove 0x and function signature to get parameters
                input_params = input_data[10:]

                if func_sig == "0x38ed1739": # swapExactTokensForTokens
                    # Define parameter types for decoding
                    param_types = ['uint256', 'uint256', 'address[]', 'address', 'uint256']
                    try:
                        decoded = decode_abi(param_types, bytes.fromhex(input_params))
                        amount_in = decoded[0]
                        amount_out_min = decoded[1]
                        path = decoded[2]
                        to_address = decoded[3]
                        deadline = decoded[4]

                        # Check if this is a WBTC/USDC pair
                        is_wbtc_usdc_pair = (
                            (WBTC_ADDRESS in [addr.lower() for addr in path]) and
                            (USDC_ADDRESS in [addr.lower() for addr in path])
                        )
                        
                        # Only continue if it passes our filter
                        if not FILTER_WBTC_USDC_ONLY or is_wbtc_usdc_pair:
                            input_token = get_token_symbol(path[0])
                            output_token = get_token_symbol(path[-1])
                            input_amount = Web3.from_wei(amount_in, 'ether')
                            output_amount = Web3.from_wei(amount_out_min, 'ether')
                            
                            # Estimate USD value (using approximate prices)
                            usd_value = 0
                            if path[0].lower() == WETH_ADDRESS:
                                usd_value = input_amount * 3500  # Approximate ETH price
                            elif path[0].lower() == USDC_ADDRESS:
                                usd_value = Web3.from_wei(amount_in, 'mwei')  # USDC has 6 decimals
                            
                            print(f"Swap Details:")
                            print(f"Amount In: {input_amount} {input_token}")
                            print(f"Min Amount Out: {output_amount} {output_token}")
                            print(f"Token Path: {[get_token_symbol(addr) for addr in path]}")
                            if usd_value > 0:
                                print(f"Total Value: ~${usd_value:.2f}")
                        
                        # Calculate USDC value for display
                        for i, addr in enumerate(path):
                            if addr.lower() == USDC_ADDRESS:
                                if i == 0:
                                    print(f"USDC Value: ${Web3.from_wei(amount_in, 'mwei'):,.2f}")
                                elif i == len(path) - 1:
                                    print(f"USDC Value: ${Web3.from_wei(amount_out_min, 'mwei'):,.2f}")
                        
                        # Calculate and display pair addresses for each hop in the path
                        for i in range(len(path) - 1):
                            pair_address = get_pair_address(path[i], path[i+1])
                            print(f"Pair Address ({path[i][:6]}.../{path[i+1][:6]}...): {pair_address}")
                            
                        print(f"To Address: {to_address}")
                        # Handle large timestamps safely
                        try:
                            print(f"Deadline: {datetime.datetime.fromtimestamp(deadline)}")
                        except (ValueError, OverflowError):
                            print(f"Deadline (raw): {deadline}")

                    except Exception as e:
                        print(f"Error decoding swapExactTokensForTokens: {e}")

                elif func_sig == "0x414bf389": # exactInputSingle
                    # Define parameter types for V3 single swap
                    param_types = ['address', 'address', 'uint24', 'address', 'uint256', 'uint256', 'uint160']
                    try:
                        decoded = decode_abi(param_types, bytes.fromhex(input_params))
                        token_in = decoded[0]
                        token_out = decoded[1]
                        fee = decoded[2]
                        recipient = decoded[3]
                        amount_in = decoded[4]
                        amount_out_min = decoded[5]
                        sqrt_price_limit = decoded[6]

                        print(f"V3 Exact Input Single Swap Details:")
                        print(f"Token In: {token_in}")
                        print(f"Token Out: {token_out}")
                        print(f"Fee Tier: {fee/10000}%")
                        print(f"Recipient: {recipient}")
                        print(f"Amount In: {Web3.from_wei(amount_in, 'ether')} tokens")
                        print(f"Min Amount Out: {Web3.from_wei(amount_out_min, 'ether')} tokens")
                        print(f"Sqrt Price Limit: {sqrt_price_limit}")
                        
                        # Calculate USDC value for display
                        if token_in.lower() == USDC_ADDRESS:
                            print(f"USDC Value: ${Web3.from_wei(amount_in, 'mwei'):,.2f}")
                        elif token_out.lower() == USDC_ADDRESS:
                            print(f"USDC Value: ${Web3.from_wei(amount_out_min, 'mwei'):,.2f}")

                    except Exception as e:
                        print(f"Error decoding exactInputSingle: {e}")
                        
                elif func_sig == "0x7ff36ab5": # swapExactETHForTokens
                    param_types = ['uint256', 'address[]', 'address', 'uint256']
                    try:
                        decoded = decode_abi(param_types, bytes.fromhex(input_params))
                        amount_out_min = decoded[0]
                        path = decoded[1]
                        to_address = decoded[2]
                        deadline = decoded[3]
                        
                        eth_value = Web3.from_wei(int(tx_contents.get('value', '0'), 16), 'ether')
                        output_token = get_token_symbol(path[1])
                        
                        print(f"SwapExactETHForTokens Details:")
                        print(f"Min Amount Out: {Web3.from_wei(amount_out_min, 'ether')} {output_token}")
                        print(f"Token Path: {[get_token_symbol(addr) for addr in path]}")
                        print(f"To Address: {to_address}")
                        # Handle large timestamps safely
                        try:
                            print(f"Deadline: {datetime.datetime.fromtimestamp(deadline)}")
                        except (ValueError, OverflowError):
                            print(f"Deadline (raw): {deadline}")
                        print(f"ETH Value: {eth_value} ETH (${eth_value * 3500:.2f})")
                        
                        # Calculate USDC value for display
                        for i, addr in enumerate(path):
                            if addr.lower() == USDC_ADDRESS and i == len(path) - 1:
                                print(f"USDC Value: ${Web3.from_wei(amount_out_min, 'mwei'):,.2f}")
                        
                        # Calculate and display pair addresses for each hop in the path
                        for i in range(len(path) - 1):
                            pair_address = get_pair_address(path[i], path[i+1])
                            print(f"Pair Address ({path[i][:6]}.../{path[i+1][:6]}...): {pair_address}")
                        
                    except Exception as e:
                        print(f"Error decoding swapExactETHForTokens: {e}")
                        
                elif func_sig == "0x8803dbee": # swapTokensForExactTokens
                    param_types = ['uint256', 'uint256', 'address[]', 'address', 'uint256']
                    try:
                        decoded = decode_abi(param_types, bytes.fromhex(input_params))
                        amount_out = decoded[0]
                        amount_in_max = decoded[1]
                        path = decoded[2]
                        to_address = decoded[3]
                        deadline = decoded[4]
                        
                        print(f"SwapTokensForExactTokens Details:")
                        print(f"Exact Amount Out: {Web3.from_wei(amount_out, 'ether')} tokens")
                        print(f"Max Amount In: {Web3.from_wei(amount_in_max, 'ether')} tokens")
                        print(f"Token Path: {path}")
                        print(f"To Address: {to_address}")
                        # Handle large timestamps safely
                        try:
                            print(f"Deadline: {datetime.datetime.fromtimestamp(deadline)}")
                        except (ValueError, OverflowError):
                            print(f"Deadline (raw): {deadline}")
                        
                        # Calculate USDC value for display
                        for i, addr in enumerate(path):
                            if addr.lower() == USDC_ADDRESS:
                                if i == 0:
                                    print(f"USDC Value: ${Web3.from_wei(amount_in_max, 'mwei'):,.2f}")
                                elif i == len(path) - 1:
                                    print(f"USDC Value: ${Web3.from_wei(amount_out, 'mwei'):,.2f}")
                        
                        # Calculate and display pair addresses for each hop in the path
                        for i in range(len(path) - 1):
                            pair_address = get_pair_address(path[i], path[i+1])
                            print(f"Pair Address ({path[i][:6]}.../{path[i+1][:6]}...): {pair_address}")
                        
                    except Exception as e:
                        print(f"Error decoding swapTokensForExactTokens: {e}")
                        
                elif func_sig == "0x18cbafe5": # swapExactTokensForETH
                    param_types = ['uint256', 'uint256', 'address[]', 'address', 'uint256']
                    try:
                        decoded = decode_abi(param_types, bytes.fromhex(input_params))
                        amount_in = decoded[0]
                        amount_out_min = decoded[1]
                        path = decoded[2]
                        to_address = decoded[3]
                        deadline = decoded[4]
                        
                        print(f"SwapExactTokensForETH Details:")
                        print(f"Amount In: {Web3.from_wei(amount_in, 'ether')} tokens")
                        print(f"Min ETH Out: {Web3.from_wei(amount_out_min, 'ether')} ETH")
                        print(f"Token Path: {path}")
                        print(f"To Address: {to_address}")
                        # Handle large timestamps safely
                        try:
                            print(f"Deadline: {datetime.datetime.fromtimestamp(deadline)}")
                        except (ValueError, OverflowError):
                            print(f"Deadline (raw): {deadline}")
                        
                        # Calculate USDC value for display
                        for i, addr in enumerate(path):
                            if addr.lower() == USDC_ADDRESS and i == 0:
                                print(f"USDC Value: ${Web3.from_wei(amount_in, 'mwei'):,.2f}")
                        
                        # Calculate and display pair addresses for each hop in the path
                        for i in range(len(path) - 1):
                            pair_address = get_pair_address(path[i], path[i+1])
                            print(f"Pair Address ({path[i][:6]}.../{path[i+1][:6]}...): {pair_address}")
                        
                    except Exception as e:
                        print(f"Error decoding swapExactTokensForETH: {e}")
                        
                elif func_sig == "0xfb3bdb41": # swapETHForExactTokens
                    param_types = ['uint256', 'address[]', 'address', 'uint256']
                    try:
                        decoded = decode_abi(param_types, bytes.fromhex(input_params))
                        amount_out = decoded[0]
                        path = decoded[1]
                        to_address = decoded[2]
                        deadline = decoded[3]
                        
                        print(f"SwapETHForExactTokens Details:")
                        print(f"Exact Amount Out: {Web3.from_wei(amount_out, 'ether')} tokens")
                        print(f"Token Path: {path}")
                        print(f"To Address: {to_address}")
                        # Handle large timestamps safely
                        try:
                            print(f"Deadline: {datetime.datetime.fromtimestamp(deadline)}")
                        except (ValueError, OverflowError):
                            print(f"Deadline (raw): {deadline}")
                        print(f"ETH Value: {Web3.from_wei(int(tx_contents.get('value', '0'), 16), 'ether')} ETH")
                        
                        # Calculate USDC value for display
                        for i, addr in enumerate(path):
                            if addr.lower() == USDC_ADDRESS and i == len(path) - 1:
                                print(f"USDC Value: ${Web3.from_wei(amount_out, 'mwei'):,.2f}")
                        
                        # Calculate and display pair addresses for each hop in the path
                        for i in range(len(path) - 1):
                            pair_address = get_pair_address(path[i], path[i+1])
                            print(f"Pair Address ({path[i][:6]}.../{path[i+1][:6]}...): {pair_address}")
                        
                    except Exception as e:
                        print(f"Error decoding swapETHForExactTokens: {e}")
                        
                elif func_sig == "0x791ac947": # swapExactTokensForTokens (Uniswap V3)
                    # For Uniswap V3, the path is encoded differently
                    try:
                        # First try with the standard parameter types
                        param_types = ['uint256', 'uint256', 'bytes', 'address', 'uint256']
                        try:
                            decoded = decode_abi(param_types, bytes.fromhex(input_params))
                            amount_in = decoded[0]
                            amount_out_min = decoded[1]
                            path = decoded[2]  # This is encoded differently in V3
                            to_address = decoded[3]
                            deadline = decoded[4]
                            
                            print(f"V3 SwapExactTokensForTokens Details:")
                            print(f"Amount In: {Web3.from_wei(amount_in, 'ether')} tokens")
                            print(f"Min Amount Out: {Web3.from_wei(amount_out_min, 'ether')} tokens")
                            print(f"To Address: {to_address}")
                            # Handle large timestamps safely
                            try:
                                print(f"Deadline: {datetime.datetime.fromtimestamp(deadline)}")
                            except (ValueError, OverflowError):
                                print(f"Deadline (raw): {deadline}")
                        except Exception as e1:
                            # If that fails, try with an alternative format that some routers use
                            try:
                                param_types = ['uint256', 'uint256', 'address[]', 'address', 'uint256']
                                decoded = decode_abi(param_types, bytes.fromhex(input_params))
                                amount_in = decoded[0]
                                amount_out_min = decoded[1]
                                path = decoded[2]
                                to_address = decoded[3]
                                deadline = decoded[4]
                                
                                # Calculate USDC value
                                usdc_value = 0
                                for i, addr in enumerate(path):
                                    if addr.lower() == USDC_ADDRESS:
                                        if i == 0:
                                            usdc_value = Web3.from_wei(amount_in, 'mwei')  # USDC has 6 decimals
                                        elif i == len(path) - 1:
                                            usdc_value = Web3.from_wei(amount_out_min, 'mwei')  # USDC has 6 decimals
                                
                                # Check if this is a WBTC/USDC pair
                                is_wbtc_usdc_pair = (
                                    (WBTC_ADDRESS in [addr.lower() for addr in path]) and
                                    (USDC_ADDRESS in [addr.lower() for addr in path])
                                )
                                
                                # Only print details if it passes our filters
                                if (not FILTER_WBTC_USDC_ONLY or is_wbtc_usdc_pair) and (usdc_value >= MIN_USDC_VALUE or usdc_value == 0):
                                    input_token = get_token_symbol(path[0])
                                    output_token = get_token_symbol(path[-1])
                                    input_amount = Web3.from_wei(amount_in, 'ether')
                                    output_amount = Web3.from_wei(amount_out_min, 'ether')
                                    
                                    # Estimate USD value (using approximate prices)
                                    usd_value = 0
                                    if path[0].lower() == WETH_ADDRESS:
                                        usd_value = input_amount * 2700  # Approximate ETH price
                                    elif path[0].lower() == USDC_ADDRESS:
                                        usd_value = Web3.from_wei(amount_in, 'mwei')  # USDC has 6 decimals
                                    
                                    print(f"V3 SwapExactTokensForTokens Details (alt format):")
                                    print(f"Amount In: {input_amount} {input_token}")
                                    print(f"Min Amount Out: {output_amount} {output_token}")
                                    print(f"Token Path: {[get_token_symbol(addr) for addr in path]}")
                                    if usd_value > 0:
                                        print(f"Total Value: ~${usd_value:.2f}")
                                
                                    # Display USDC value if present
                                    if usdc_value > 0:
                                        print(f"USDC Value: ${usdc_value:,.2f}")
                                
                                # Calculate and display pair addresses for each hop in the path
                                for i in range(len(path) - 1):
                                    pair_address = get_pair_address(path[i], path[i+1])
                                    print(f"Pair Address ({path[i][:6]}.../{path[i+1][:6]}...): {pair_address}")
                                
                                print(f"To Address: {to_address}")
                                # Handle large timestamps safely
                                try:
                                    print(f"Deadline: {datetime.datetime.fromtimestamp(deadline)}")
                                except (ValueError, OverflowError):
                                    print(f"Deadline (raw): {deadline}")
                            except Exception as e2:
                                print(f"Error decoding V3 swapExactTokensForTokens: Primary: {e1}, Alternative: {e2}")
                                print(f"Raw input params: {input_params[:100]}...")
                    except Exception as e:
                        print(f"Error decoding V3 swapExactTokensForTokens: {e}")
                        
                elif func_sig == "0xb6f9de95": # swapExactETHForTokens (Uniswap V3)
                    try:
                        # First try with the standard parameter types
                        param_types = ['uint256', 'bytes', 'address', 'uint256']
                        try:
                            decoded = decode_abi(param_types, bytes.fromhex(input_params))
                            amount_out_min = decoded[0]
                            path = decoded[1]  # This is encoded differently in V3
                            to_address = decoded[2]
                            deadline = decoded[3]
                            
                            print(f"V3 SwapExactETHForTokens Details:")
                            print(f"Min Amount Out: {Web3.from_wei(amount_out_min, 'ether')} tokens")
                            print(f"To Address: {to_address}")
                            # Handle large timestamps safely
                            try:
                                print(f"Deadline: {datetime.datetime.fromtimestamp(deadline)}")
                            except (ValueError, OverflowError):
                                print(f"Deadline (raw): {deadline}")
                            print(f"ETH Value: {Web3.from_wei(int(tx_contents.get('value', '0'), 16), 'ether')} ETH")
                        except Exception as e1:
                            # If that fails, try with an alternative format that some routers use
                            try:
                                param_types = ['uint256', 'address[]', 'address', 'uint256']
                                decoded = decode_abi(param_types, bytes.fromhex(input_params))
                                amount_out_min = decoded[0]
                                path = decoded[1]
                                to_address = decoded[2]
                                deadline = decoded[3]
                                
                                print(f"V3 SwapExactETHForTokens Details (alt format):")
                                print(f"Min Amount Out: {Web3.from_wei(amount_out_min, 'ether')} tokens")
                                print(f"Token Path: {path}")
                                print(f"To Address: {to_address}")
                                # Handle large timestamps safely
                                try:
                                    print(f"Deadline: {datetime.datetime.fromtimestamp(deadline)}")
                                except (ValueError, OverflowError):
                                    print(f"Deadline (raw): {deadline}")
                                print(f"ETH Value: {Web3.from_wei(int(tx_contents.get('value', '0'), 16), 'ether')} ETH")
                                
                                # Calculate USDC value for display
                                for i, addr in enumerate(path):
                                    if addr.lower() == USDC_ADDRESS and i == len(path) - 1:
                                        print(f"USDC Value: ${Web3.from_wei(amount_out_min, 'mwei'):,.2f}")
                                
                                # Calculate and display pair addresses for each hop in the path
                                for i in range(len(path) - 1):
                                    pair_address = get_pair_address(path[i], path[i+1])
                                    print(f"Pair Address ({path[i][:6]}.../{path[i+1][:6]}...): {pair_address}")
                            except Exception as e2:
                                print(f"Error decoding V3 swapExactETHForTokens: Primary: {e1}, Alternative: {e2}")
                                print(f"Raw input params: {input_params[:100]}...")
                    except Exception as e:
                        print(f"Error decoding V3 swapExactETHForTokens: {e}")
            except Exception as e:
                print(f"Error parsing swap data: {e}")
                print(f"Function signature: {func_sig}")
                print(f"Input data (first 100 chars): {input_data[:100]}...")

        print(f"New to Transaction: {to}")
        print(f"Raw TX: {raw_tx}")
        return raw_tx
    return None
if __name__ == '__main__':
    asyncio.run(main())
