"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.getProxyAdmin = exports.getProxyImplementation = exports.buildDelegationWithSigParams = exports.getSignatureFromTypedData = exports.buildPermitParams = exports.convertToCurrencyDecimals = void 0;
const ethers_1 = require("ethers");
const eth_sig_util_1 = require("eth-sig-util");
const ethereumjs_util_1 = require("ethereumjs-util");
const deploy_v3_1 = require("@aave/deploy-v3");
const misc_utils_1 = require("./misc-utils");
const convertToCurrencyDecimals = async (tokenAddress, amount) => {
    const token = await (0, deploy_v3_1.getContract)('IERC20Detailed', tokenAddress);
    let decimals = (await token.decimals()).toString();
    return ethers_1.ethers.utils.parseUnits(amount, decimals);
};
exports.convertToCurrencyDecimals = convertToCurrencyDecimals;
const buildPermitParams = (chainId, token, revision, tokenName, owner, spender, nonce, deadline, value) => ({
    types: {
        EIP712Domain: [
            { name: 'name', type: 'string' },
            { name: 'version', type: 'string' },
            { name: 'chainId', type: 'uint256' },
            { name: 'verifyingContract', type: 'address' },
        ],
        Permit: [
            { name: 'owner', type: 'address' },
            { name: 'spender', type: 'address' },
            { name: 'value', type: 'uint256' },
            { name: 'nonce', type: 'uint256' },
            { name: 'deadline', type: 'uint256' },
        ],
    },
    primaryType: 'Permit',
    domain: {
        name: tokenName,
        version: revision,
        chainId: chainId,
        verifyingContract: token,
    },
    message: {
        owner,
        spender,
        value,
        nonce,
        deadline,
    },
});
exports.buildPermitParams = buildPermitParams;
const getSignatureFromTypedData = (privateKey, typedData // TODO: should be TypedData, from eth-sig-utils, but TS doesn't accept it
) => {
    const signature = (0, eth_sig_util_1.signTypedData_v4)(Buffer.from(privateKey.substring(2, 66), 'hex'), {
        data: typedData,
    });
    return (0, ethereumjs_util_1.fromRpcSig)(signature);
};
exports.getSignatureFromTypedData = getSignatureFromTypedData;
const buildDelegationWithSigParams = (chainId, token, revision, tokenName, delegatee, nonce, deadline, value) => ({
    types: {
        EIP712Domain: [
            { name: 'name', type: 'string' },
            { name: 'version', type: 'string' },
            { name: 'chainId', type: 'uint256' },
            { name: 'verifyingContract', type: 'address' },
        ],
        DelegationWithSig: [
            { name: 'delegatee', type: 'address' },
            { name: 'value', type: 'uint256' },
            { name: 'nonce', type: 'uint256' },
            { name: 'deadline', type: 'uint256' },
        ],
    },
    primaryType: 'DelegationWithSig',
    domain: {
        name: tokenName,
        version: revision,
        chainId: chainId,
        verifyingContract: token,
    },
    message: {
        delegatee,
        value,
        nonce,
        deadline,
    },
});
exports.buildDelegationWithSigParams = buildDelegationWithSigParams;
const getProxyImplementation = async (proxyAdminAddress, proxyAddress) => {
    // Impersonate proxy admin
    await (0, misc_utils_1.impersonateAccountsHardhat)([proxyAdminAddress]);
    const proxyAdminSigner = await hre.ethers.getSigner(proxyAdminAddress);
    const proxy = (await hre.ethers.getContractAt('InitializableImmutableAdminUpgradeabilityProxy', proxyAddress, proxyAdminSigner));
    const implementationAddress = await proxy.callStatic.implementation();
    return implementationAddress;
};
exports.getProxyImplementation = getProxyImplementation;
const getProxyAdmin = async (proxyAddress) => {
    const EIP1967_ADMIN_SLOT = '0xb53127684a568b3173ae13b9f8a6016e243e63b6e8ee1178d6a717850b5d6103';
    const adminStorageSlot = await hre.ethers.provider.getStorageAt(proxyAddress, EIP1967_ADMIN_SLOT, 'latest');
    const adminAddress = ethers_1.ethers.utils.defaultAbiCoder
        .decode(['address'], adminStorageSlot)
        .toString();
    return ethers_1.ethers.utils.getAddress(adminAddress);
};
exports.getProxyAdmin = getProxyAdmin;
