import { Signer } from "ethers";
import type { Provider } from "@ethersproject/providers";
import type { AggregatorInterface, AggregatorInterfaceInterface } from "../../../dependencies/chainlink/AggregatorInterface";
export declare class AggregatorInterface__factory {
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
    static createInterface(): AggregatorInterfaceInterface;
    static connect(address: string, signerOrProvider: Signer | Provider): AggregatorInterface;
}
//# sourceMappingURL=AggregatorInterface__factory.d.ts.map