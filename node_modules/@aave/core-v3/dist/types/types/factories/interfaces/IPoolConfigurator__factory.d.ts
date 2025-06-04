import { Signer } from "ethers";
import type { Provider } from "@ethersproject/providers";
import type { IPoolConfigurator, IPoolConfiguratorInterface } from "../../interfaces/IPoolConfigurator";
export declare class IPoolConfigurator__factory {
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
    } | {
        inputs: {
            components: {
                internalType: string;
                name: string;
                type: string;
            }[];
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
    static createInterface(): IPoolConfiguratorInterface;
    static connect(address: string, signerOrProvider: Signer | Provider): IPoolConfigurator;
}
//# sourceMappingURL=IPoolConfigurator__factory.d.ts.map