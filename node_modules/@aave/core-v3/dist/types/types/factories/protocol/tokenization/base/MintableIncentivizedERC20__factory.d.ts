import { Signer } from "ethers";
import type { Provider } from "@ethersproject/providers";
import type { MintableIncentivizedERC20, MintableIncentivizedERC20Interface } from "../../../../protocol/tokenization/base/MintableIncentivizedERC20";
export declare class MintableIncentivizedERC20__factory {
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
    static createInterface(): MintableIncentivizedERC20Interface;
    static connect(address: string, signerOrProvider: Signer | Provider): MintableIncentivizedERC20;
}
//# sourceMappingURL=MintableIncentivizedERC20__factory.d.ts.map