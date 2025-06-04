import { Signer } from "ethers";
import type { Provider } from "@ethersproject/providers";
import type { IInitializableDebtToken, IInitializableDebtTokenInterface } from "../../interfaces/IInitializableDebtToken";
export declare class IInitializableDebtToken__factory {
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
        outputs: never[];
        stateMutability: string;
        type: string;
        anonymous?: undefined;
    })[];
    static createInterface(): IInitializableDebtTokenInterface;
    static connect(address: string, signerOrProvider: Signer | Provider): IInitializableDebtToken;
}
//# sourceMappingURL=IInitializableDebtToken__factory.d.ts.map