import asyncio, json, ssl, websockets
import datetime


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

        # ETH Example
        subscribe_request = {
            # "jsonrpc": "2.0",
            "id": 1,
            "method": "subscribe",
            "params": [
                "pendingTxs",
                {
                    "include": ["tx_hash", "raw_tx", "tx_contents"],
                    "filters": "to in ["
                               "0x7a250d5630b4cf539739df2c5dacb4c659f2488d, " # Uniswap V2
                               "0xe592427a0aece92de3edee1f18e0157c05861564, " # Uniswap V3
                               "0xd9e1ce17f2641f24ae83637ab66a2cca9c378b9f, " # SushiSwap
                               "0xba12222222228d8ba445958a75a0704d566bf2c8, " # Balancer V2
                               "0xa5E0829CaCEd8fFDD4De3c43696c57F7D7A678ff, " # QuickSwap
                               "0xa5e0829caced8ffdd4de3c43696c57f7d7a678ff, " # QuickSwap lowercase
                               "0x1b02da8cb0d097eb8d57a175b88c7d8b47997506, " # Sushi
                               "0xE592427A0AEce92De3Edee1F18E0157C05861564, " # Uni v3
                               "0xe592427a0aece92de3edee1f18e0157c05861564 " # Uni v3 lowercase
                               "]",
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
    if "params" in tx_data and "result" in tx_data["params"]:
        result = tx_data["params"]["result"]
        print(f"[{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] result: {result}")
        tx_contents = result.get("txContents", "Unknown")
        to = tx_contents.get("to", "Unknown")
        raw_tx = result.get("rawTx", "Unknown")
        print(f"New to Transaction: {to}")
        return raw_tx
    return None

if __name__ == '__main__':
    asyncio.run(main())
