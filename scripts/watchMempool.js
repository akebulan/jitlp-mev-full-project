// watchMempool.js
// Monitors Base mempool for WETH/USDC swaps and triggers LP strategy using QuickNode
// Includes fallback polling to catch missed pending txs

const { ethers } = require('ethers');
const { decodeSwapTx } = require('./decodeSwap');
const { triggerLPStrategy } = require('./triggerLP');

const QUICKNODE_WS_URL = 'wss://stylish-red-wildflower.base-mainnet.quiknode.pro/d2df1554392e6deea8124dc6a19434b49bf0a53b/';
const provider = new ethers.WebSocketProvider(QUICKNODE_WS_URL);
const POLLING_INTERVAL = 10000; // fallback polling every 10 seconds

const ROUTERS = new Set([
  '0x2626664c2603336e57b271c5c0b26f421741e481', // Uniswap V3
  '0xdef1c0ded9bec7f1a1670819833240f027b25eff', // 0x
  '0x111111125421ca6dc452d289314280a0f8842a65', // 1inch
  '0x9008d19f58aabd9ed0d60971565aa8510560ab41'  // CowSwap
]);

console.log('🔍 JIT LP Watcher Active on Base (QuickNode + Polling)...');

provider.on('pending', async (txHash) => {
  try {
    const tx = await provider.getTransaction(txHash);
    if (!tx || !tx.to) return;
    await handleTransaction(tx);
  } catch (err) {
    console.error(`[pending error] ${txHash}: ${err.message}`);
  }
});

async function pollPendingBlock() {
  try {
    const block = await provider.send('eth_getBlockByNumber', ['pending', true]);
    if (!block || !block.transactions) return;
    for (const tx of block.transactions) {
      if (tx.to) await handleTransaction(tx);
    }
  } catch (err) {
    console.error(`[poll error] ${err.message}`);
  }
}

async function handleTransaction(tx) {
  const to = tx.to.toLowerCase();
  if (!ROUTERS.has(to)) return;
  console.log(`[MATCH] Router tx: ${tx.hash} to ${to}`);

  if (!tx.data || tx.data.length < 10) {
    console.log(`[SKIP] Tx ${tx.hash} has no valid input data`);
    return;
  }

  const swapData = await decodeSwapTx(tx);
  if (!swapData) return;

  console.log(`🚨 Detected WETH/USDC swap:
→ Direction: ${swapData.direction}
→ Amount In: ${swapData.amountIn}
→ Min Out: ${swapData.minOut}
→ From: ${tx.from}
→ Hash: ${tx.hash}`);

  await triggerLPStrategy(swapData, tx);
}

setInterval(pollPendingBlock, POLLING_INTERVAL);
