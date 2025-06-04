import { Signer } from "ethers";
import type { Provider } from "@ethersproject/providers";
import type { IFlashLoanSimpleReceiver, IFlashLoanSimpleReceiverInterface } from "../../../flashloan/interfaces/IFlashLoanSimpleReceiver";
export declare class IFlashLoanSimpleReceiver__factory {
    static readonly abi: {
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
    }[];
    static createInterface(): IFlashLoanSimpleReceiverInterface;
    static connect(address: string, signerOrProvider: Signer | Provider): IFlashLoanSimpleReceiver;
}
//# sourceMappingURL=IFlashLoanSimpleReceiver__factory.d.ts.map