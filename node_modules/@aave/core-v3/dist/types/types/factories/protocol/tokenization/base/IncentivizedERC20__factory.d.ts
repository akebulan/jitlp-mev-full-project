import { Signer } from "ethers";
import type { Provider } from "@ethersproject/providers";
import type { IncentivizedERC20, IncentivizedERC20Interface } from "../../../../protocol/tokenization/base/IncentivizedERC20";
export declare class IncentivizedERC20__factory {
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
    static createInterface(): IncentivizedERC20Interface;
    static connect(address: string, signerOrProvider: Signer | Provider): IncentivizedERC20;
}
//# sourceMappingURL=IncentivizedERC20__factory.d.ts.map