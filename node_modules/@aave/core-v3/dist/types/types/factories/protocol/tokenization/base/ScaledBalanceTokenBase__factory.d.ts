import { Signer } from "ethers";
import type { Provider } from "@ethersproject/providers";
import type { ScaledBalanceTokenBase, ScaledBalanceTokenBaseInterface } from "../../../../protocol/tokenization/base/ScaledBalanceTokenBase";
export declare class ScaledBalanceTokenBase__factory {
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
        inputs: {
            internalType: string;
            name: string;
            type: string;
        }[];
        name: string;
        outputs: {
            internalType: string;
            name: string;
            type: string;
        }[];
        stateMutability: string;
        type: string;
        anonymous?: undefined;
    })[];
    static createInterface(): ScaledBalanceTokenBaseInterface;
    static connect(address: string, signerOrProvider: Signer | Provider): ScaledBalanceTokenBase;
}
//# sourceMappingURL=ScaledBalanceTokenBase__factory.d.ts.map