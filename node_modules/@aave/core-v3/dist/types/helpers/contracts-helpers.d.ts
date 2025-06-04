import { ethers } from 'ethers';
import { ECDSASignature } from 'ethereumjs-util';
import { tEthereumAddress, tStringTokenSmallUnits } from './types';
export declare const convertToCurrencyDecimals: (tokenAddress: tEthereumAddress, amount: string) => Promise<ethers.BigNumber>;
export declare const buildPermitParams: (chainId: number, token: tEthereumAddress, revision: string, tokenName: string, owner: tEthereumAddress, spender: tEthereumAddress, nonce: number, deadline: string, value: tStringTokenSmallUnits) => {
    types: {
        EIP712Domain: {
            name: string;
            type: string;
        }[];
        Permit: {
            name: string;
            type: string;
        }[];
    };
    primaryType: "Permit";
    domain: {
        name: string;
        version: string;
        chainId: number;
        verifyingContract: string;
    };
    message: {
        owner: string;
        spender: string;
        value: string;
        nonce: number;
        deadline: string;
    };
};
export declare const getSignatureFromTypedData: (privateKey: string, typedData: any) => ECDSASignature;
export declare const buildDelegationWithSigParams: (chainId: number, token: tEthereumAddress, revision: string, tokenName: string, delegatee: tEthereumAddress, nonce: number, deadline: string, value: tStringTokenSmallUnits) => {
    types: {
        EIP712Domain: {
            name: string;
            type: string;
        }[];
        DelegationWithSig: {
            name: string;
            type: string;
        }[];
    };
    primaryType: "DelegationWithSig";
    domain: {
        name: string;
        version: string;
        chainId: number;
        verifyingContract: string;
    };
    message: {
        delegatee: string;
        value: string;
        nonce: number;
        deadline: string;
    };
};
export declare const getProxyImplementation: (proxyAdminAddress: string, proxyAddress: string) => Promise<string>;
export declare const getProxyAdmin: (proxyAddress: string) => Promise<string>;
//# sourceMappingURL=contracts-helpers.d.ts.map