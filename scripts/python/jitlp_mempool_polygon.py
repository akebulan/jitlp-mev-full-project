import asyncio
import datetime
import json
import websockets
from web3 import Web3
from eth_abi import decode_abi

QUICKNODE_WS = 'wss://tiniest-thrumming-research.matic.quiknode.pro/9309689ad8cd10f8f068c0d227ed6bb1b0289e7e/'
ROUTERS = {
    'uniswap': '0x68b3465833fb72A70ecDF485E0e4C7bD8665Fc45'.lower(),
    'quickswap': '0xEf1c6E67703c7BD7107eed8303Fbe6EC2554BF6B'.lower()
}
FACTORY = '0x1F98431c8aD98523631AE4a59f267346ea31F984'
POOL_INIT_CODE_HASH = '0xe34f199b19b2b4f47f68442619d555527d244f78a3297ea89325f843f87b8b54'

SWAP_SIGS = {
    '0x04e45aaf': 'exactInputSingle',
    '0x5023b4df': 'exactOutputSingle',
    '0x472b43f3': 'exactInput',
    '0x09b81346': 'exactOutput'
}

w3 = Web3(Web3.HTTPProvider("https://polygon-rpc.com"))

POOL_ABI = json.loads('[{"inputs":[],"name":"slot0","outputs":[{"internalType":"uint160","name":"sqrtPriceX96","type":"uint160"},{"internalType":"int24","name":"tick","type":"int24"},{"internalType":"uint16","name":"observationIndex","type":"uint16"},{"internalType":"uint16","name":"observationCardinality","type":"uint16"},{"internalType":"uint16","name":"observationCardinalityNext","type":"uint16"},{"internalType":"uint8","name":"feeProtocol","type":"uint8"},{"internalType":"bool","name":"unlocked","type":"bool"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"liquidity","outputs":[{"internalType":"uint128","name":"","type":"uint128"}],"stateMutability":"view","type":"function"}]')

async def monitor():
    print("🔍 Watching for Uniswap v3 + QuickSwap swaps on Polygon (QuickNode)...")
    while True:
        try:
            async with websockets.connect(QUICKNODE_WS, ping_interval=20, ping_timeout=10) as ws:
                await ws.send(json.dumps({
                    "jsonrpc": "2.0",
                    "id": 1,
                    "method": "eth_subscribe",
                    "params": ["newPendingTransactions"]
                }))
                sub_response = await ws.recv()
                print(f"📡 Subscribed: {sub_response}")

                while True:
                    try:
                        # Optional ping check
                        pong_waiter = await ws.ping()
                        await asyncio.wait_for(pong_waiter, timeout=5)

                        message = await asyncio.wait_for(ws.recv(), timeout=20)
                        msg = json.loads(message)
                        if 'params' in msg and 'result' in msg['params']:
                            tx_hash = msg['params']['result']
                            await handle_tx(tx_hash)
                            await asyncio.sleep(0.25)
                    except asyncio.TimeoutError:
                        print("⏱️ Timeout waiting for messages, reconnecting...")
                        break
                    except Exception as inner:
                        print(f"❌ Inner loop error: {inner}")
                        break
        except Exception as outer:
            print(f"❌ Outer loop error (reconnecting): {outer}")
            await asyncio.sleep(5)

async def handle_tx(tx_hash):
    try:
        tx = w3.eth.get_transaction(tx_hash)
        if tx and tx.to:
            to = tx.to.lower()
            if to in ROUTERS.values():
                sig = tx.input[:10]
                if sig in SWAP_SIGS:
                    router_name = [k for k, v in ROUTERS.items() if v == to][0]
                    print(f"[{datetime.datetime.now().time()}] Potential JIT swap on {router_name.title()}: {tx_hash} ({SWAP_SIGS[sig]})")
                    await inspect_pool(tx, sig)
    except Exception:
        pass

def get_pool_address(token0, token1, fee):
    token0, token1 = sorted([Web3.toChecksumAddress(token0), Web3.toChecksumAddress(token1)])
    salt = Web3.solidityKeccak(['address', 'address', 'uint24'], [token0, token1, fee])
    packed = b'\xff' + bytes.fromhex(FACTORY[2:]) + salt + bytes.fromhex(POOL_INIT_CODE_HASH[2:])
    return Web3.toChecksumAddress(Web3.keccak(packed)[12:].hex())

async def inspect_pool(tx, sig):
    try:
        calldata = tx.input[10:]
        if sig in ['0x04e45aaf', '0x5023b4df']:
            types = ['address', 'address', 'uint24', 'address', 'uint256', 'uint256', 'uint160']
            decoded = decode_abi(types, bytes.fromhex(calldata))
            token0, token1, fee = decoded[0], decoded[1], decoded[2]
        elif sig in ['0x472b43f3', '0x09b81346']:
            path_offset = int(calldata[64:128], 16) * 2
            path = calldata[128 + path_offset:]
            if len(path) < 86:
                print("⚠️ Multi-hop swaps not yet decoded.")
                return
            token0 = '0x' + path[:40]
            fee = int(path[40:46], 16)
            token1 = '0x' + path[46:86]
        else:
            return

        pool_address = get_pool_address(token0, token1, fee)
        code = w3.eth.get_code(pool_address)
        if code == b'' or code == b'0x':
            print(f"❌ No pool contract found at {pool_address} (tokens: {token0[:6]}.../{token1[:6]}, fee: {fee})")
            return

        pool = w3.eth.contract(address=pool_address, abi=POOL_ABI)
        slot0 = pool.functions.slot0().call()
        liquidity = pool.functions.liquidity().call()
        print(f"➡️  Pool {pool_address} | Tick: {slot0[1]} | Liquidity: {liquidity}")
    except Exception as e:
        print(f"❌ Failed to inspect pool: {e}")

if __name__ == "__main__":
    asyncio.run(monitor())
