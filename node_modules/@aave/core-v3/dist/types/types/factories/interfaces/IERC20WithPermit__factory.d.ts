import { Signer } from "ethers";
import type { Provider } from "@ethersproject/providers";
import type { IERC20WithPermit, IERC20WithPermitInterface } from "../../interfaces/IERC20WithPermit";
export declare class IERC20WithPermit__factory {
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
    static createInterface(): IERC20WithPermitInterface;
    static connect(address: string, signerOrProvider: Signer | Provider): IERC20WithPermit;
}
//# sourceMappingURL=IERC20WithPermit__factory.d.ts.map