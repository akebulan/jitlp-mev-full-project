import { Signer, ContractFactory, Overrides } from "ethers";
import type { Provider, TransactionRequest } from "@ethersproject/providers";
import type { PromiseOrValue } from "../../../../common";
import type { ReserveLogic, ReserveLogicInterface } from "../../../../protocol/libraries/logic/ReserveLogic";
type ReserveLogicConstructorParams = [signer?: Signer] | ConstructorParameters<typeof ContractFactory>;
export declare class ReserveLogic__factory extends ContractFactory {
    constructor(...args: ReserveLogicConstructorParams);
    deploy(overrides?: Overrides & {
        from?: PromiseOrValue<string>;
    }): Promise<ReserveLogic>;
    getDeployTransaction(overrides?: Overrides & {
        from?: PromiseOrValue<string>;
    }): TransactionRequest;
    attach(address: string): ReserveLogic;
    connect(signer: Signer): ReserveLogic__factory;
    static readonly bytecode = "0x60566037600b82828239805160001a607314602a57634e487b7160e01b600052600060045260246000fd5b30600052607381538281f3fe73000000000000000000000000000000000000000030146080604052600080fdfea2646970667358221220b67b48e38d0b6703d367ce4558f5085a19bced7f68aeb09d1e6a84ae221ac48e64736f6c634300080a0033";
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
    static createInterface(): ReserveLogicInterface;
    static connect(address: string, signerOrProvider: Signer | Provider): ReserveLogic;
}
export {};
//# sourceMappingURL=ReserveLogic__factory.d.ts.map