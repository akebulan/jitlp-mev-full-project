import { Signer, ContractFactory, Overrides } from "ethers";
import type { Provider, TransactionRequest } from "@ethersproject/providers";
import type { PromiseOrValue } from "../../../../common";
import type { IsolationModeLogic, IsolationModeLogicInterface } from "../../../../protocol/libraries/logic/IsolationModeLogic";
type IsolationModeLogicConstructorParams = [signer?: Signer] | ConstructorParameters<typeof ContractFactory>;
export declare class IsolationModeLogic__factory extends ContractFactory {
    constructor(...args: IsolationModeLogicConstructorParams);
    deploy(overrides?: Overrides & {
        from?: PromiseOrValue<string>;
    }): Promise<IsolationModeLogic>;
    getDeployTransaction(overrides?: Overrides & {
        from?: PromiseOrValue<string>;
    }): TransactionRequest;
    attach(address: string): IsolationModeLogic;
    connect(signer: Signer): IsolationModeLogic__factory;
    static readonly bytecode = "0x60566037600b82828239805160001a607314602a57634e487b7160e01b600052600060045260246000fd5b30600052607381538281f3fe73000000000000000000000000000000000000000030146080604052600080fdfea2646970667358221220d2215214a28d82a7052ab556d4e217d1af346b5c73c03fd2d835b0da1773a2ab64736f6c634300080a0033";
    static readonly abi: {
        anonymous: boolean;
        inputs: {
            indexed: boolean;
            internalType: string;
            name: string;
            type: string;
        }[];
        name: string;
        type: string;
    }[];
    static createInterface(): IsolationModeLogicInterface;
    static connect(address: string, signerOrProvider: Signer | Provider): IsolationModeLogic;
}
export {};
//# sourceMappingURL=IsolationModeLogic__factory.d.ts.map