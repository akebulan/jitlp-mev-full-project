import asyncio
import websockets

async def main():
    uri = "wss://api.blxrbdn.com/ws"
    async with websockets.connect(
        uri,
        extra_headers={"Authorization": "Bearer testkey"},
        ping_interval=20,
        ping_timeout=10
    ) as ws:
        print("✅ Connected (dummy test)")

asyncio.run(main())
