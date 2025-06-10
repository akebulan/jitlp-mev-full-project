import asyncio
import json
import os
from dotenv import load_dotenv
from websockets.legacy.client import connect
from websockets.exceptions import ConnectionClosedError

load_dotenv()
BLOXROUTE_AUTH_KEY = os.getenv("BLOXROUTE_AUTH_KEY")
BLOXROUTE_WSS = "wss://ws.blxrbdn.com/mempool"  # ✅ this is the correct WebSocket endpoint

SUBSCRIBE_MESSAGE = {
    "id": 1,
    "method": "subscribe",
    "params": {
        "subscription": "newTxs",
        "filters": [
            {
                "chains": ["Polygon"],
                "protocols": ["ethereum"]
            }
        ]
    }
}


async def main():
    headers = {
        "Authorization": f"Bearer {BLOXROUTE_AUTH_KEY}",
        "Sec-WebSocket-Protocol": "json"  # ✅ critical fix
    }

    print("🔌 Connecting to bloXroute WebSocket...")
    try:
        async with connect(BLOXROUTE_WSS, extra_headers=headers, ping_interval=20) as ws:
            print("✅ Connected to bloXroute WebSocket")
            print("🧾 Sent headers:", headers)

            try:
                initial_msg = await ws.recv()
                print("👋 Initial message:", initial_msg)
            except ConnectionClosedError as e:
                print(f"❌ Error receiving initial message: {e}")
                return

            await ws.send(json.dumps(SUBSCRIBE_MESSAGE))
            print("📡 Sent subscription")

            while True:
                try:
                    msg = await ws.recv()
                    print("📥 Received message:", msg)
                except ConnectionClosedError:
                    print("❌ WebSocket closed by server.")
                    break

    except Exception as e:
        print(f"❌ Unhandled exception: {e}")


if __name__ == "__main__":
    asyncio.run(main())
