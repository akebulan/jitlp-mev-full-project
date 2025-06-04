import { Signer } from "ethers";
import type { Provider } from "@ethersproject/providers";
import type { IPoolDataProvider, IPoolDataProviderInterface } from "../../interfaces/IPoolDataProvider";
export declare class IPoolDataProvider__factory {
    static readonly abi: ({
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
    } | {
        inputs: never[];
        name: string;
        outputs: {
            components: {
                internalType: string;
                name: string;
                type: string;
            }[];
            internalType: string;
            name: string;
            type: string;
        }[];
        stateMutability: string;
        type: string;
    })[];
    static createInterface(): IPoolDataProviderInterface;
    static connect(address: string, signerOrProvider: Signer | Provider): IPoolDataProvider;
}
//# sourceMappingURL=IPoolDataProvider__factory.d.ts.map