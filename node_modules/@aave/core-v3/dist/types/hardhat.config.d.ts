import '@nomicfoundation/hardhat-toolbox';
import 'hardhat-deploy';
import '@tenderly/hardhat-tenderly';
import 'hardhat-contract-sizer';
import 'hardhat-dependency-compiler';
import '@nomicfoundation/hardhat-chai-matchers';
declare const hardhatConfig: {
    gasReporter: {
        enabled: boolean;
    };
    contractSizer: {
        alphaSort: boolean;
        runOnCompile: boolean;
        disambiguatePaths: boolean;
    };
    solidity: {
        version: string;
        settings: {
            optimizer: {
                enabled: boolean;
                runs: number;
            };
            evmVersion: string;
        };
    };
    typechain: {
        outDir: string;
        target: string;
    };
    mocha: {
        timeout: number;
        bail: boolean;
    };
    tenderly: {
        project: string;
        username: string;
        forkNetwork: string;
    };
    networks: {
        coverage: {
            url: string;
            chainId: number;
            throwOnTransactionFailures: boolean;
            throwOnCallFailures: boolean;
        };
        hardhat: {
            hardfork: string;
            blockGasLimit: number;
            gas: number;
            gasPrice: number;
            chainId: number;
            throwOnTransactionFailures: boolean;
            throwOnCallFailures: boolean;
            forking: import("hardhat/types").HardhatNetworkForkingUserConfig | undefined;
            allowUnlimitedContractSize: boolean;
            accounts: any;
        };
        ganache: {
            url: string;
            accounts: {
                mnemonic: string;
                path: string;
                initialIndex: number;
                count: number;
            };
        };
    };
    namedAccounts: {
        deployer: {
            default: number;
        };
        aclAdmin: {
            default: number;
        };
        emergencyAdmin: {
            default: number;
        };
        poolAdmin: {
            default: number;
        };
        addressesProviderRegistryOwner: {
            default: number;
        };
        treasuryProxyAdmin: {
            default: number;
        };
        incentivesProxyAdmin: {
            default: number;
        };
        incentivesEmissionManager: {
            default: number;
        };
        incentivesRewardsVault: {
            default: number;
        };
    };
    external: {
        contracts: {
            artifacts: string;
            deploy: string;
        }[];
    };
};
export default hardhatConfig;
//# sourceMappingURL=hardhat.config.d.ts.map