# Python 3.7 or higher required due to the use of asyncio.run()
import asyncio, json, ssl
from websocket import create_connection

async def main():
    try:
        ws = create_connection('wss://api.blxrbdn.com/ws',
                               header=["Authorization:{}".format("MTAzYWY1MjQtMDIwNC00OTNhLTk3NmItMWU4MTQ4ZGUxMDg0OmQwN2Q0MDQyZjI2NzY1ZDdhYTAwMTc0YjM0NDVlY2E3")],
                               sslopt={"cert_reqs": ssl.CERT_NONE})
        # ETH Example
        request = json.dumps({"id": "1", "method": "quota_usage", "params": "null"})
        # # BSC Example
        # request = json.dumps({"id": 1, "method": "blxr_tx", "params": {"transaction": "f86b0184...e0b58219", "blockchain_network": "BSC-Mainnet"}})

        ws.send(str(request))
        while True:
            response = json.loads(ws.recv())
            print(response) # or process it generally
    except Exception as e:
        print(f'Connection failed, Reason: {e}')


if __name__ == '__main__':
    asyncio.run(main())
