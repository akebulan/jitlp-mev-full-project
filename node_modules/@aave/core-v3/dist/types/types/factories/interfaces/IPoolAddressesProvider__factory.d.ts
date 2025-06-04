import { Signer } from "ethers";
import type { Provider } from "@ethersproject/providers";
import type { IPoolAddressesProvider, IPoolAddressesProviderInterface } from "../../interfaces/IPoolAddressesProvider";
export declare class IPoolAddressesProvider__factory {
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
    static createInterface(): IPoolAddressesProviderInterface;
    static connect(address: string, signerOrProvider: Signer | Provider): IPoolAddressesProvider;
}
//# sourceMappingURL=IPoolAddressesProvider__factory.d.ts.map