import { Signer } from "ethers";
import type { Provider } from "@ethersproject/providers";
import type { IERC20Detailed, IERC20DetailedInterface } from "../../../../dependencies/openzeppelin/contracts/IERC20Detailed";
export declare class IERC20Detailed__factory {
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
    static createInterface(): IERC20DetailedInterface;
    static connect(address: string, signerOrProvider: Signer | Provider): IERC20Detailed;
}
//# sourceMappingURL=IERC20Detailed__factory.d.ts.map