"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.BLOCK_TO_FORK = exports.NETWORKS_RPC_URL = exports.buildForkConfig = void 0;
const types_1 = require("./helpers/types");
require('dotenv').config();
const INFURA_KEY = process.env.INFURA_KEY || '';
const ALCHEMY_KEY = process.env.ALCHEMY_KEY || '';
const TENDERLY_FORK_ID = process.env.TENDERLY_FORK_ID || '';
const FORK = process.env.FORK || '';
const FORK_BLOCK_NUMBER = process.env.FORK_BLOCK_NUMBER
    ? parseInt(process.env.FORK_BLOCK_NUMBER)
    : 0;
const GWEI = 1000 * 1000 * 1000;
const buildForkConfig = () => {
    let forkMode;
    if (FORK) {
        forkMode = {
            url: exports.NETWORKS_RPC_URL[FORK],
        };
        if (FORK_BLOCK_NUMBER || exports.BLOCK_TO_FORK[FORK]) {
            forkMode.blockNumber = FORK_BLOCK_NUMBER || exports.BLOCK_TO_FORK[FORK];
        }
    }
    return forkMode;
};
exports.buildForkConfig = buildForkConfig;
exports.NETWORKS_RPC_URL = {
    [types_1.eEthereumNetwork.kovan]: ALCHEMY_KEY
        ? `https://eth-kovan.alchemyapi.io/v2/${ALCHEMY_KEY}`
        : `https://kovan.infura.io/v3/${INFURA_KEY}`,
    [types_1.eEthereumNetwork.ropsten]: ALCHEMY_KEY
        ? `https://eth-ropsten.alchemyapi.io/v2/${ALCHEMY_KEY}`
        : `https://ropsten.infura.io/v3/${INFURA_KEY}`,
    [types_1.eEthereumNetwork.main]: ALCHEMY_KEY
        ? `https://eth-mainnet.alchemyapi.io/v2/${ALCHEMY_KEY}`
        : `https://mainnet.infura.io/v3/${INFURA_KEY}`,
    [types_1.eEthereumNetwork.coverage]: 'http://localhost:8555',
    [types_1.eEthereumNetwork.hardhat]: 'http://localhost:8545',
    [types_1.eEthereumNetwork.tenderlyMain]: `https://rpc.tenderly.co/fork/${TENDERLY_FORK_ID}`,
};
exports.BLOCK_TO_FORK = {
    [types_1.eEthereumNetwork.main]: 12406069,
    [types_1.eEthereumNetwork.kovan]: undefined,
    [types_1.eEthereumNetwork.ropsten]: undefined,
    [types_1.eEthereumNetwork.coverage]: undefined,
    [types_1.eEthereumNetwork.hardhat]: undefined,
    [types_1.eEthereumNetwork.tenderlyMain]: 12406069,
};
