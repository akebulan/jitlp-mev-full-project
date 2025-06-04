import { Signer } from "ethers";
import type { Provider } from "@ethersproject/providers";
import type { IScaledBalanceToken, IScaledBalanceTokenInterface } from "../../interfaces/IScaledBalanceToken";
export declare class IScaledBalanceToken__factory {
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
    static createInterface(): IScaledBalanceTokenInterface;
    static connect(address: string, signerOrProvider: Signer | Provider): IScaledBalanceToken;
}
//# sourceMappingURL=IScaledBalanceToken__factory.d.ts.map