"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.impersonateAccountsHardhat = exports.setAutomineEvm = exports.setAutomine = exports.setBlocktime = exports.timeLatest = exports.createRandomAddress = void 0;
const ethers_1 = require("ethers");
const createRandomAddress = () => ethers_1.Wallet.createRandom().address;
exports.createRandomAddress = createRandomAddress;
const timeLatest = async () => {
    const block = await hre.ethers.provider.getBlock('latest');
    return ethers_1.BigNumber.from(block.timestamp);
};
exports.timeLatest = timeLatest;
const setBlocktime = async (time) => {
    await hre.ethers.provider.send('evm_setNextBlockTimestamp', [time]);
};
exports.setBlocktime = setBlocktime;
const setAutomine = async (activate) => {
    await hre.network.provider.send('evm_setAutomine', [activate]);
    if (activate)
        await hre.network.provider.send('evm_mine', []);
};
exports.setAutomine = setAutomine;
const setAutomineEvm = async (activate) => {
    await hre.network.provider.send('evm_setAutomine', [activate]);
};
exports.setAutomineEvm = setAutomineEvm;
const impersonateAccountsHardhat = async (accounts) => {
    if (process.env.TENDERLY === 'true') {
        return;
    }
    // eslint-disable-next-line no-restricted-syntax
    for (const account of accounts) {
        // eslint-disable-next-line no-await-in-loop
        await hre.network.provider.request({
            method: 'hardhat_impersonateAccount',
            params: [account],
        });
    }
};
exports.impersonateAccountsHardhat = impersonateAccountsHardhat;
