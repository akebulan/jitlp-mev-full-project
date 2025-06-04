# JIT LP MEV Strategy on Base

## Overview
This strategy uses an Aave flash loan to provide Just-In-Time liquidity to the WETH/USDC 0.5% pool on Uniswap v3 on the Base network. It watches for large swaps, bundles a liquidity provision, collects the fees, and repays Aave — all in one transaction.

## Structure

- `contracts/`: Solidity smart contract `JITLPWithAave.sol`
- `scripts/`: JS scripts for mempool monitoring, profit checks, and Flashbots bundling
- `.env.example`: Config example
- `hardhat.config.js`: Hardhat setup for deploying and testing

## Setup

1. Copy `.env.example` to `.env` and fill in your values
2. Install dependencies:
   ```
   npm install
   ```
3. Compile contract:
   ```
   npx hardhat compile
   ```
4. Deploy to Base:
   ```
   npx hardhat run scripts/deploy.js --network base
   ```
5. Start mempool watcher:
   ```
   node scripts/watchMempool.js
   ```

## Flashbots Bundling
Triggered automatically via `autoTriggerBundle.js` if expected fees > cost.

---

## 🔧 Build & Run Instructions

### 1. Install Dependencies

```bash
npm install --save-dev hardhat @nomicfoundation/hardhat-toolbox dotenv
npm install ethers @flashbots/ethers-provider-bundle
```

---

### 2. Configure `.env`

Copy `.env.example` to `.env` and fill in:

```
BASE_RPC_URL=https://base-mainnet.g.alchemy.com/v2/YOUR_API_KEY
PRIVATE_KEY=your_wallet_private_key
JIT_CONTRACT=your_deployed_contract_address
AAVE_POOL=0x...
WETH=0x...
USDC=0x...
UNISWAP_ROUTER=0x...
POSITION_MANAGER=0x...
```

---

### 3. Compile Contract

```bash
npx hardhat compile
```

---

### 4. Deploy to Base Network

Add a deploy script `scripts/deploy.js`:

```js
const hre = require("hardhat");

async function main() {
  const Contract = await hre.ethers.getContractFactory("JITLPWithAave");
  const contract = await Contract.deploy(
    process.env.AAVE_POOL,
    process.env.WETH,
    process.env.USDC,
    process.env.UNISWAP_ROUTER,
    process.env.POSITION_MANAGER
  );
  await contract.deployed();
  console.log("✅ Deployed to:", contract.address);
}

main().catch((error) => {
  console.error(error);
  process.exitCode = 1;
});
```

Then run:
```bash
npx hardhat run scripts/deploy.js --network base
```

---

### 5. Start Monitoring Strategy

```bash
node scripts/watchMempool.js
```

This will listen for Uniswap swaps and bundle a flash loan + LP transaction if profitable.

---

### ✅ Done
You're now live with a real MEV-aware LP bot on Base Mainnet.
