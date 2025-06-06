// decodeSwap.js
// Parses calldata from various router contracts to extract WETH/USDC swap intent

const { ethers } = require('ethers');

const WETH = '0x4200000000000000000000000000000000000006';
const USDC = '0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913';

const ifaceMap = {
    // Uniswap V3 exactInputSingle(address tokenIn, address tokenOut, ...)
    '0x414bf389': new ethers.Interface([
        'function exactInputSingle((address tokenIn, address tokenOut, uint24 fee, address recipient, uint256 deadline, uint256 amountIn, uint256 amountOutMinimum, uint160 sqrtPriceLimitX96))'
    ]),
    // 0x swap(address,address,(...))
    '0x12aa3caf': new ethers.Interface([
        'function swap(address,uint256,address,uint256,bytes)' // simplified
    ])
};

function normalize(addr) {
    return addr?.toLowerCase();
}

async function decodeSwapTx(tx) {
    const selector = tx.data.slice(0, 10);
    const iface = ifaceMap[selector];
    if (!iface) return null;

    try {
        const decoded = iface.parseTransaction({ data: tx.data });
        const args = decoded.args[0];

        let tokenIn, tokenOut, amountIn, amountOutMin;
        if (selector === '0x414bf389') {
            // exactInputSingle
            tokenIn = normalize(args.tokenIn);
            tokenOut = normalize(args.tokenOut);
            amountIn = args.amountIn.toString();
            amountOutMin = args.amountOutMinimum.toString();
        } else if (selector === '0x12aa3caf') {
            // simplified 0x
            tokenIn = normalize(args[0]);
            tokenOut = normalize(args[1]);
            amountIn = args[3].toString();
            amountOutMin = '0';
        } else {
            return null;
        }

        const direction = tokenIn === WETH ? 'WETH → USDC' : 'USDC → WETH';

        return {
            pool: normalize(tx.to),
            direction,
            amountIn,
            minOut: amountOutMin
        };
    } catch (err) {
        return null;
    }
}

module.exports = { decodeSwapTx };
