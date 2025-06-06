const { ethers } = require('ethers');
const https = require('https');

const ALCHEMY_WS_URL = 'wss://base-mainnet.g.alchemy.com/v2/mHhjGOZeDUTGL2XjVPGgPuNrABWDJmwO';
const BASESCAN_API_KEY = 'MYERHHYJ57PVFD3W6YAGJRN45TTTASBCD9';
const provider = new ethers.WebSocketProvider(ALCHEMY_WS_URL);

const WETH = '0x4200000000000000000000000000000000000006'.toLowerCase();
const USDC = '0xd9aa7c4db446281f623cf1ed0e8d3b72a27d3f32'.toLowerCase();

const ROUTERS = {
  '0x2626664c2603336e57b271c5c0b26f421741e481': 'Uniswap V3',
  '0xdef1c0ded9bec7f1a1670819833240f027b25eff': '0x Exchange Proxy',
  '0x111111125421ca6dc452d289314280a0f8842a65': '1inch Aggregation',
  '0x9008d19f58aabd9ed0d60971565aa8510560ab41': 'CowSwap Settlement'
};

const knownSelectors = {
  '0x12aa3caf': {
    name: '0x Swap',
    abi: [
      'function swap(address, (address sellToken, address buyToken, address allowanceTarget, bytes swapCallData, uint256 sellAmount, uint256 minBuyAmount, uint256 deadline))'
    ]
  },
  '0x5ae401dc': {
    name: 'Uniswap Multicall',
    abi: ['function multicall(bytes[])']
  },
  '0xe449022e': {
    name: '1inch V3 Swap',
    abi: ['function uniswapV3Swap(uint256,uint256,uint256[],bytes[])']
  }
};

const format = (value, token) => ethers.formatUnits(value, token === USDC ? 6 : 18);

function timestamp() {
  return new Date().toISOString().replace('T', ' ').replace(/\..+/, '');
}

async function fetchAbiFromBasescan(address) {
  return new Promise((resolve, reject) => {
    const url = `https://api.basescan.org/api?module=contract&action=getabi&address=${address}&apikey=${BASESCAN_API_KEY}`;
    https.get(url, (res) => {
      let data = '';
      res.on('data', chunk => data += chunk);
      res.on('end', () => {
        try {
          const json = JSON.parse(data);
          if (json.status === '1') {
            resolve(JSON.parse(json.result));
          } else {
            resolve(null);
          }
        } catch (e) {
          reject(e);
        }
      });
    }).on('error', reject);
  });
}

async function decodeTransaction(tx) {
  const selector = tx.data.slice(0, 10).toLowerCase();
  const to = tx.to?.toLowerCase();
  const tag = ROUTERS[to] || 'Unknown Router';

  let iface;
  if (knownSelectors[selector]) {
    iface = new ethers.Interface(knownSelectors[selector].abi);
  } else {
    const abi = await fetchAbiFromBasescan(to);
    if (!abi) return;
    iface = new ethers.Interface(abi);
  }

  try {
    const decoded = iface.parseTransaction({ data: tx.data });
    const name = decoded.name;
    const args = decoded.args;

    const gas = tx.gasPrice ? ethers.formatUnits(tx.gasPrice, 'gwei') : 'N/A';
    const valueETH = ethers.formatEther(tx.value || 0);

    console.log(`🧠 ${timestamp()} | ${tag} — ${name}`);
    console.log(`Tx: ${tx.hash}`);
    console.log(`From: ${tx.from}`);
    console.log(`To:   ${tx.to}`);
    console.log(`Value Sent: ${valueETH} ETH`);
    console.log(`Selector: ${selector}`);
    console.log(`Gas Price: ${gas} gwei`);

    // Handle 0x swaps
    if (name === 'swap') {
      const sellToken = args[1].sellToken.toLowerCase();
      const buyToken = args[1].buyToken.toLowerCase();
      const amountIn = args[1].sellAmount;
      const minOut = args[1].minBuyAmount;

      const isRelevant =
          (sellToken === WETH && buyToken === USDC) ||
          (sellToken === USDC && buyToken === WETH);

      if (isRelevant) {
        const direction = sellToken === WETH ? 'WETH → USDC' : 'USDC → WETH';
        console.log(`Direction: ${direction}`);
        console.log(`Sell Amount: ${format(amountIn, sellToken)} ${sellToken === WETH ? 'WETH' : 'USDC'}`);
        console.log(`Min Out:     ${format(minOut, buyToken)} ${buyToken === WETH ? 'WETH' : 'USDC'}`);
      }
    }

    console.log('-----------------------------');
  } catch (err) {
    console.warn(`⚠️ Failed to decode tx ${tx.hash}:`, err.message);
  }
}

console.log('🔍 Mempool watching for WETH ↔ USDC swaps on Base...');

provider.on('pending', async (txHash) => {
  try {
    const tx = await provider.getTransaction(txHash);
    if (!tx || !tx.to) return;

    const to = tx.to.toLowerCase();
    if (Object.keys(ROUTERS).includes(to)) {
      await decodeTransaction(tx);
    }
  } catch (err) {
    // ignore
  }
});
