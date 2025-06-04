import { Signer } from "ethers";
import type { Provider } from "@ethersproject/providers";
import type { IPriceOracleSentinel, IPriceOracleSentinelInterface } from "../../interfaces/IPriceOracleSentinel";
export declare class IPriceOracleSentinel__factory {
    static readonly abi: ({
        anonymous: boolean;
        inputs: {
            indexed: boolean;
            internalType: string;
            name: string;
            type: string;
        }[];
        name: string;
        type: string;
        outputs?: undefined;
        stateMutability?: undefined;
    } | {
        inputs: never[];
        name: string;
        outputs: {
            internalType: string;
            name: string;
            type: string;
        }[];
        stateMutability: string;
        type: string;
        anonymous?: undefined;
    } | {
        inputs: {
            internalType: string;
            name: string;
            type: string;
        }[];
        name: string;
        outputs: never[];
        stateMutability: string;
        type: string;
        anonymous?: undefined;
    })[];
    static createInterface(): IPriceOracleSentinelInterface;
    static connect(address: string, signerOrProvider: Signer | Provider): IPriceOracleSentinel;
}
//# sourceMappingURL=IPriceOracleSentinel__factory.d.ts.map