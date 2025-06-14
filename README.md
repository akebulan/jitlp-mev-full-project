# JITLP MEV Project

This project contains smart contracts and scripts for MEV opportunities on Base blockchain, focusing on Aave liquidations and Just-In-Time Liquidity Provision.

## Components

### Smart Contracts

- **AaveV3Liquidator**: Flash loan liquidator for Aave V3 positions
- **JITLPWithAave**: Just-In-Time Liquidity Provider using Aave

### Scripts

- **monitor_aave_liquidations_1.py**: Monitors Aave positions and executes liquidations
- **aave_collateral_finder.py**: Finds collateral assets for users by querying Aave contracts
- **bloxroute_liquidator.py**: Executes liquidations through bloXroute for MEV protection

## Setup

1. Install dependencies:
```bash
# Smart contracts
npm install

# Python scripts
pip install web3 requests python-dotenv
```

2. Set up environment variables in `.env`:
```
# RPC URLs
BASE_RPC=https://rpc.ankr.com/base/YOUR_API_KEY

# Contract addresses
LIQUIDATOR_ADDRESS=YOUR_DEPLOYED_CONTRACT_ADDRESS

# Private key (NEVER commit this to git)
PRIVATE_KEY=YOUR_PRIVATE_KEY

# bloXroute configuration (optional)
BLOXROUTE_BASE_URL=https://api.blxrbdn.com
BLOXROUTE_AUTH_HEADER=YOUR_BLOXROUTE_AUTH_TOKEN
```

3. Deploy the contracts:
```bash
npx hardhat run scripts/deploy-aave-liquidator.js --network base
```

## Usage

### Monitoring Aave Liquidations

Basic monitoring:
```bash
python scripts/python/monitor_aave_liquidations_1.py
```

Test mode (simulates liquidations for users with HF < 1.05):
```bash
python scripts/python/monitor_aave_liquidations_1.py --test
```

With bloXroute for MEV protection:
```bash
python scripts/python/monitor_aave_liquidations_1.py --bloxroute
```

Additional options:
```bash
python scripts/python/monitor_aave_liquidations_1.py --test --max-liquidations 3 --interval 30
```

### Finding User Collateral

```bash
python scripts/python/aave_collateral_finder.py 0xUSER_ADDRESS
```

## Security Notes

- Never commit your `.env` file with private keys
- Use a dedicated wallet with minimal funds for testing
- Rotate keys regularly
- Consider using a hardware wallet for production

## License

MIT