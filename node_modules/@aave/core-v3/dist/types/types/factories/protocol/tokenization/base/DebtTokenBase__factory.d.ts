import { Signer } from "ethers";
import type { Provider } from "@ethersproject/providers";
import type { DebtTokenBase, DebtTokenBaseInterface } from "../../../../protocol/tokenization/base/DebtTokenBase";
export declare class DebtTokenBase__factory {
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
    static createInterface(): DebtTokenBaseInterface;
    static connect(address: string, signerOrProvider: Signer | Provider): DebtTokenBase;
}
//# sourceMappingURL=DebtTokenBase__factory.d.ts.map