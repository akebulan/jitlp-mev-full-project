import requests
import time

SUBGRAPH_URL = "https://gateway.thegraph.com/api/1a8f7cc18094075c9ab149357cabf07a/subgraphs/id/EAfvtfPqhv9BJ6iEnZGL3HBJ2HYiF7hBP3GS3XkZ5k9F"

QUERY = """
{
  users(first: 50, where: {healthFactor_lt: "1.0", borrowedReservesCount_gt: 0}) {
    id
    healthFactor
    totalCollateralUSD
    totalBorrowsUSD
  }
}
"""

def check_risky_accounts():
    try:
        res = requests.post(SUBGRAPH_URL, json={'query': QUERY})
        data = res.json()

        risky = data['data']['users']
        if not risky:
            print("✅ No liquidation candidates at the moment.")
        else:
            print(f"\n🚨 Found {len(risky)} risky borrowers:")
            for user in risky:
                print(f"  - {user['id'][:8]}... | HF: {float(user['healthFactor']):.4f} | "
                      f"Collateral: ${float(user['totalCollateralUSD']):,.2f} | "
                      f"Debt: ${float(user['totalBorrowsUSD']):,.2f}")
    except Exception as e:
        print("❌ Error fetching data:", e)

if __name__ == "__main__":
    while True:
        check_risky_accounts()
        time.sleep(30)

