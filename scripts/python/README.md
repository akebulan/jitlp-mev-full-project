# Aave Liquidation Monitor

This script monitors Aave V3 positions on Base network and executes liquidations when health factors fall below 1.0.

## Features

- Monitors Aave V3 positions in real-time
- Identifies users with low health factors
- Finds collateral assets using on-chain data
- Executes liquidations through a flash loan contract
- Test mode for simulating liquidations

## Setup

1. Install dependencies:
```bash
pip install web3 requests python-dotenv
```

2. Set up environment variables in `.env`:
```
BASE_RPC=https://rpc.ankr.com/base/YOUR_API_KEY
PRIVATE_KEY=YOUR_PRIVATE_KEY
LIQUIDATOR_ADDRESS=YOUR_DEPLOYED_CONTRACT_ADDRESS
```

## Usage

### Basic monitoring:
```bash
python monitor_aave_liquidations_1.py
```

### Test mode (simulates liquidations for users with HF < 1.05):
```bash
python monitor_aave_liquidations_1.py --test
```

### Additional options:
```bash
python monitor_aave_liquidations_1.py --test --max-liquidations 3 --interval 30
```

## bloXroute Integration

The script includes bloXroute integration for MEV protection, but it requires:
1. A valid bloXroute subscription
2. Proper API access for Base network
3. Valid authentication credentials

To use bloXroute (if configured):
```bash
python monitor_aave_liquidations_1.py --bloxroute --auth YOUR_AUTH_TOKEN
```

## Security Notes

- Never commit your `.env` file with private keys
- Use a dedicated wallet with minimal funds for testing
- Rotate keys regularly
- Consider using a hardware wallet for production